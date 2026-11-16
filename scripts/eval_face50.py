"""Đo độ lệch nháp mặt 50 điểm so với nhãn bạn đã SỬA TAY trên CVAT (gold). Chỉ đọc CVAT.

Gold = frame mà nhãn auto đã đẩy lên bị sửa nhiều (>= --min-moved điểm lệch > --tol px so với nháp lúc đẩy).
Gold lưu ở <job>/metrics/gold.json (giữ lại cho lần đo sau). NME = lệch TB / khoảng cách hai khóe mắt ngoài (14 và 26).

  python scripts/eval_face50.py --job 1975 --refresh-gold                      # cập nhật gold từ CVAT rồi đo nháp mới nhất
  python scripts/eval_face50.py --job 1975 --draft week02/.../drafts/face50_XXX.json
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cvat_tools.core.client import Cvat  # noqa: E402
from cvat_tools.pose import week2  # noqa: E402

GROUPS = week2.FACE_LABELS


def _draft_points(path: Path) -> dict:
    d = json.loads(path.read_text(encoding="utf8"))
    return {fr["frame"]: {n: (pt["x"], pt["y"]) for p in fr["people"] for n, pt in p["points"].items()} for fr in d["frames"]}


def _label_of(labels: list) -> dict:
    return {s["name"]: l["name"] for l in labels for s in l["sublabels"]}


def refresh_gold(c: Cvat, job: int, folder: Path, tol: float, min_moved: int) -> dict:
    runs = sorted((folder / "backups").glob("run_*.json"))
    if not runs:
        raise SystemExit("Chưa có run_*.json: chưa đẩy nháp nào lên CVAT nên chưa có gì để so.")
    run = json.loads(runs[-1].read_text(encoding="utf8"))
    pushed = _draft_points(folder / "drafts" / run["draft"])
    labels = c.labels(job)
    subn = {s["id"]: s["name"] for l in labels for s in l["sublabels"]}
    cur: dict = {}
    for s in c.annotations(job)["shapes"]:
        if s["id"] in set(run["created_ids"]):
            for e in s["elements"]:
                cur.setdefault(s["frame"], {})[subn[e["label_id"]]] = tuple(e["points"])
    gf = folder / "metrics" / "gold.json"
    gold = json.loads(gf.read_text(encoding="utf8")) if gf.exists() else {}
    for fr, pts in cur.items():
        moved = sum(1 for n, (x, y) in pts.items() if fr in pushed and math.hypot(x - pushed[fr][n][0], y - pushed[fr][n][1]) > tol)
        if moved >= min_moved:    # chỉ lưu điểm BẠN ĐÃ SỬA (điểm không đổi có thể chỉ là nháp cũ, không phải nhãn đã duyệt)
            gold[str(fr)] = {n: list(v) for n, v in pts.items()
                             if math.hypot(v[0] - pushed[fr][n][0], v[1] - pushed[fr][n][1]) > tol}
    gf.parent.mkdir(exist_ok=True)
    gf.write_text(json.dumps(gold, ensure_ascii=False), encoding="utf8")
    return gold


def evaluate(gold: dict, draft: dict, grp: dict) -> dict:
    rows, per = {}, {g: [] for g in GROUPS}
    nme = []
    for fr, pts in gold.items():
        fr = int(fr)
        if fr not in draft:
            continue
        iod = math.hypot(pts["14"][0] - pts["26"][0], pts["14"][1] - pts["26"][1]) if "14" in pts and "26" in pts else float("nan")
        errs = {n: math.hypot(pts[n][0] - draft[fr][n][0], pts[n][1] - draft[fr][n][1]) for n in pts if n in draft[fr]}
        for n, e in errs.items():
            per[grp[n]].append(e)
        nme.append(float(np.mean(list(errs.values()))) / iod)
        rows[fr] = {"mean_px": float(np.mean(list(errs.values()))), "nme": nme[-1], "iod": iod}
    return {"frames": rows, "group_px": {g: (float(np.mean(v)) if v else None) for g, v in per.items()},
            "nme_mean": float(np.mean(nme)) if nme else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", type=int, required=True); ap.add_argument("--profile", default="edufun")
    ap.add_argument("--draft", nargs="*", default=None, help="file nháp cần đo (mặc định: nháp đang đẩy + nháp mới nhất)")
    ap.add_argument("--refresh-gold", action="store_true"); ap.add_argument("--tol", type=float, default=1.5)
    ap.add_argument("--min-moved", type=int, default=30)
    a = ap.parse_args()
    c = Cvat.from_env(a.profile); folder = week2.job_folder(a.job)
    gold = refresh_gold(c, a.job, folder, a.tol, a.min_moved) if a.refresh_gold else json.loads((folder / "metrics" / "gold.json").read_text(encoding="utf8"))
    grp = _label_of(c.labels(a.job))
    files = [Path(f) for f in a.draft] if a.draft else sorted((folder / "drafts").glob("face50_*.json"))[-2:]
    print(f"gold: frame {sorted(map(int, gold))} ({len(gold)} frame)")
    for f in files:
        r = evaluate(gold, _draft_points(f), grp)
        print(f"\n== {f.name}")
        print("  lệch TB theo nhóm (px):", {g: (round(v, 1) if v is not None else None) for g, v in r["group_px"].items()})
        print("  theo frame:", {k: (round(v["mean_px"], 1), round(v["nme"], 3)) for k, v in r["frames"].items()}, "(px, NME)")
        print("  NME trung bình:", None if r["nme_mean"] is None else round(r["nme_mean"], 3))


if __name__ == "__main__":
    main()
