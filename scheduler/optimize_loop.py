"""Local optimization scheduler & checkpointed evaluator for CVAT Tools."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cvat_tools.quality.metrics_eval import evaluate_split  # noqa: E402

LOCK_FILE = ROOT / "scheduler" / "loop.lock"
STATE_FILE = ROOT / "scheduler" / "state.json"
REPORTS_DIR = ROOT / "reports"
ITER_DIR = REPORTS_DIR / "iterations"
CKPT_DIR = ROOT / "checkpoints"

GOALS = {
    "bbox_map50": 0.90,
    "macro_miou": 0.85,
    "area_direct_iou": 0.90,
    "building_fp_area_rate_max": 0.02,
    "invalid_geometry_max": 0,
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_state() -> dict[str, Any]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"status": "idle", "iteration": 0, "non_improving": 0, "best_score": -1.0, "started_at": _now()}


def _save_state(st: dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")


def _rss_mb() -> float:
    return round(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024), 1)


def _flatten_export(export_path: Path) -> list[dict[str, Any]]:
    data = json.loads(export_path.read_text(encoding="utf-8"))
    items: list[dict[str, Any]] = []
    for f_str, arr in data.get("frames", {}).items():
        for x in arr:
            items.append({"frame": int(f_str), **x})
    return items


def run_tick(*, run_pytest: bool = True) -> dict[str, Any]:
    st = _load_state()
    if st.get("status") in ("paused", "stopped"):
        return {"skipped": True, "reason": f"state={st['status']}"}
    if LOCK_FILE.exists():
        return {"skipped": True, "reason": "lock_active"}

    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCK_FILE.write_text(json.dumps({"pid": os.getpid(), "at": _now()}), encoding="utf-8")
    t0 = time.perf_counter()
    try:
        gt_path = ROOT.parent / "tools" / "cvat-seg-copilot" / "frames" / "j285_ann.json"
        pred_path = ROOT / "week01" / "job285-bbox" / "previews_full_bbox" / "full_bbox_job285.json"
        if not gt_path.exists() or not pred_path.exists():
            st["status"] = "STOP_LIMIT"
            _save_state(st)
            return {"stop": "STOP_LIMIT", "reason": "missing_gt_or_pred"}

        gt = json.loads(gt_path.read_text(encoding="utf-8"))
        preds = _flatten_export(pred_path)
        dev = evaluate_split(gt, preds, list(range(60, 70)))
        evl = evaluate_split(gt, preds, list(range(70, 80)))

        reg_ok = True
        reg_summary = "skipped"
        if run_pytest:
            p = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=str(ROOT), capture_output=True, text=True)
            reg_ok = p.returncode == 0
            reg_summary = (p.stdout or "").strip().splitlines()[-1] if p.stdout else f"rc={p.returncode}"

        score = round(float(evl.get("macro_miou") or 0.0) + float(evl.get("area_direct_iou") or 0.0), 4)
        it_id = int(st["iteration"]) + 1
        improved = score > float(st.get("best_score", -1.0))
        st["iteration"] = it_id
        st["non_improving"] = 0 if improved else int(st.get("non_improving", 0)) + 1
        if improved:
            st["best_score"] = score

        goals_met = (
            evl["macro_miou"] >= GOALS["macro_miou"]
            and (evl["area_direct_iou"] or 0.0) >= GOALS["area_direct_iou"]
            and evl["building_fp_area_rate"] <= GOALS["building_fp_area_rate_max"]
            and evl["invalid_geometry"] <= GOALS["invalid_geometry_max"]
            and reg_ok
        )
        stop_reason = None
        if goals_met:
            stop_reason = "STOP_SUCCESS"
        elif it_id >= 30 or st["non_improving"] >= 5 or _rss_mb() > 14000:
            stop_reason = "STOP_LIMIT"

        report = {
            "iteration_id": it_id,
            "timestamp": _now(),
            "hypothesis": "Baseline evaluation after building rectilinear cap + night union + f69 area/direct fix",
            "changed_module": "geomrefine.py, framegen.py, export_full_bbox_job285.py",
            "baseline": {"best_score": st.get("best_score")},
            "candidate": {"dev": dev, "eval": evl, "score": score},
            "delta": {"score_improved": improved},
            "regression_result": reg_summary,
            "runtime_s": round(time.perf_counter() - t0, 2),
            "peak_ram_mb": _rss_mb(),
            "decision": "keep" if (improved and reg_ok and evl["invalid_geometry"] == 0) else "gap_recorded",
            "next_action": stop_reason or "priority_1_building_fp_or_expand_gold_set",
        }
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        ITER_DIR.mkdir(parents=True, exist_ok=True)
        CKPT_DIR.mkdir(parents=True, exist_ok=True)

        if not (REPORTS_DIR / "baseline.json").exists():
            (REPORTS_DIR / "baseline.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        (ITER_DIR / f"iter_{it_id:03d}.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        if improved:
            (CKPT_DIR / "best.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

        gap_md = (
            f"# Final Gap Report (Iter {it_id})\n\n"
            f"- Status: **{stop_reason or 'STOP_LIMIT (goals not yet reached; draft + benchmark reproducible)'}**\n"
            f"- Dev (f60-69): `macro_miou={dev['macro_miou']}`, `area_direct_iou={dev['area_direct_iou']}`, `building_fp_area_rate={dev['building_fp_area_rate']}`, `invalid_geometry={dev['invalid_geometry']}`\n"
            f"- Held-out Eval (f70-79): `macro_miou={evl['macro_miou']}`, `area_direct_iou={evl['area_direct_iou']}`, `building_fp_area_rate={evl['building_fp_area_rate']}`, `invalid_geometry={evl['invalid_geometry']}`\n"
            f"- Regression: `{reg_summary}`\n"
            f"- Gaps vs Goals: `macro_miou` target `{GOALS['macro_miou']}`, `area_direct_iou` target `{GOALS['area_direct_iou']}`, `bbox_drafts` TP={evl['bbox_drafts']['tp']} FP={evl['bbox_drafts']['fp']}.\n"
        )
        (REPORTS_DIR / "final_gap_report.md").write_text(gap_md, encoding="utf-8")
        st["status"] = stop_reason or "idle"
        _save_state(st)
        return report
    finally:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()


def main() -> int:
    ap = argparse.ArgumentParser(description="Local CVAT Optimization Scheduler")
    ap.add_argument("--tick", action="store_true", help="Run 1 optimization/evaluation tick")
    ap.add_argument("--no-pytest", action="store_true", help="Skip pytest during quick tick")
    ap.add_argument("--daemon", action="store_true", help="Run persistent loop every --interval seconds")
    ap.add_argument("--interval", type=int, default=600, help="Seconds between ticks (default 600 = 10m)")
    ap.add_argument("--pause", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--stop", action="store_true")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()

    if a.pause:
        st = _load_state(); st["status"] = "paused"; _save_state(st); print(st); return 0
    if a.resume:
        st = _load_state(); st["status"] = "idle"; _save_state(st); print(st); return 0
    if a.stop:
        st = _load_state(); st["status"] = "stopped"; _save_state(st); print(st); return 0
    if a.status:
        print(json.dumps(_load_state(), indent=2, ensure_ascii=False)); return 0
    if a.tick:
        print(json.dumps(run_tick(run_pytest=not a.no_pytest), indent=2, ensure_ascii=False))
        return 0
    if a.daemon:
        while True:
            res = run_tick(run_pytest=not a.no_pytest)
            print(json.dumps({"tick": res.get("iteration_id"), "status": _load_state().get("status")}, ensure_ascii=False))
            if _load_state().get("status") in ("STOP_SUCCESS", "STOP_LIMIT", "stopped"):
                break
            time.sleep(a.interval)
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
