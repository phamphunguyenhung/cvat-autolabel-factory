"""Do anh huong chinh sach tien xu ly (do phan giai, tile, tang sang) len IoU road + thoi gian, TACH sang/dem, tung model
(tuan tu, moi model 1 tien trinh rieng), roi chon chinh sach tot nhat trong NGAN SACH cua model (config/model_inputs.yaml).

  python cvat/scripts/seg_input_bench.py                         # b2,b5,m2f,lane,yolo26n/s/l,yolo26s-seg
  python cvat/scripts/seg_input_bench.py --models m2f --frames 60-64
  python cvat/scripts/seg_input_bench.py --gt live               # GT road lay qua client CVAT CHI DOC (job 285)

GT: 20 polygon road nguoi ve tay (frame 60..79). Mac dinh doc cache tools/cvat-seg-copilot/frames/j285_ann.json (ban sao job 285);
--gt live doi chieu lai bang cvat_tools.core.client.Cvat (GET only). Seg model do IoU road (lane: recall lane_paint, GT lane
chi danh dau mot phan). YOLO khong co GT -> chi do thoi gian + so hop (khong ket luan chat luong).
Chinh sach "legacy_square" = tien xu ly cu SAI (HF processor ep vuong) de co moc TRUOC.
"""
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import cv2
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "cvat" / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cvat_tools.segmentation import evidence as E  # noqa: E402
from cvat_tools.segmentation import inputspec as I  # noqa: E402
import seg_model_bench as B  # noqa: E402  (load_gt, tool_draft_keys, iou_recall)

OUT = REPO / "cvat" / "data" / "benchmarks" / "seg_input_bench_job285.json"
SEG = ("b2", "b5", "m2f", "lane")
DETS = ("yolo26n", "yolo26s", "yolo26l", "yolo26s-seg")
BUDGET_KEY = {"b2": "road_sky_model", "b5": "road_sky_model", "m2f": "road_sky_model", "lane": "lane_model",
              "yolo26n": "yolo_tile", "yolo26s": "yolo_tile", "yolo26l": "yolo_tile", "yolo26s-seg": "yolo_tile"}
RES = {"b2": [640, 768, 1024, 1280], "b5": [640, 768, 1024, 1280], "m2f": [512, 640, 768, 1024],
       "lane": [224, 320, 448], "yolo26n": [640, 960, 1280], "yolo26s": [640, 960, 1280], "yolo26l": [640, 960, 1280],
       "yolo26s-seg": [640, 960, 1280]}
LEGACY = {"b5": 1024, "m2f": 384}  # kich thuoc vuong HF AutoImageProcessor
VEH = [0, 1, 2, 3, 5, 7]


def live_road_gt(size, frames) -> dict:
    """GT road qua client CHI DOC (write_enabled=False)."""
    from cvat_tools.core.client import Cvat

    c = Cvat.from_env("local")
    names = {l["id"]: l["name"] for l in c.labels(285)}
    W, H = size
    gt = {}
    for s in c.annotations(285).get("shapes", []):
        if names.get(s["label_id"]) == "road" and s["type"] == "polygon" and s["frame"] in frames:
            m = gt.setdefault((s["frame"], "road"), {"human": np.zeros((H, W), np.uint8), "draft": np.zeros((H, W), np.uint8)})
            cv2.fillPoly(m["human"], [np.round(np.array(s["points"], np.float32).reshape(-1, 2)).astype(np.int32)], 1)
    return gt


class Runner:
    """Chay 1 model seg -> diem so (N,C,h,w) cho tung tile; moi logic tien xu ly qua inputspec."""

    def __init__(self, mid):
        self.mid = mid
        if mid == "b2":
            sys.path.insert(0, str(E._COPILOT_SRC))
            from cvat_seg.scene import SceneParser

            self.sess = SceneParser().session
        else:
            import torch
            from transformers import Mask2FormerForUniversalSegmentation as M2, SegformerForSemanticSegmentation as SF

            torch.set_grad_enabled(False)
            self.torch = torch
            repo = {"b5": E.HF_REPOS["b5"], "m2f": E.HF_REPOS["m2f"], "lane": "8bits-ai/SegFormer-Lane-Marking"}[mid]
            self.model = (M2 if mid == "m2f" else SF).from_pretrained(repo).eval()

    def scores(self, x: np.ndarray) -> np.ndarray:
        outs = []
        for t in x:
            t = t[None]
            if self.mid == "b2":
                o = self.sess.run(None, {"pixel_values": t})[0]
            elif self.mid == "m2f":
                r = self.model(pixel_values=self.torch.from_numpy(t))
                o = self.torch.einsum("bqc,bqhw->bchw", r.class_queries_logits.softmax(-1)[..., :-1], r.masks_queries_logits.sigmoid()).numpy()
            else:
                lg = self.model(pixel_values=self.torch.from_numpy(t)).logits
                o = lg.softmax(1).numpy() if self.mid == "lane" else lg.numpy()
            outs.append(o[0])
        return np.stack(outs)

    def predict(self, frame, policy=None, legacy=None):
        H, W = frame.shape[:2]
        if legacy:  # moc TRUOC: ep vuong nhu HF processor mac dinh
            rgb = cv2.cvtColor(cv2.resize(frame, (legacy, legacy)), cv2.COLOR_BGR2RGB)
            x = ((rgb.astype(np.float32) / 255 - E._MEAN) / E._STD).transpose(2, 0, 1)[None]
            meta = {"orig_hw": (H, W), "in_hw": (legacy, legacy), "pad": (0, 0, 0, 0), "tiles": None}
        else:
            x, meta = I.prepare_input(frame, self.mid, policy)
        sc = self.scores(x)
        sc = sc if meta["tiles"] else sc[0]
        full = I.restore(sc, meta)
        if self.mid == "lane":
            return (full[1] > 0.5).astype(np.uint8) * 255
        return (full.argmax(0) == 0).astype(np.uint8) * 255  # road = class 0 Cityscapes


def run_seg(mid, imgs, gt, bright, budget):
    r = Runner(mid)
    metric_label = "lane_paint" if mid == "lane" else "road"
    key = lambda f: "bright" if f in bright else "night"
    r.predict(next(iter(imgs.values())), {"long_side": 256} if mid != "lane" else {"short_side": 224})  # warm-up, khong tinh

    def run(policy=None, legacy=None, only=None):
        rec = {}
        for f, im in imgs.items():
            if only is not None and f not in only:
                continue
            t = time.time()
            p = r.predict(im, policy, legacy)
            dt = time.time() - t
            g = gt.get((f, metric_label), {}).get("human")
            rec[f] = {"s": dt}
            if g is not None and g.any():
                rec[f]["iou"], rec[f]["recall"] = B.iou_recall(p, g)
        return rec

    def summ(name, policy, rec, extra=None):
        m = "recall" if mid == "lane" else "iou"
        grp = {k: [v for f, v in rec.items() if key(f) == k] for k in ("night", "bright")}
        mv = lambda xs: [v[m] for v in xs if m in v]
        out = {"name": name, "policy": policy, "metric": m, "n": len(mv(rec.values())), **(extra or {}),
               "all": round(float(np.mean(mv(rec.values()))), 3) if mv(rec.values()) else None, "s_mean": round(statistics.mean(v["s"] for v in rec.values()), 2)}
        for k, xs in grp.items():
            out[k] = round(float(np.mean(mv(xs))), 3) if mv(xs) else None
            out[f"s_{k}"] = round(statistics.mean(v["s"] for v in xs), 2) if xs else None
        out["in_budget"] = out["s_mean"] <= budget
        return out

    rows, base = [], {}
    if mid in LEGACY:
        rows.append(summ("legacy_square(truoc)", {"square": LEGACY[mid]}, run(legacy=LEGACY[mid])))
    key_res = "short_side" if mid == "lane" else "long_side"
    for v in RES[mid]:
        base[v] = run({key_res: v, "enhance": "none"})
        rows.append(summ(f"{key_res}={v}", {key_res: v, "enhance": "none"}, base[v]))
    if mid in ("b2", "b5"):  # tile chi thu cho model re (global context cua road co the mat)
        pol = {"long_side": 1280, "tile": {"size": 640, "overlap": 0.25}, "enhance": "none"}
        rows.append(summ("tile640@1280", pol, run(pol)))
    cand = [x for x in rows if x["in_budget"] and "square" not in x["policy"] and not x["policy"].get("tile")]
    bestres = max(cand, key=lambda x: x["all"]) if cand else min((x for x in rows if "long_side" in x["policy"] or "short_side" in x["policy"]), key=lambda x: x["s_mean"])
    v = bestres["policy"][key_res]
    dark = {f for f in imgs if key(f) == "night"}
    for en in ("gamma", "clahe", "gamma_clahe"):  # frame sang khong doi -> tai dung ket qua nen; chi chay lai frame toi
        pol = {key_res: v, "enhance": en}
        rec = {**{f: x for f, x in base[v].items() if f not in dark}, **run(pol, only=dark)}
        rows.append(summ(f"{key_res}={v}+{en}", pol, rec))
    return rows


def run_det(mid, imgs):
    from ultralytics import YOLO
    import torch
    from torchvision.ops import nms

    sp = I.get_spec(mid)
    model = YOLO(str(REPO / sp["ref"]))
    first = next(iter(imgs.values()))
    model.predict(first, imgsz=320, verbose=False)
    rows = []

    def infer(frame, pol):
        x, meta = I.prepare_input(frame, mid, pol)
        tiles = x if isinstance(x, list) else [x]
        bs, sc = [], []
        for i, t in enumerate(tiles):
            res = model.predict(t, imgsz=max(t.shape[:2]), classes=VEH, conf=0.25, verbose=False)[0]
            if len(res.boxes):
                bs.append(I.restore_boxes(res.boxes.xyxy.numpy(), meta, i if meta["tiles"] else None))
                sc.append(res.boxes.conf.numpy())
        if not bs:
            return 0
        b, s = np.concatenate(bs), np.concatenate(sc)
        return int(len(nms(torch.from_numpy(b), torch.from_numpy(s), 0.5)))

    pols = [(f"imgsz={v}", {"long_side": v}) for v in RES[mid]] + [("tile640@1280", {"long_side": 1280, "tile": {"size": 640, "overlap": 0.2}})]
    if mid == "yolo26s-seg":
        pols = pols[:3]
    for name, pol in pols:
        ts, ns = [], []
        for f, im in imgs.items():
            t = time.time()
            n = infer(im, pol)
            ts.append(time.time() - t)
            ns.append(n)
        rows.append({"name": name, "policy": pol, "s_mean": round(statistics.mean(ts), 2), "boxes_mean": round(statistics.mean(ns), 1),
                     "metric": "none (khong GT)"})
    d0 = len(model.predict(first, imgsz=640, classes=VEH, conf=0.25, verbose=False)[0].boxes)
    d1 = infer(first, {"long_side": 640})
    for x in rows:
        x["contract_vs_direct_640_frame0"] = [d1, d0]
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default=",".join(SEG + DETS))
    ap.add_argument("--frames", default="60-79")
    ap.add_argument("--gt", choices=("cache", "live"), default="cache")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--worker", default="")
    a = ap.parse_args()
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    fr = [int(y) for x in a.frames.split(",") for y in (range(int(x.split("-")[0]), int(x.split("-")[1]) + 1) if "-" in x else [x])]
    imgs = {f: cv2.imread(str(B.FRAMES / f"j285_f{f}.jpg")) for f in fr}
    H, W = next(iter(imgs.values())).shape[:2]
    bright = {f for f, im in imgs.items() if I.mean_gray(im) >= B.BRIGHT_MEAN}
    gt = B.load_gt(B.FRAMES / "j285_ann.json", B.tool_draft_keys(), (W, H))
    if a.gt == "live":
        lg = live_road_gt((W, H), set(fr))
        same = sum(bool((lg[k]["human"] == gt[k]["human"]).all()) for k in lg if k in gt)
        print(f"GT live: {len(lg)} road polygon-frame, trung cache {same}/{len(lg)}", flush=True)
        gt.update({k: v for k, v in lg.items()})
    specs = I.load_specs()
    if a.worker:
        mid = a.worker
        budget = specs["pipeline_budget_s"][BUDGET_KEY[mid]]
        rows = run_seg(mid, imgs, gt, bright, budget) if mid in SEG else run_det(mid, imgs)
        Path(a.out).write_text(json.dumps({"budget_s": budget, "rows": rows}), encoding="utf8")
        return 0
    print(f"{len(imgs)} frame, sang={sorted(bright)}, toi={len(imgs) - len(bright)}; ngan sach tong {specs['pipeline_budget_s']}", flush=True)
    res = {}
    for mid in a.models.split(","):  # TUAN TU
        tmp = Path(tempfile.gettempdir()) / f"inbench_{mid}.json"
        t = time.time()
        extra = ["--gt", a.gt] if mid in SEG else []
        subprocess.run([sys.executable, __file__, "--worker", mid, "--frames", a.frames, "--out", str(tmp), *extra], check=True, stderr=subprocess.DEVNULL)
        res[mid] = json.loads(tmp.read_text(encoding="utf8"))
        print(f"\n== {mid} (ngan sach {res[mid]['budget_s']} s; chay {time.time() - t:.0f}s) ==", flush=True)
        for x in res[mid]["rows"]:
            if "iou" in x["metric"] or x["metric"] == "recall":
                print(f"  {x['name'].ljust(26)} {x['metric']}: dem {x['night']} / sang {x['bright']} / tat ca {x['all']}   {x['s_mean']:5.2f}s (dem {x['s_night']}, sang {x['s_bright']}){'' if x['in_budget'] else '  VUOT NGAN SACH'}", flush=True)
            else:
                print(f"  {x['name'].ljust(26)} {x['s_mean']:5.2f}s  {x['boxes_mean']} hop/frame", flush=True)
    rec = {}
    for mid, r in res.items():
        if mid in SEG:
            ok = [x for x in r["rows"] if x["in_budget"] and "square" not in x["policy"]]
            if ok:
                b = max(ok, key=lambda x: (x["all"], -x["s_mean"]))
                rec[mid] = {"policy": b["policy"], "all": b["all"], "night": b["night"], "bright": b["bright"], "s_mean": b["s_mean"]}
            else:
                rec[mid] = {"error": "khong chinh sach nao trong ngan sach", "fastest_s": min(x["s_mean"] for x in r["rows"])}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps({"bright_frames": sorted(bright), "budget": specs["pipeline_budget_s"], "models": res, "recommended": rec}, ensure_ascii=False, indent=1), encoding="utf8")
    print("\nkhuyen nghi trong ngan sach:", json.dumps(rec, ensure_ascii=False))
    print(f"luu {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
