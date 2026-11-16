"""Export CVAT job annotations to YOLO format and optionally fine-tune YOLO.

Examples:
  python scripts/train_from_cvat.py --job 285 --export-only
  python scripts/train_from_cvat.py --job 285 --train --model yolo26s.pt
  python scripts/train_from_cvat.py --job 285 --train --model yolo26l.pt --device 0
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

from cvat_tools.core import paths
from cvat_tools.core.client import Cvat
from cvat_tools.learning.yolo_exporter import export_cvat_to_yolo

IMG_EXTS = (".jpg", ".jpeg", ".png")


def _find_local_frame(frames_dir: Path, job_id: int, fid: int) -> Path | None:
    if not frames_dir.exists():
        return None
    candidates = [
        f"frame_{fid:06d}",
        f"j{job_id}_f{fid}",
        f"{fid:06d}",
        str(fid),
    ]
    for stem in candidates:
        for ext in IMG_EXTS:
            p = frames_dir / f"{stem}{ext}"
            if p.exists():
                return p
    return None


def _resolve_checkpoint(model_arg: str) -> Path:
    p = Path(model_arg)
    if p.exists():
        return p
    ckpt = paths.CHECKPOINTS / model_arg
    if ckpt.exists():
        return ckpt
    raise FileNotFoundError(
        f"Checkpoint not found: {model_arg!r} (also checked {paths.CHECKPOINTS})"
    )


def _load_train_config(config_path: Path | None, job_id: int) -> dict[str, Any]:
    if config_path is None:
        candidate = paths.CONFIG / "training" / f"job{job_id}_yolo.yaml"
        config_path = candidate if candidate.exists() else paths.CONFIG / "training" / "job285_yolo.yaml"
    if not config_path.exists():
        return {}
    return yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}


def _gather_frames(
    cv: Cvat | None,
    job_id: int,
    frame_ids: list[int],
    frames_dir: Path,
) -> dict[int, Path]:
    frames_dir.mkdir(parents=True, exist_ok=True)
    frame_images: dict[int, Path] = {}
    for fid in frame_ids:
        local = _find_local_frame(frames_dir, job_id, fid)
        if local is not None:
            frame_images[fid] = local
            continue
        if cv is None:
            continue
        dst = frames_dir / f"frame_{fid:06d}.jpg"
        dst.write_bytes(cv.frame(job_id, fid))
        frame_images[fid] = dst
    return frame_images


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Export CVAT annotations to YOLO and fine-tune.")
    ap.add_argument("--job", type=int, default=285, help="CVAT job ID (default: 285)")
    ap.add_argument("--profile", default="local", help="CVAT config profile (default: local)")
    ap.add_argument(
        "--export-only",
        action="store_true",
        help="Only export YOLO dataset without training (default behavior unless --train is set)",
    )
    ap.add_argument("--train", action="store_true", help="Run Ultralytics fine-tuning after export")
    ap.add_argument(
        "--model",
        default=None,
        help="Base checkpoint in models/checkpoints/ (e.g. yolo26s.pt or yolo26l.pt)",
    )
    ap.add_argument("--config", type=Path, default=None, help="Training YAML config path")
    ap.add_argument("--out-dir", type=Path, default=None, help="Output YOLO dataset directory")
    ap.add_argument("--frames-dir", type=Path, default=None, help="Local frame cache directory")
    ap.add_argument("--annotations-json", type=Path, default=None, help="Optional offline CVAT annotations JSON")
    ap.add_argument("--val-ratio", type=float, default=None, help="Validation split ratio")
    ap.add_argument("--epochs", type=int, default=None, help="Override training epochs")
    ap.add_argument("--batch", type=int, default=None, help="Override training batch size")
    ap.add_argument("--imgsz", type=int, default=None, help="Override training image size")
    ap.add_argument("--device", default=None, help="Training device (e.g. cpu, 0)")
    return ap


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = build_parser().parse_args(argv)
    cfg = _load_train_config(args.config, args.job)

    out_dir = args.out_dir or (paths.DATA / "datasets" / f"job{args.job}_yolo")
    frames_dir = args.frames_dir or (paths.DATA / "jobs" / str(args.job) / "frames")
    val_ratio = args.val_ratio if args.val_ratio is not None else float(cfg.get("val_ratio", 0.2))
    seed = int(cfg.get("seed", 42))

    cv: Cvat | None = None
    if args.annotations_json is not None:
        payload = json.loads(args.annotations_json.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            shapes = payload
            id_to_label = {}
        else:
            shapes = payload.get("shapes", [])
            id_to_label = {int(k): str(v) for k, v in payload.get("id_to_label", {}).items()}
    else:
        cv = Cvat.from_env(profile=args.profile)
        id_to_label = {int(lbl["id"]): str(lbl["name"]) for lbl in cv.labels(args.job)}
        shapes = cv.annotations(args.job).get("shapes", [])

    annotated_fids = sorted({int(s["frame"]) for s in shapes if s.get("type") == "rectangle" and "frame" in s})
    frame_images = _gather_frames(cv, args.job, annotated_fids, frames_dir)

    summary = export_cvat_to_yolo(
        shapes=shapes,
        id_to_label=id_to_label,
        frame_images=frame_images,
        out_dir=out_dir,
        val_ratio=val_ratio,
        seed=seed,
    )
    (out_dir / "export_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if args.export_only or not args.train:
        return 0

    model_name = args.model or str(cfg.get("base_model", "yolo26s.pt"))
    ckpt_path = _resolve_checkpoint(model_name)

    from ultralytics import YOLO

    train_kwargs: dict[str, Any] = {
        "data": summary["data_yaml"],
        "imgsz": args.imgsz or int(cfg.get("imgsz", 960)),
        "epochs": args.epochs or int(cfg.get("epochs", 50)),
        "batch": args.batch or int(cfg.get("batch", 4)),
        "patience": int(cfg.get("patience", 15)),
        "workers": int(cfg.get("workers", 0)),
        "mosaic": float(cfg.get("mosaic", 0.5)),
        "hsv_h": float(cfg.get("hsv_h", 0.015)),
        "hsv_s": float(cfg.get("hsv_s", 0.7)),
        "hsv_v": float(cfg.get("hsv_v", 0.4)),
        "fliplr": float(cfg.get("fliplr", 0.5)),
        "scale": float(cfg.get("scale", 0.5)),
        "seed": seed,
        "project": str(paths.WORKSPACE / cfg.get("project", "data/training")),
        "name": str(cfg.get("name", f"job{args.job}_yolo")),
    }
    if args.device is not None:
        train_kwargs["device"] = args.device

    model = YOLO(str(ckpt_path))
    model.train(**train_kwargs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
