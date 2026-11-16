"""Do cong bang cac model phan vung nen tren frame job 285 co GT tay, TACH sang/dem, chon to hop theo label.

  python cvat/scripts/seg_model_bench.py --models b2,b5,m2f,lane          # chay tuan tu, tung model mot
  python cvat/scripts/seg_model_bench.py --models b5@1536 --out x.json     # bien the do phan giai

Chi doc file local (khong goi CVAT): tools/cvat-seg-copilot/frames/j285_ann.json + j285_f<N>.jpg.
GT = polygon trong j285_ann.json, chia 2 muc:
  human : polygon KHONG trung diem-diem voi bat ky nhap cua tool (cvat/week01/job285-bbox/drafts/*.json) -> do nguoi ve
          tay (road 20/20 frame, vai building/sky, lane/crosswalk). DAY LA GT sach.
  draft : polygon nguoi dung da chap nhan tu nhap B2 (sidewalk, pole, vegetation, building, sky...) -> thien vi ve B2,
          chi tham khao, KHONG dung de ket luan model nao thang B2.
Sang/dem theo mau cua du an: do sang TB >= 80 -> sang (61,63,69,70,71,73,77 = 7 frame), con lai dem (13 frame).
Job 987: bo qua (khong co mask tay cache offline day du; khong goi CVAT).
"""
from __future__ import annotations

import argparse
import glob
import json
import statistics
import sys
import threading
import time
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np
import psutil

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "cvat" / "src"))
from cvat_tools.segmentation import evidence as E  # noqa: E402

FRAMES = REPO / "tools" / "cvat-seg-copilot" / "frames"
DRAFTS = REPO / "cvat" / "week01" / "job285-bbox" / "drafts"
OUT_DIR = REPO / "cvat" / "data" / "benchmarks"
BRIGHT_MEAN = 80.0
GT_LABEL = {**{n: n for n in E.STUFF}, "lane/crosswalk": E.LANE_LABEL, "lane/single white": E.LANE_LABEL}


def _key(frame: int, pts) -> tuple:
    return frame, tuple(round(float(p), 1) for p in pts)


def tool_draft_keys() -> set:
    keys = set()
    for f in glob.glob(str(DRAFTS / "*.json")):
        d = json.load(open(f, encoding="utf8"))
        for s in d.get("shapes", []) if isinstance(d, dict) else []:
            if s.get("type") == "polygon":
                keys.add(_key(s["frame"], s["points"]))
    return keys


def load_gt(ann_path: Path, draft_keys: set, size) -> dict:
    """{(frame, label): {'human': bool mask|None, 'draft': bool mask|None}} (label da gop lane -> lane_paint)."""
    W, H = size
    gt: dict = {}
    for a in json.load(open(ann_path, encoding="utf8")):
        if a["type"] != "polygon" or a["label"] not in GT_LABEL:
            continue
        lab = GT_LABEL[a["label"]]
        kind = "draft" if _key(a["frame"], a["points"]) in draft_keys else "human"
        m = gt.setdefault((a["frame"], lab), {"human": np.zeros((H, W), np.uint8), "draft": np.zeros((H, W), np.uint8)})
        cv2.fillPoly(m[kind], [np.round(np.array(a["points"], np.float32).reshape(-1, 2)).astype(np.int32)], 1)
    return gt


class PeakRSS:
    def __init__(self):
        self.p, self.peak, self._stop = psutil.Process(), 0, threading.Event()

    def __enter__(self):
        def run():
            while not self._stop.is_set():
                self.peak = max(self.peak, self.p.memory_info().rss)
                time.sleep(0.02)

        self.t = threading.Thread(target=run, daemon=True)
        self.t.start()
        return self

    def __exit__(self, *a):
        self._stop.set()
        self.t.join()


def iou_recall(pred: np.ndarray, ref: np.ndarray):
    p, r = pred > 0, ref > 0
    u = int((p | r).sum())
    inter = int((p & r).sum())
    return (inter / u if u else 0.0), (inter / int(r.sum()) if r.any() else 0.0)


def run_model(spec: str, imgs: dict, gt: dict, labels) -> dict:
    t0 = time.time()
    with PeakRSS() as mem:
        E.load_model(spec)
        load_s = time.time() - t0
        rec, times = [], []
        for f, img in imgs.items():
            t = time.time()
            ev = E.model_evidence(spec, img, labels)
            times.append(time.time() - t)
            for lab, pred in ev.items():
                g = gt.get((f, lab))
                if not g:
                    continue
                for kind in ("human", "draft"):
                    if g[kind].any():
                        i, r = iou_recall(pred, g[kind])
                        rec.append({"frame": f, "label": lab, "kind": kind, "iou": i, "recall": r})
    E.free_model(spec)
    return {"load_s": round(load_s, 1), "s_per_frame_mean": round(statistics.mean(times), 2),
            "s_per_frame_median": round(statistics.median(times), 2), "peak_rss_mb": round(mem.peak / 2**20),
            "records": rec}


def aggregate(res: dict, bright: set) -> dict:
    """{kind: {label: {model: {'night': (mean, n), 'bright': (mean, n)}}}}"""
    agg: dict = {}
    for spec, r in res.items():
        by = defaultdict(list)
        for x in r["records"]:
            by[(x["kind"], x["label"], "bright" if x["frame"] in bright else "night")].append(x)
        for (kind, lab, grp), xs in by.items():
            agg.setdefault(kind, {}).setdefault(lab, {}).setdefault(spec, {})[grp] = {
                "iou": round(float(np.mean([x["iou"] for x in xs])), 3),
                "recall": round(float(np.mean([x["recall"] for x in xs])), 3), "n": len(xs)}
    return agg


def best_per_label(agg: dict, kind: str = "human") -> dict:
    """Model tot nhat theo (label, nhom) tren GT `kind`; lane_paint xep theo recall (GT lane chi danh dau mot phan)."""
    out = {}
    for lab, per_model in agg.get(kind, {}).items():
        metric = "recall" if lab == E.LANE_LABEL else "iou"
        for grp in ("night", "bright"):
            cand = {m: g[grp][metric] for m, g in per_model.items() if grp in g}
            if cand:
                m = max(cand, key=cand.get)
                out[f"{lab}/{grp}"] = {"best": m, metric: cand[m], "b2": cand.get("b2"), "n": per_model[m][grp]["n"]}
    return out


def print_tables(res: dict, agg: dict) -> None:
    models = list(res)
    for kind, title in (("human", "GT TAY SACH (nguoi ve)"), ("draft", "GT DA CHAP NHAN TU NHAP B2 (thien vi B2, chi tham khao)")):
        print(f"\n== IoU theo label x model, {title}  [moi o: dem / sang, (n frame)] ==")
        print("label".ljust(14) + "".join(m.ljust(24) for m in models))
        for lab, per_model in sorted(agg.get(kind, {}).items()):
            row = lab.ljust(14)
            for m in models:
                g = per_model.get(m, {})
                metric = "recall" if lab == E.LANE_LABEL else "iou"
                cell = " / ".join(f"{g[k][metric]:.2f}({g[k]['n']})" if k in g else "  -  " for k in ("night", "bright"))
                row += cell.ljust(24)
            print(row + ("   [lane_paint: recall]" if lab == E.LANE_LABEL else ""))
    print("\n== toc do / RAM ==")
    for m, r in res.items():
        print(f"{m.ljust(10)} {r['s_per_frame_mean']:6.2f} s/frame (median {r['s_per_frame_median']}), load {r['load_s']}s, peak RSS {r['peak_rss_mb']} MB")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="b2,b5,m2f,lane", help="tuan tu; 'b5@1536' = bien the do phan giai")
    ap.add_argument("--frames", default="", help="vd 60-69 hoac 61,63 (mac dinh 60-79)")
    ap.add_argument("--out", default=str(OUT_DIR / "seg_model_bench_job285.json"))
    ap.add_argument("--worker", default="", help="noi bo: chay 1 model trong tien trinh rieng (RAM do sach)")
    a = ap.parse_args()
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    fr = list(range(60, 80))
    if a.frames:
        fr = [int(y) for x in a.frames.split(",") for y in (range(int(x.split("-")[0]), int(x.split("-")[1]) + 1) if "-" in x else [x])]
    imgs = {f: cv2.imread(str(FRAMES / f"j285_f{f}.jpg")) for f in fr}
    H, W = next(iter(imgs.values())).shape[:2]
    bright = {f for f, im in imgs.items() if cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).mean() >= BRIGHT_MEAN}
    gt = load_gt(FRAMES / "j285_ann.json", tool_draft_keys(), (W, H))
    gt = {k: v for k, v in gt.items() if k[0] in imgs}
    print(f"{len(imgs)} frame, sang={sorted(bright)}, GT (frame,label): "
          f"human={sum(v['human'].any() for v in gt.values())}, draft={sum(v['draft'].any() for v in gt.values())}", flush=True)
    if a.worker:
        Path(a.out).write_text(json.dumps(run_model(a.worker, imgs, gt, E.ALL_LABELS)), encoding="utf8")
        return 0
    import subprocess
    import tempfile

    res = {}
    for spec in a.models.split(","):  # TUAN TU, moi model 1 tien trinh rieng -> RSS/thoi gian khong nhieu nhau
        print(f"... {spec}", flush=True)
        tmp = Path(tempfile.gettempdir()) / f"segbench_{spec.replace('@', '_')}.json"
        subprocess.run([sys.executable, __file__, "--worker", spec, "--frames", a.frames, "--out", str(tmp)], check=True,
                       stderr=subprocess.DEVNULL)
        res[spec] = json.loads(tmp.read_text(encoding="utf8"))
        print(f"    {res[spec]['s_per_frame_mean']} s/frame, {res[spec]['peak_rss_mb']} MB", flush=True)
    agg = aggregate(res, bright)
    print_tables(res, agg)
    best = {k: best_per_label(agg, k) for k in ("human", "draft")}
    print("\n== to hop tot nhat theo label (GT tay sach) ==")
    for k, v in best["human"].items():
        print(f"{k.ljust(20)} -> {v['best']} ({list(v.items())[1][0]}={list(v.items())[1][1]}, b2={v['b2']}, n={v['n']})")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps({"bright_frames": sorted(bright), "models": {m: {k: v for k, v in r.items() if k != "records"} for m, r in res.items()},
                                       "agg": agg, "best": best, "records": {m: r["records"] for m, r in res.items()}},
                                      ensure_ascii=False, indent=1), encoding="utf8")
    print(f"\nluu {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
