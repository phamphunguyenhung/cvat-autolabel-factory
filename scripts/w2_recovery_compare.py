"""Recovery W2: chuẩn hóa mọi phiên bản annotation (server backup, draft, live) về cùng dạng và so sánh theo frame.

Chỉ ĐỌC CVAT (write_enabled=False). Snapshot live lưu bất biến vào reports/w2_recovery/snapshots/.

  python -X utf8 scripts/w2_recovery_compare.py snapshot            # tải live 1623+1975
  python -X utf8 scripts/w2_recovery_compare.py compare --job 1975  # bảng so sánh các phiên bản
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(ROOT / "src"))
OUT = ROOT / "reports" / "w2_recovery"
SNAP = OUT / "snapshots"
JOBDIR = {
    1623: ROOT / "week02/task402-pose/job1623-pose17",
    1975: ROOT / "week02/task473-face/job1975-face50",
}


def labels(job: int) -> dict:
    d = json.loads((ROOT / f"data/jobs/edufun/{job}/labels.json").read_text(encoding="utf8"))
    return {l["id"]: l["name"] for l in d}, {s["id"]: s["name"] for l in d for s in l.get("sublabels", [])}


def norm_server(job: int, anno) -> dict:
    """server annotations -> {frame: {skel_label: {elem: [x,y,occ,out]}}} ; gồm source."""
    lab, sub = labels(job)
    shapes = anno["shapes"] if isinstance(anno, dict) else anno
    out: dict = {}
    for s in shapes:
        if s["type"] != "skeleton":
            continue
        sk = out.setdefault(s["frame"], {}).setdefault(lab.get(s["label_id"], str(s["label_id"])), {})
        sk["_source"] = s.get("source")
        for e in s.get("elements", []):
            p = e["points"]
            sk[sub.get(e["label_id"], str(e["label_id"]))] = [p[0], p[1], bool(e.get("occluded")), bool(e.get("outside"))]
    return out


def norm_draft(d: dict) -> dict:
    out: dict = {}
    for fr in d["frames"]:
        for p in fr.get("people", []):
            sk = out.setdefault(fr["frame"], {}).setdefault(p["label"], {})
            sk["_source"] = "draft"
            for k, v in p["points"].items():
                st = v.get("state", "visible")
                sk[str(k)] = [v["x"], v["y"], st == "occluded", st == "outside"]
    return out


def versions(job: int) -> dict:
    jd = JOBDIR[job]
    v = {}
    for p in sorted(glob.glob(str(jd / "backups" / "before_2*.json"))) + sorted(glob.glob(str(jd / "backups" / "before_manual_*.json"))):
        d = json.loads(Path(p).read_text(encoding="utf8"))
        v["srv:" + Path(p).stem] = norm_server(job, d)
    for p in sorted(glob.glob(str(jd / "drafts" / "*.json"))):
        d = json.loads(Path(p).read_text(encoding="utf8"))
        if isinstance(d, dict) and d.get("frames"):
            v["draft:" + Path(p).stem] = norm_draft(d)
    for p in sorted(glob.glob(str(OUT / "proposals" / f"prop_{job}_*.json"))):
        v["prop:" + Path(p).stem] = norm_draft(json.loads(Path(p).read_text(encoding="utf8")))
    for p in sorted(glob.glob(str(SNAP / f"live_{job}_*.json"))):
        v["live:" + Path(p).stem] = norm_server(job, json.loads(Path(p).read_text(encoding="utf8")))
    return v


def spread(sk: dict) -> float:
    """Độ trải của các điểm nhìn thấy (căn bậc hai diện tích bbox). Nhỏ = co cụm."""
    pts = [(v[0], v[1]) for k, v in sk.items() if k != "_source" and not v[3]]
    if len(pts) < 2:
        return 0.0
    xs, ys = zip(*pts)
    return math.sqrt(max(xs) - min(xs) + 1e-6) * math.sqrt(max(ys) - min(ys) + 1e-6)


def disp(a: dict, b: dict):
    ds = []
    for k, v in a.items():
        if k == "_source" or k not in b:
            continue
        ds.append(math.hypot(v[0] - b[k][0], v[1] - b[k][1]))
    return (sum(ds) / len(ds), max(ds), len(ds)) if ds else (0, 0, 0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["snapshot", "compare"])
    ap.add_argument("--job", type=int, action="append")
    a = ap.parse_args()
    jobs = a.job or [1623, 1975]
    if a.cmd == "snapshot":
        from cvat_tools.core.client import Cvat
        c = Cvat.from_env("edufun", write_enabled=False)
        SNAP.mkdir(parents=True, exist_ok=True)
        ts = time.strftime("%Y%m%d_%H%M%S")
        for j in jobs:
            an = c.annotations(j)
            p = SNAP / f"live_{j}_{ts}.json"
            p.write_text(json.dumps(an, ensure_ascii=False), encoding="utf8")
            print(j, "version", an.get("version"), "shapes", len(an["shapes"]), "->", p.name)
        return
    for j in jobs:
        V = versions(j)
        print(f"== job {j}: {list(V)}")
        for n, v in V.items():
            print(f"  {n}: frames={len(v)} sources={sorted({sk['_source'] for f in v.values() for sk in f.values()}, key=str)}")
        names = list(V)
        live = [n for n in names if n.startswith("live:")]
        if not live:
            continue
        L = V[live[-1]]
        print("frame | " + " | ".join(n[:22] for n in names if n != live[-1]) + "  (mean px lệch so với live / n skel)")
        for f in sorted(L):
            row = []
            for n in names:
                if n == live[-1]:
                    continue
                v = V[n].get(f)
                if not v:
                    row.append("   -  ")
                    continue
                ms = [disp(v[k], L[f][k])[0] for k in v if k in L[f]]
                row.append(f"{sum(ms)/len(ms):6.1f}" if ms else "  -  ")
            print(f"{f:5d} | " + " | ".join(row))


if __name__ == "__main__":
    main()
