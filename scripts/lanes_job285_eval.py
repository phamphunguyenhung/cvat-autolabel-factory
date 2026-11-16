"""Chay sinh nhap lane/area TUNG FRAME tren job 285 + do voi shape nguoi ve + so voi nhap cu. CHI DOC, khong ghi CVAT.

  python cvat/scripts/lanes_job285_eval.py [--frames 60-79]

Nguon: cache offline tools/cvat-seg-copilot/frames (j285_ann.json + anh) - CVAT local co the tat.
GT chi la polygon KHONG trung nhap cua tool (nguoi ve tay): road 20/20, area/direct 11 frame, crosswalk 5 shape.
Vach trang/vang/curb khong co GT: chi bao so vach/frame + overlay vao cvat/data/jobs/285/previews/lanes/.
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
import time
from collections import Counter
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cvat_tools.lanes.framegen import generate_frame  # noqa: E402

FRAMES = ROOT.parent / "tools" / "cvat-seg-copilot" / "frames"
DRAFTS = ROOT / "week01" / "job285-bbox" / "drafts"
OUT = ROOT / "data" / "jobs" / "285" / "previews" / "lanes"
COL = {"lane/single white": (255, 255, 255), "lane/double white": (255, 200, 200), "lane/single yellow": (0, 220, 255),
       "lane/double yellow": (0, 160, 255), "lane/crosswalk": (255, 255, 0), "area/direct": (255, 0, 255),
       "area/alternative": (0, 255, 0)}


def _key(f, p):
    return f, tuple(round(float(x), 1) for x in p)


def draft_keys():
    ks = set()
    for f in glob.glob(str(DRAFTS / "*.json")):
        d = json.load(open(f, encoding="utf8"))
        for s in d.get("shapes", []) if isinstance(d, dict) else []:
            ks.add(_key(s["frame"], s["points"]))
    return ks


def mask(p, W=1280, H=720):
    m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [np.round(np.float32(p)).astype(np.int32).reshape(-1, 2)], 1)
    return m


def iou(a, b):
    return float((a & b).sum() / max(1, (a | b).sum()))


def best_iou(gt_masks, preds):
    """IoU cua gop mask GT voi gop mask du doan (area), hoac khop tot nhat tung GT (crosswalk)."""
    return [max([iou(g, p) for p in preds] or [0.0]) for g in gt_masks]


def old_draft(frame, label):
    d = json.load(open(DRAFTS / "LATEST_lanearea.json", encoding="utf8"))
    out = [s["points"] for s in d["shapes"] if s["frame"] == frame and s.get("_label") == label]
    if frame == 61:
        d2 = json.load(open(DRAFTS / "LATEST_lanearea61.json", encoding="utf8"))
        out = [s["points"] for s in d2["shapes"] if s["frame"] == 61 and s.get("_label") == label]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", default="60-79")
    a = ap.parse_args()
    lo, hi = (int(x) for x in a.frames.split("-"))
    ann = json.load(open(FRAMES / "j285_ann.json", encoding="utf8"))
    dk = draft_keys()
    OUT.mkdir(parents=True, exist_ok=True)
    rows, res = [], {}
    for fr in range(lo, hi + 1):
        img = cv2.imread(str(FRAMES / f"j285_f{fr}.jpg"))
        H, W = img.shape[:2]
        roads = [x["points"] for x in ann if x["frame"] == fr and x["label"] == "road" and x["type"] == "polygon"]
        t0 = time.time()
        g = generate_frame(img, roads)
        dt = time.time() - t0
        sh = g["shapes"]
        human = lambda lab: [x["points"] for x in ann if x["frame"] == fr and x["label"] == lab and x["type"] == "polygon"
                             and _key(fr, x["points"]) not in dk]
        row = {"frame": fr, "dark": g["dark"], "s": round(dt, 2), "vp": [round(v) for v in g["vp"]] if g["vp"] else None,
               "vp_src": g["vp_src"], "lines": dict(Counter(s["label"].split("/")[1] for s in sh if s["label"].startswith("lane/") and "crosswalk" not in s["label"])),
               "n_cw": sum(s["label"] == "lane/crosswalk" for s in sh)}
        gd = human("area/direct")
        pd = [mask(s["polygon"]) for s in sh if s["label"] == "area/direct"]
        if gd:
            gm = mask(gd[0]) if len(gd) == 1 else np.clip(sum(mask(p) for p in gd), 0, 1).astype(np.uint8)
            row["direct_iou"] = round(iou(gm, pd[0]), 3) if pd else 0.0
            od = [mask(p) for p in old_draft(fr, "area/direct")]
            row["direct_iou_old"] = round(iou(gm, np.clip(sum(od), 0, 1).astype(np.uint8)), 3) if od else None
            rm = np.clip(sum(mask(p) for p in roads), 0, 1).astype(np.uint8)
            row["direct_in_road"] = round(float((pd[0] & rm).sum() / max(1, pd[0].sum())), 3) if pd else None
            row["direct_top_dy"] = None
            if pd:
                ys = np.nonzero(pd[0].any(1))[0]
                ysg = np.nonzero(gm.any(1))[0]
                row["direct_top_dy"] = int(ys.min() - ysg.min())
        gc = human("lane/crosswalk")
        if gc:
            pc = [mask(s["polygon"]) for s in sh if s["label"] == "lane/crosswalk"]
            oc = [mask(p) for p in old_draft(fr, "lane/crosswalk")]
            row["cw_iou"] = [round(v, 2) for v in best_iou([mask(p) for p in gc], pc)]
            row["cw_iou_old"] = [round(v, 2) for v in best_iou([mask(p) for p in gc], oc)]
        rows.append(row)
        res[fr] = [{k: v for k, v in s.items()} for s in sh]
        o = img.copy()
        ov = o.copy()
        for s in sh:
            c = COL.get(s["label"], (200, 200, 200))
            pts = np.round(np.float32(s["polygon"]).reshape(-1, 2)).astype(np.int32)
            if s["label"].startswith("area/"):
                cv2.fillPoly(ov, [pts], c)
            else:
                cv2.polylines(o, [pts], True, c, 2)
        o = cv2.addWeighted(ov, 0.25, o, 0.75, 0)
        for x in ann:
            if x["frame"] == fr and x["type"] == "polygon" and x["label"] in ("road", "area/direct", "lane/crosswalk") \
                    and _key(fr, x["points"]) not in dk:
                cv2.polylines(o, [np.round(np.float32(x["points"]).reshape(-1, 2)).astype(np.int32)], True,
                              {"road": (0, 120, 0), "area/direct": (0, 0, 255), "lane/crosswalk": (0, 128, 255)}[x["label"]], 1)
        if g["vp"]:
            cv2.drawMarker(o, (int(g["vp"][0]), int(g["vp"][1])), (0, 255, 255), cv2.MARKER_CROSS, 24, 2)
        cv2.putText(o, f"f{fr} {'DARK' if g['dark'] else 'BRIGHT'} vp={g['vp_src']} lines={row['lines']}", (8, 22), 0, 0.55, (0, 255, 0), 2)
        cv2.imwrite(str(OUT / f"f{fr}.jpg"), o)
        print(json.dumps(row, ensure_ascii=False), flush=True)
    json.dump({"rows": rows, "shapes": res}, open(OUT / "lanes_job285_result.json", "w", encoding="utf8"), ensure_ascii=False)
    di = [r["direct_iou"] for r in rows if "direct_iou" in r]
    do = [r["direct_iou_old"] for r in rows if r.get("direct_iou_old") is not None]
    print(f"\nTONG direct IoU moi mean={np.mean(di):.3f} (n={len(di)}); cu mean={np.mean(do) if do else float('nan'):.3f} (n={len(do)}); "
          f"tb {np.mean([r['s'] for r in rows]):.2f}s/frame")


if __name__ == "__main__":
    main()
