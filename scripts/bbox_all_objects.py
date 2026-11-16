"""Unified end-to-end all-object bbox pipeline (replaces cars_first.py).

Learns from human CVAT annotations, runs night-aware multiscale detection +
dedicated traffic-sign/light detection, applies job conventions, evaluates
against human boxes, exports previews/reports/drafts, and optionally pushes
new boxes to CVAT (with backup + source='manual' + dedupe_against_human).

Usage:
  python scripts/bbox_all_objects.py --job 285 --frames 60-79 --learn
  python scripts/bbox_all_objects.py --job 285 --frames 60-79 --backend openvino
  python scripts/bbox_all_objects.py --job 285 --frames 60-79 --push
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path
from typing import Any

import cv2
import numpy as np

WORKSPACE = Path(__file__).resolve().parents[1]
SRC_DIR = WORKSPACE / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cvat_tools.core import paths  # noqa: E402
from cvat_tools.core import transactions as tx  # noqa: E402
from cvat_tools.core.client import Cvat, WriteNotAuthorized  # noqa: E402
from cvat_tools.learning.types import Detection  # noqa: E402


def parse_frames(spec: str) -> list[int]:
    """Parse frame range spec like '60-79', '71', or '60-65,71'."""
    frames: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, _, end_s = part.partition("-")
            start, end = int(start_s), int(end_s)
            frames.extend(range(start, end + 1))
        else:
            frames.append(int(part))
    return sorted(set(frames))


def compute_iou(a: list[float], b: list[float]) -> float:
    """Compute IoU between two [x1, y1, x2, y2] boxes."""
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    if inter <= 0.0:
        return 0.0
    area_a = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
    area_b = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
    union = area_a + area_b - inter
    return inter / union if union > 0.0 else 0.0


def nms_detections(dets: list[Detection], iou_thresh: float = 0.55) -> list[Detection]:
    """Class-aware greedy NMS plus cross-class vehicle suppression (car vs truck/bus/train)."""
    vehicle_group = {"car", "truck", "bus", "train"}
    kept: list[Detection] = []
    for det in sorted(
        dets,
        key=lambda d: (d.conf + (0.15 if d.label == "car" else 0.0)),
        reverse=True,
    ):
        conflict = False
        for k in kept:
            iou = compute_iou(k.box, det.box)
            if k.label == det.label and iou >= iou_thresh:
                conflict = True
                break
            if k.label in vehicle_group and det.label in vehicle_group and iou >= 0.70:
                conflict = True
                break
        if conflict:
            continue
        kept.append(det)
    return kept


def load_frame_image(cv: Any, job_id: int, frame_idx: int) -> np.ndarray:
    """Load frame image from local cache if available, otherwise from CVAT."""
    candidates = [
        paths.DATA / "jobs" / str(job_id) / "frames" / f"f{frame_idx}.jpg",
        paths.COPILOT / "frames" / f"j{job_id}_f{frame_idx}.jpg",
    ]
    for p in candidates:
        if p.exists():
            img = cv2.imread(str(p), cv2.IMREAD_COLOR)
            if img is not None:
                return img
    raw = cv.frame(job_id, frame_idx)
    arr = np.frombuffer(raw, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError(f"Failed to decode frame {frame_idx} for job {job_id}")
    return img


def match_detections(
    dets: list[Detection],
    human_boxes: list[tuple[str, list[float]]],
    iou_thresh: float = 0.5,
) -> tuple[
    list[tuple[Detection, str]],
    list[Detection],
    list[tuple[str, list[float]]],
]:
    """Match machine detections against human boxes greedily by confidence & IoU."""
    used: set[int] = set()
    matched: list[tuple[Detection, str]] = []
    extra: list[Detection] = []

    for det in sorted(dets, key=lambda d: -d.conf):
        best_iou = 0.0
        best_idx = -1
        for idx, (h_label, h_box) in enumerate(human_boxes):
            if idx in used:
                continue
            score = compute_iou(det.box, h_box)
            # Prefer exact label match on ties
            if score >= iou_thresh and (
                score > best_iou
                or (abs(score - best_iou) < 1e-6 and h_label == det.label)
            ):
                best_iou = score
                best_idx = idx
        if best_idx >= 0:
            used.add(best_idx)
            matched.append((det, human_boxes[best_idx][0]))
        else:
            extra.append(det)

    missed = [h for idx, h in enumerate(human_boxes) if idx not in used]
    return matched, extra, missed


def draw_frame_preview(
    img: np.ndarray,
    frame_idx: int,
    night: bool,
    matched: list[tuple[Detection, str]],
    extra: list[Detection],
    missed: list[tuple[str, list[float]]],
    n_human: int,
    elapsed_s: float,
) -> np.ndarray:
    """Draw green=khop, red=thua(do), yellow=bo sot(vang) boxes with label names."""
    vis = img.copy()
    h_img, w_img = vis.shape[:2]

    for det, human_label in matched:
        x1, y1, x2, y2 = map(int, det.box)
        cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 200, 0), 2)
        tag = det.label if det.label == human_label else f"{det.label}({human_label})"
        cv2.putText(
            vis,
            f"{tag} {det.conf:.2f}",
            (x1 + 2, max(38, y1 + 14)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            (0, 200, 0),
            1,
            cv2.LINE_AA,
        )

    for det in extra:
        x1, y1, x2, y2 = map(int, det.box)
        cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(
            vis,
            f"{det.label} {det.conf:.2f}",
            (x1 + 2, max(38, y1 + 14)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )

    for h_label, h_box in missed:
        x1, y1, x2, y2 = map(int, h_box)
        cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.putText(
            vis,
            f"nguoi:{h_label}",
            (x1 + 2, max(38, y1 + 14)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 200, 255),
            1,
            cv2.LINE_AA,
        )

    title = (
        f"f{frame_idx} {'TOI' if night else 'SANG'} | "
        f"khop {len(matched)}  thua(do) {len(extra)}  bo sot(vang) {len(missed)} | "
        f"nguoi {n_human}  {elapsed_s:.1f}s"
    )
    cv2.rectangle(vis, (0, 0), (w_img, 30), (255, 255, 255), -1)
    cv2.putText(vis, title, (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 0), 2, cv2.LINE_AA)
    return vis


def build_contact_sheet(thumbs: list[np.ndarray], cols: int = 4) -> np.ndarray:
    """Assemble thumbnail grid (4x5 for 20 frames) padded with white tiles."""
    if not thumbs:
        return np.full((360, 640 * cols, 3), 255, dtype=np.uint8)
    padded = list(thumbs)
    while len(padded) % cols != 0:
        padded.append(np.full_like(padded[0], 255))
    rows = [np.hstack(padded[i : i + cols]) for i in range(0, len(padded), cols)]
    return np.vstack(rows)


def _prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    f1 = (
        2.0 * precision * recall / (precision + recall)
        if (precision + recall) > 0.0
        else 0.0
    )
    return recall, precision, f1


def write_csv_report(path: Path, frame_rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "frame",
        "sang_toi",
        "hop_nguoi",
        "hop_may",
        "khop_IoU0.5",
        "dung_nhan",
        "may_thua",
        "may_bo_sot",
        "recall",
        "precision",
        "f1",
        "giay",
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(frame_rows)


def write_md_report(
    path: Path,
    job_id: int,
    frame_rows: list[dict[str, Any]],
    label_rows: list[dict[str, Any]],
) -> None:
    tot_h = sum(r["hop_nguoi"] for r in frame_rows)
    tot_m = sum(r["hop_may"] for r in frame_rows)
    tot_tp = sum(r["khop_IoU0.5"] for r in frame_rows)
    tot_exact = sum(r["dung_nhan"] for r in frame_rows)
    tot_fp = sum(r["may_thua"] for r in frame_rows)
    tot_fn = sum(r["may_bo_sot"] for r in frame_rows)
    tot_sec = sum(r["giay"] for r in frame_rows)
    rec, prec, f1 = _prf(tot_tp, tot_fp, tot_fn)

    lines = [
        f"# All-BBox Pipeline Report — Job {job_id}",
        "",
        "## Summary",
        f"- Frames evaluated: {len(frame_rows)}",
        f"- Human boxes: {tot_h} | Machine boxes: {tot_m}",
        f"- Matched (IoU>=0.5): {tot_tp} (exact label: {tot_exact})",
        f"- Extra (red): {tot_fp} | Missed (yellow): {tot_fn}",
        f"- **Recall**: {rec:.1%} | **Precision**: {prec:.1%} | **F1**: {f1:.1%}",
        f"- Total inference time: {tot_sec:.2f}s",
        "",
        "## Per-Frame Metrics",
        "| Frame | Day/Night | Human | Machine | Matched | Exact Label | Extra | Missed | Recall | Precision | F1 | Time (s) |",
        "| ---: | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in frame_rows:
        lines.append(
            f"| {r['frame']} | {r['sang_toi']} | {r['hop_nguoi']} | {r['hop_may']} | "
            f"{r['khop_IoU0.5']} | {r['dung_nhan']} | {r['may_thua']} | {r['may_bo_sot']} | "
            f"{r['recall']:.1%} | {r['precision']:.1%} | {r['f1']:.1%} | {r['giay']:.2f} |"
        )

    lines.extend(
        [
            "",
            "## Per-Label Metrics",
            "| Label | Human | Machine | Matched | Recall | Precision | F1 |",
            "| :--- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for lr in label_rows:
        lines.append(
            f"| {lr['label']} | {lr['human']} | {lr['machine']} | {lr['matched']} | "
            f"{lr['recall']:.1%} | {lr['precision']:.1%} | {lr['f1']:.1%} |"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def push_to_cvat(cv: Any, job_id: int, draft_shapes: list[dict[str, Any]]) -> dict[str, Any]:
    """Push filtered new shapes to CVAT with backup, source='manual', and run log."""
    if not getattr(cv, "write_enabled", False):
        raise WriteNotAuthorized("Push requires Cvat(..., write_enabled=True).")
    if not draft_shapes:
        return {"pushed": 0, "backup": None, "run_log": None, "verified": True}

    # Ensure every pushed shape has source='manual'
    payload = [{**s, "source": "manual"} for s in draft_shapes]
    before, backup_path = tx.backup_annotations(cv, job_id, "bbox_all")
    before_ids = {s["id"] for s in before.get("shapes", [])}

    cv.create_shapes(job_id, payload)
    after = cv.annotations(job_id).get("shapes", [])
    created_ids = [s["id"] for s in after if s["id"] not in before_ids]
    verified = len(after) == len(before_ids) + len(payload)

    run_log = tx.write_run_log(
        job_id,
        {
            "kind": "shapes",
            "tool": "bbox_all_objects",
            "created_ids": created_ids,
            "backup": backup_path,
            "n_before": len(before_ids),
            "n_after": len(after),
            "verified": verified,
        },
    )
    return {
        "pushed": len(payload),
        "created_ids": created_ids,
        "backup": backup_path,
        "run_log": run_log,
        "verified": verified,
    }


def _extract_variant_image(variant: Any) -> np.ndarray:
    """Support either np.ndarray or (name, np.ndarray) from get_detection_variants."""
    if isinstance(variant, tuple) and len(variant) >= 2:
        for item in variant:
            if isinstance(item, np.ndarray):
                return item
    return variant


def run_pipeline(args: argparse.Namespace) -> dict[str, Any]:
    """Execute the unified all-object bbox pipeline."""
    from cvat_tools.detection.all_objects import detect_objects_multiscale, load_detector
    from cvat_tools.detection.night_enhance import get_detection_variants, is_night_frame
    from cvat_tools.detection.signs_lights import detect_signs_and_lights
    from cvat_tools.learning.convention_engine import (
        ALL_OBJECT_LABELS,
        apply_conventions,
        dedupe_against_human,
    )
    from cvat_tools.learning.cvat_learner import (
        apply_profile_filter,
        learn_from_cvat_shapes,
        load_profile,
        save_profile,
    )

    dry_run = not getattr(args, "push", False)
    cv = Cvat.from_env(profile=args.cvat_profile, write_enabled=not dry_run)

    job_labels = cv.labels(args.job)
    id_to_name = {lbl["id"]: lbl["name"] for lbl in job_labels}
    name_to_id = {lbl["name"]: lbl["id"] for lbl in job_labels}

    annotations = cv.annotations(args.job)
    all_shapes = annotations.get("shapes", [])

    # Learn or load profile
    profile_path = paths.DATA / "jobs" / str(args.job) / "learned_profile.json"
    profile = None
    if args.learn:
        profile = learn_from_cvat_shapes(all_shapes, id_to_name)
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        save_profile(profile, profile_path)
    elif profile_path.exists():
        profile = load_profile(profile_path)

    # Index human rectangle annotations by frame
    allowed_labels = set(ALL_OBJECT_LABELS) if ALL_OBJECT_LABELS else set(name_to_id.keys())
    human_by_frame: dict[int, list[tuple[str, list[float]]]] = {}
    human_shapes_by_frame: dict[int, list[dict[str, Any]]] = {}
    for s in all_shapes:
        if s.get("type") != "rectangle":
            continue
        lname = id_to_name.get(s.get("label_id"), "")
        if lname not in allowed_labels:
            continue
        frame_id = int(s["frame"])
        human_by_frame.setdefault(frame_id, []).append((lname, list(s["points"])))
        human_shapes_by_frame.setdefault(frame_id, []).append({**s, "label": lname})

    detector = load_detector(backend=args.backend, model_name=getattr(args, "model", "yolo26s"))
    frames = parse_frames(args.frames)

    out_dir = paths.DATA / "jobs" / str(args.job) / "previews" / "all_bbox"
    drafts_dir = out_dir / "drafts"
    out_dir.mkdir(parents=True, exist_ok=True)
    drafts_dir.mkdir(parents=True, exist_ok=True)

    frame_rows: list[dict[str, Any]] = []
    thumbs: list[np.ndarray] = []
    draft_shapes: list[dict[str, Any]] = []

    per_label_human: dict[str, int] = {}
    per_label_machine: dict[str, int] = {}
    per_label_matched: dict[str, int] = {}

    for f in frames:
        img = load_frame_image(cv, args.job, f)
        night_res = is_night_frame(img)
        night = bool(night_res[0]) if isinstance(night_res, tuple) else bool(night_res)
        t0 = time.perf_counter()

        variants = get_detection_variants(img)
        raw_dets: list[Detection] = []
        for var in variants:
            v_img = _extract_variant_image(var)
            raw_dets.extend(detect_objects_multiscale(v_img, detector, is_night=night))
        sl_img = _extract_variant_image(variants[1]) if (night and len(variants) > 1) else img
        shared_yolo = detector.load()._model if getattr(detector, "backend", None) == "pytorch" else None
        raw_dets.extend(
            detect_signs_and_lights(
                sl_img, is_night=night, yolo_model=shared_yolo
            )
        )

        merged_dets = nms_detections(raw_dets)
        conv_dets = apply_conventions(merged_dets)
        filtered_dets = (
            apply_profile_filter(conv_dets, profile, is_night=night)
            if profile is not None
            else conv_dets
        )
        elapsed_s = time.perf_counter() - t0

        hum = human_by_frame.get(f, [])
        matched, extra, missed = match_detections(
            filtered_dets, hum, iou_thresh=args.iou_thresh
        )

        # Accumulate per-label stats
        for h_label, _ in hum:
            per_label_human[h_label] = per_label_human.get(h_label, 0) + 1
        for det in filtered_dets:
            per_label_machine[det.label] = per_label_machine.get(det.label, 0) + 1
        for det, h_label in matched:
            if det.label == h_label:
                per_label_matched[h_label] = per_label_matched.get(h_label, 0) + 1

        # Preview image + thumbnail
        vis = draw_frame_preview(img, f, night, matched, extra, missed, len(hum), elapsed_s)
        cv2.imwrite(str(out_dir / f"f{f}_all.jpg"), vis)
        thumbs.append(cv2.resize(vis, (640, 360)))

        # Frame metrics
        tp = len(matched)
        fp = len(extra)
        fn = len(missed)
        rec, prec, f1 = _prf(tp, fp, fn)
        exact_label = sum(1 for det, hl in matched if det.label == hl)
        frame_rows.append(
            {
                "frame": f,
                "sang_toi": "toi" if night else "sang",
                "hop_nguoi": len(hum),
                "hop_may": len(filtered_dets),
                "khop_IoU0.5": tp,
                "dung_nhan": exact_label,
                "may_thua": fp,
                "may_bo_sot": fn,
                "recall": round(rec, 4),
                "precision": round(prec, 4),
                "f1": round(f1, 4),
                "giay": round(elapsed_s, 3),
            }
        )

        # Dedupe against human annotations for draft & optional push
        new_dets = dedupe_against_human(filtered_dets, human_shapes_by_frame.get(f, []))
        for det in new_dets:
            lid = name_to_id.get(det.label)
            if lid is not None:
                draft_shapes.append(det.to_cvat_shape(frame=f, label_id=lid))

    # Build per-label rows
    all_seen_labels = sorted(
        set(per_label_human.keys()) | set(per_label_machine.keys())
    )
    label_rows: list[dict[str, Any]] = []
    for lbl in all_seen_labels:
        h_cnt = per_label_human.get(lbl, 0)
        m_cnt = per_label_machine.get(lbl, 0)
        tp_cnt = per_label_matched.get(lbl, 0)
        rec, prec, f1 = _prf(tp_cnt, m_cnt - tp_cnt, h_cnt - tp_cnt)
        label_rows.append(
            {
                "label": lbl,
                "human": h_cnt,
                "machine": m_cnt,
                "matched": tp_cnt,
                "recall": round(rec, 4),
                "precision": round(prec, 4),
                "f1": round(f1, 4),
            }
        )

    # Save contact sheet, reports, and draft JSON
    contact_sheet_path = out_dir / "all_bbox_contact_sheet.jpg"
    cv2.imwrite(str(contact_sheet_path), build_contact_sheet(thumbs, cols=4))

    csv_path = out_dir / "all_bbox_report.csv"
    md_path = out_dir / "all_bbox_report.md"
    write_csv_report(csv_path, frame_rows)
    write_md_report(md_path, args.job, frame_rows, label_rows)

    draft_path = drafts_dir / f"all_bbox_draft_job{args.job}.json"
    draft_payload = {
        "job": args.job,
        "frames": frames,
        "backend": args.backend,
        "dry_run": dry_run,
        "count": len(draft_shapes),
        "shapes": draft_shapes,
    }
    draft_path.write_text(
        json.dumps(draft_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    push_result = None
    if not dry_run:
        push_result = push_to_cvat(cv, args.job, draft_shapes)

    return {
        "job": args.job,
        "frames": frames,
        "dry_run": dry_run,
        "out_dir": str(out_dir),
        "contact_sheet": str(contact_sheet_path),
        "csv_report": str(csv_path),
        "md_report": str(md_path),
        "draft_path": str(draft_path),
        "draft_count": len(draft_shapes),
        "frame_rows": frame_rows,
        "label_rows": label_rows,
        "push_result": push_result,
    }


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Unified all-object CVAT bbox pipeline.")
    ap.add_argument("--job", type=int, default=285, help="CVAT job ID (default: 285)")
    ap.add_argument("--frames", default="60-79", help="Frame range, e.g. 60-79")
    ap.add_argument(
        "--learn",
        action="store_true",
        help="Learn/update data/jobs/<job>/learned_profile.json from CVAT human annotations",
    )
    ap.add_argument(
        "--backend",
        choices=["auto", "openvino", "pytorch"],
        default="auto",
        help="Detector backend (default: auto)",
    )
    ap.add_argument(
        "--model",
        choices=["yolo26s", "yolo26l", "yolo26n"],
        default="yolo26s",
        help="YOLO model size (default: yolo26s for fast CPU OpenVINO)",
    )
    ap.add_argument(
        "--cvat-profile",
        default="local",
        help="CVAT connection profile name in config/cvat.<profile>.yaml",
    )
    ap.add_argument(
        "--iou-thresh",
        type=float,
        default=0.5,
        help="IoU threshold for matching machine vs human boxes",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Do not write to CVAT (default: True)",
    )
    ap.add_argument(
        "--push",
        action="store_true",
        help="Explicitly push deduped new boxes to CVAT with backup + source='manual'",
    )
    return ap


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args(argv)
    result = run_pipeline(args)
    print(
        f"Job {result['job']} | frames={len(result['frames'])} | "
        f"dry_run={result['dry_run']} | draft_boxes={result['draft_count']}"
    )
    print(f"Outputs: {result['out_dir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
