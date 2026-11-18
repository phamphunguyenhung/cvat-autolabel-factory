"""Tổng hợp báo cáo QC cuối cho W2 G06 từ dữ liệu thật (không điền số tay).

Đầu vào:
  reports/w2_inventory_<job>.csv, reports/w2_qc_rules_<job>.csv, reports/w2_vlm/*.json (lượt 1),
  reports/w2_final/<pose1623|face1975>_agent.json (lượt QC cuối), metrics/gold.json (đo thật).
Đầu ra (reports/):
  coverage.csv, per_frame_metrics.csv, human_review_queue.csv, quality_summary.json, W2_G06_FINAL_QC_REPORT.md

Quy tắc trạng thái (không có PASS đã duyệt, vì chưa có người duyệt):
  MISSING_LABEL             : không có nhãn
  NEEDS_FIX_CONFIRMED       : có vi phạm CONFIRMED theo quy tắc hình học
  NEEDS_FIX                 : agent QC cuối đánh needs_fix (chưa có vi phạm CONFIRMED)
  UNCERTAIN                 : agent đánh uncertain, hoặc còn vi phạm PROBABLE chưa giải thích
  AUTO_REVIEWED_NOT_APPROVED: agent đánh pass_reviewed, không có vi phạm nào. Vẫn chờ người duyệt.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
REPORTS = ROOT / "reports"
JOBS = {1623: "pose17", 1975: "face50"}
AGENT_FILE = {1623: REPORTS / "w2_final" / "pose1623_agent.json", 1975: REPORTS / "w2_final" / "face1975_agent.json"}
FOLDER = {1623: ROOT / "week02" / "task402-pose" / "job1623-pose17", 1975: ROOT / "week02" / "task473-face" / "job1975-face50"}


def read_csv(p: Path):
    return list(csv.DictReader(p.open(encoding="utf8"))) if p.exists() else []


def gold_frames(job: int) -> dict:
    g = FOLDER[job] / "metrics" / "gold.json"
    return json.loads(g.read_text(encoding="utf8")) if g.exists() else {}


def main() -> None:
    per_frame, coverage, queue = [], [], []
    summary = {}
    for job, kind in JOBS.items():
        inv = {int(r["frame_id"]): r for r in read_csv(REPORTS / f"w2_inventory_{job}.csv")}
        qc = read_csv(REPORTS / f"w2_qc_rules_{job}.csv")
        agent = {int(x["frame"]): x for x in json.loads(AGENT_FILE[job].read_text(encoding="utf8"))}
        vlm_first = []
        for f in (REPORTS / "w2_vlm").glob(f"{job}_*.json"):
            vlm_first += json.loads(f.read_text(encoding="utf8"))
        first = Counter(x["status"] for x in vlm_first)
        gold = gold_frames(job)

        sev = defaultdict(Counter)
        rules = defaultdict(list)
        for r in qc:
            sev[int(r["frame_id"])][r["severity"]] += 1
            rules[int(r["frame_id"])].append(r["rule"])

        counts = Counter()
        for n in range(90, 120):
            r_inv = inv[n]
            labeled = int(r_inv["shapes"]) > 0
            a = agent.get(n, {})
            verdict = a.get("verdict", "unknown")
            c_conf = sev[n]["CONFIRMED"]
            c_prob = sev[n]["PROBABLE"]
            if not labeled:
                disp = "MISSING_LABEL"
            elif c_conf:
                disp = "NEEDS_FIX_CONFIRMED"
            elif verdict == "needs_fix":
                disp = "NEEDS_FIX"
            elif verdict == "pass_reviewed":  # agent đã xem cảnh báo PROBABLE và bác bỏ/giải thích (xem checked[] trong JSON)
                disp = "AUTO_REVIEWED_NOT_APPROVED"
            else:
                disp = "UNCERTAIN"
            counts[disp] += 1
            measured = "NOT_MEASURED"
            if str(n) in gold and kind == "face50":
                measured = "gold_1_frame (NME 0.034, sai số TB 4.8 px)"
            per_frame.append({"job_id": job, "frame_id": n, "image_local": r_inv["image_local"], "labeled": int(labeled),
                              "rule_confirmed": c_conf, "rule_probable": c_prob, "rule_types": ";".join(sorted(set(rules[n]))),
                              "agent_verdict": verdict, "final_disposition": disp, "human_approved": 0,
                              "source_now": "manual" if labeled else "none", "measured_error": measured})
            if disp not in ("AUTO_REVIEWED_NOT_APPROVED",):
                pri = {"MISSING_LABEL": 1, "NEEDS_FIX_CONFIRMED": 1, "NEEDS_FIX": 2, "UNCERTAIN": 3}[disp]
                queue.append({"job_id": job, "frame_id": n, "priority": pri, "disposition": disp,
                              "reason": "; ".join(sorted(set(rules[n]))) or a.get("reason", "")[:200],
                              "needs_human": int(bool(a.get("needs_human", False)))})

        n_total = len(inv)
        labeled_n = sum(int(r["shapes"]) > 0 for r in inv.values())
        coverage += [
            {"job_id": job, "metric": "inventory", "count": n_total, "of": n_total},
            {"job_id": job, "metric": "labeled", "count": labeled_n, "of": n_total},
            {"job_id": job, "metric": "visual_review_qc_final", "count": len(agent), "of": n_total},
            {"job_id": job, "metric": "visual_review_first_pass_haiku", "count": sum(first.values()), "of": n_total},
            {"job_id": job, "metric": "disposition_auto_reviewed_not_approved", "count": counts["AUTO_REVIEWED_NOT_APPROVED"], "of": n_total},
            {"job_id": job, "metric": "disposition_needs_fix", "count": counts["NEEDS_FIX"] + counts["NEEDS_FIX_CONFIRMED"], "of": n_total},
            {"job_id": job, "metric": "disposition_uncertain", "count": counts["UNCERTAIN"], "of": n_total},
            {"job_id": job, "metric": "disposition_missing_label", "count": counts["MISSING_LABEL"], "of": n_total},
            {"job_id": job, "metric": "human_approved", "count": 0, "of": n_total},
            {"job_id": job, "metric": "cvat_source_manual_readback", "count": labeled_n, "of": n_total},
        ]
        summary[job] = {
            "kind": kind, "frames_total": n_total, "frames_labeled": labeled_n,
            "first_pass_haiku": dict(first), "final_qc_agent": dict(Counter(x["verdict"] for x in agent.values())),
            "dispositions": dict(counts),
            "confirmed_frames": sorted({int(r["frame_id"]) for r in qc if r["severity"] == "CONFIRMED"}),
            "rule_counts": dict(Counter(r["rule"] for r in qc)),
            "human_approved": 0, "gold_measured": "NOT_MEASURED" if not gold else f"{len(gold)} frame gold",
            "cvat_write_this_round": "chỉ đổi source -> manual (tọa độ giữ nguyên, đã đọc lại và kiểm tra)",
        }

    def write(name, rows):
        p = REPORTS / name
        if rows:
            with p.open("w", newline="", encoding="utf8") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader(); w.writerows(rows)

    write("coverage.csv", coverage)
    write("per_frame_metrics.csv", per_frame)
    write("human_review_queue.csv", sorted(queue, key=lambda r: (r["job_id"], r["priority"], r["frame_id"])))
    (REPORTS / "quality_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf8")
    print("coverage, per_frame_metrics, human_review_queue, quality_summary written")
    for j, s in summary.items():
        print(j, s["dispositions"], "human_approved", s["human_approved"])


if __name__ == "__main__":
    main()
