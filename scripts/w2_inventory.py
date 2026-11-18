"""Inventory per-frame cho job tuần 2 (chỉ đọc CVAT). Ghi reports/w2_inventory_<job>.csv.

Mỗi dòng = một frame trong job_info.json: có ảnh local không, số shape, số điểm, nguồn (source),
số điểm occluded/outside, và frame có nằm trong backup run (nháp tool đã đẩy) không.

  python -X utf8 scripts/w2_inventory.py --job 1623 --job 1975
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cvat_tools.core.client import Cvat  # noqa: E402
from cvat_tools.pose import week2  # noqa: E402


def frame_numbers(job: int) -> list[int]:
    info = json.loads((ROOT / "data" / "jobs" / "edufun" / str(job) / "job_info.json").read_text(encoding="utf8"))
    start = info.get("start_frame", 0)
    return [start + i for i in range(len(info["names"]))]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", type=int, action="append", required=True)
    ap.add_argument("--profile", default="edufun")
    a = ap.parse_args()
    c = Cvat.from_env(a.profile)
    for job in a.job:
        folder = week2.job_folder(job)
        pushed_ids: set = set()
        for run in sorted((folder / "backups").glob("run_*.json")):
            pushed_ids |= set(json.loads(run.read_text(encoding="utf8")).get("created_ids", []))
        by_frame: dict[int, dict] = {}
        for s in c.annotations(job)["shapes"]:
            row = by_frame.setdefault(s["frame"], {"shapes": 0, "points": 0, "occluded": 0, "outside": 0, "sources": Counter(), "tool_ids": 0})
            row["shapes"] += 1
            row["sources"][s.get("source", "?")] += 1
            row["tool_ids"] += int(s["id"] in pushed_ids)
            for e in s.get("elements", []):
                row["points"] += len(e.get("points", [])) // 2
                row["occluded"] += int(bool(e.get("occluded")))
                row["outside"] += int(bool(e.get("outside")))
        out = ROOT / "reports" / f"w2_inventory_{job}.csv"
        out.parent.mkdir(exist_ok=True)
        local = ROOT / "data" / "jobs" / "edufun" / str(job) / "frames"
        gold_file = folder / "metrics" / "gold.json"
        gold = set(json.loads(gold_file.read_text(encoding="utf8")).keys()) if gold_file.exists() else set()
        with out.open("w", newline="", encoding="utf8") as f:
            w = csv.writer(f)
            w.writerow(["job_id", "frame_id", "image_local", "shapes", "points", "occluded", "outside", "sources", "tool_pushed_shapes", "final_status"])
            for fr in frame_numbers(job):
                r = by_frame.get(fr, {"shapes": 0, "points": 0, "occluded": 0, "outside": 0, "sources": Counter(), "tool_ids": 0})
                img = any(local.glob(f"*_{fr + 1:03d}.jpg")) if local.exists() else False
                src = ";".join(f"{k}:{v}" for k, v in sorted(r["sources"].items()))
                if not img and r["shapes"] == 0:
                    status = "Blocked: thiếu ảnh local và chưa có nhãn"
                elif r["shapes"] == 0:
                    status = "Not processed: chưa có nhãn, cần vẽ tay (policy)"
                elif str(fr) in gold:
                    status = "Human edited (gold): có so sánh đo được"
                elif r["tool_ids"] > 0:
                    status = "AI draft on CVAT: chưa VLM review, chưa human approve"
                else:
                    status = "Pre-label source=file: chưa kiểm, chưa human approve"
                w.writerow([job, fr, int(img), r["shapes"], r["points"], r["occluded"], r["outside"], src, r["tool_ids"], status])
        print(f"job {job}: {len(by_frame)} frame có shape -> {out}")


if __name__ == "__main__":
    main()
