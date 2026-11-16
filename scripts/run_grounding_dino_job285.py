"""Run Grounding DINO (full CVAT Job 285 labels) on all 20 frames (60-79) and export local previews.

Usage:
  python scripts/run_grounding_dino_job285.py
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

import cv2
import numpy as np
import torch
from PIL import Image
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

CVAT_ROOT = Path(__file__).resolve().parents[1]
FRAMES_DIR = CVAT_ROOT.parent / "tools" / "cvat-seg-copilot" / "frames"
OUT_DIR = CVAT_ROOT / "week01" / "job285-bbox" / "previews_dino"

MODEL_ID = "IDEA-Research/grounding-dino-tiny"

PROMPT_GROUPS = [
    (
        "things",
        "car . truck . bus . motorcycle . bicycle . pedestrian . rider . train . traffic light . traffic sign .",
        0.24,
    ),
    (
        "stuff",
        "pole . building . fence . road . sidewalk . sky . terrain . vegetation . crosswalk . road curb . lane line .",
        0.22,
    ),
]

PHRASE_TO_LABEL = {
    "car": "car",
    "truck": "truck",
    "bus": "bus",
    "motorcycle": "motorcycle",
    "bicycle": "bicycle",
    "pedestrian": "pedestrian",
    "person": "pedestrian",
    "rider": "rider",
    "train": "train",
    "traffic light": "traffic light",
    "traffic sign": "traffic sign",
    "pole": "pole",
    "building": "building",
    "fence": "fence",
    "road": "road",
    "sidewalk": "sidewalk",
    "sky": "sky",
    "terrain": "terrain",
    "vegetation": "vegetation",
    "crosswalk": "lane/crosswalk",
    "road curb": "lane/road curb",
    "lane line": "lane/single white",
}

PALETTE: dict[str, tuple[int, int, int]] = {
    "car": (0, 220, 0),
    "truck": (0, 165, 255),
    "bus": (0, 120, 255),
    "motorcycle": (255, 200, 0),
    "bicycle": (255, 160, 0),
    "pedestrian": (0, 255, 255),
    "rider": (255, 255, 0),
    "train": (180, 105, 255),
    "traffic light": (0, 60, 255),
    "traffic sign": (255, 0, 200),
    "pole": (200, 200, 200),
    "building": (150, 120, 90),
    "fence": (180, 160, 120),
    "road": (128, 64, 128),
    "sidewalk": (232, 35, 244),
    "sky": (255, 190, 120),
    "terrain": (152, 251, 152),
    "vegetation": (35, 142, 107),
    "lane/crosswalk": (255, 255, 255),
    "lane/road curb": (200, 150, 255),
    "lane/single white": (220, 220, 255),
}


def compute_iou(a: list[float], b: list[float]) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    if inter <= 0.0:
        return 0.0
    area_a = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
    area_b = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
    union = area_a + area_b - inter
    return inter / union if union > 0.0 else 0.0


def map_phrase(raw_phrase: str) -> str:
    p = raw_phrase.strip().lower()
    if p in PHRASE_TO_LABEL:
        return PHRASE_TO_LABEL[p]
    for k, v in PHRASE_TO_LABEL.items():
        if k in p:
            return v
    return p


def enhance_if_night(img_bgr: np.ndarray) -> tuple[np.ndarray, bool]:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    is_night = float(gray.mean()) < 75.0
    if not is_night:
        return img_bgr, False
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l_ch, a_ch, b_ch = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    l_eq = clahe.apply(l_ch)
    enhanced = cv2.cvtColor(cv2.merge([l_eq, a_ch, b_ch]), cv2.COLOR_LAB2BGR)
    return enhanced, True


def nms_boxes(dets: list[dict[str, Any]], iou_thresh: float = 0.55) -> list[dict[str, Any]]:
    vehicle_group = {"car", "truck", "bus", "train"}
    kept: list[dict[str, Any]] = []
    for d in sorted(
        dets,
        key=lambda x: x["conf"] + (0.15 if x["label"] == "car" else 0.0),
        reverse=True,
    ):
        conflict = False
        for k in kept:
            iou = compute_iou(k["box"], d["box"])
            if k["label"] == d["label"] and iou >= iou_thresh:
                conflict = True
                break
            if k["label"] in vehicle_group and d["label"] in vehicle_group and iou >= 0.70:
                conflict = True
                break
        if not conflict:
            kept.append(d)
    return kept


def draw_boxes(img_bgr: np.ndarray, frame_idx: int, is_night: bool, dets: list[dict[str, Any]], elapsed_s: float) -> np.ndarray:
    vis = img_bgr.copy()
    # Draw stuff/lanes first (thin), then things (thicker) so cars/signs stay readable
    stuff_labels = {"sky", "road", "building", "vegetation", "terrain", "sidewalk", "fence", "pole", "lane/crosswalk", "lane/road curb", "lane/single white"}
    ordered = sorted(dets, key=lambda d: (0 if d["label"] in stuff_labels else 1, -d["conf"]))
    for d in ordered:
        x1, y1, x2, y2 = [int(round(v)) for v in d["box"]]
        lbl = d["label"]
        color = PALETTE.get(lbl, (0, 255, 180))
        thick = 1 if lbl in stuff_labels else 2
        cv2.rectangle(vis, (x1, y1), (x2, y2), color, thick)
        txt = f"{lbl} {d['conf']:.2f}"
        (tw, th), _ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, 0.42, 1)
        ty = max(th + 4, y1)
        cv2.rectangle(vis, (x1, ty - th - 4), (x1 + tw + 4, ty), color, -1)
        cv2.putText(vis, txt, (x1 + 2, ty - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 0), 1, cv2.LINE_AA)

    mode = "NIGHT" if is_night else "DAY"
    header = f"Job 285 | Frame {frame_idx} ({mode}) | GroundingDINO-tiny FULL LABELS: {len(dets)} boxes | {elapsed_s:.1f}s"
    cv2.rectangle(vis, (0, 0), (vis.shape[1], 28), (15, 15, 15), -1)
    cv2.putText(vis, header, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (255, 255, 255), 1, cv2.LINE_AA)
    return vis


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    torch.set_grad_enabled(False)
    print(f"Loading {MODEL_ID}...")
    t_load = time.perf_counter()
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model = AutoModelForZeroShotObjectDetection.from_pretrained(MODEL_ID)
    model.eval()
    print(f"Loaded in {time.perf_counter() - t_load:.2f}s")

    all_results: dict[str, Any] = {"model": MODEL_ID, "frames": {}, "label_totals": {}}
    thumbs: list[np.ndarray] = []

    for f in range(60, 80):
        img_path = FRAMES_DIR / f"j285_f{f}.jpg"
        if not img_path.exists():
            print(f"Missing {img_path}, skipping")
            continue
        img_bgr = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
        infer_bgr, is_night = enhance_if_night(img_bgr)
        pil_img = Image.fromarray(cv2.cvtColor(infer_bgr, cv2.COLOR_BGR2RGB))

        t0 = time.perf_counter()
        raw_dets: list[dict[str, Any]] = []
        for _group_name, prompt, thresh in PROMPT_GROUPS:
            inputs = processor(images=pil_img, text=prompt, return_tensors="pt")
            outputs = model(**inputs)
            res = processor.post_process_grounded_object_detection(
                outputs,
                inputs.input_ids,
                threshold=thresh,
                text_threshold=0.20,
                target_sizes=[pil_img.size[::-1]],
            )[0]
            labels_list = res.get("text_labels") or res.get("labels") or []
            for box, score, raw_lbl in zip(res["boxes"].tolist(), res["scores"].tolist(), labels_list):
                lbl = map_phrase(str(raw_lbl))
                raw_dets.append({"label": lbl, "conf": round(float(score), 4), "box": [round(float(v), 1) for v in box]})

        merged = nms_boxes(raw_dets)
        elapsed_s = time.perf_counter() - t0
        vis = draw_boxes(img_bgr, f, is_night, merged, elapsed_s)
        out_img = OUT_DIR / f"f{f}_dino.jpg"
        cv2.imwrite(str(out_img), vis)
        thumbs.append(cv2.resize(vis, (480, 270)))

        all_results["frames"][str(f)] = {"is_night": is_night, "count": len(merged), "elapsed_s": round(elapsed_s, 2), "detections": merged}
        for d in merged:
            all_results["label_totals"][d["label"]] = all_results["label_totals"].get(d["label"], 0) + 1
        print(f"Frame {f} ({'night' if is_night else 'day'}): {len(merged)} boxes in {elapsed_s:.2f}s -> {out_img.name}")

    if thumbs:
        rows = []
        cols = 4
        while len(thumbs) % cols != 0:
            thumbs.append(np.zeros_like(thumbs[0]))
        for i in range(0, len(thumbs), cols):
            rows.append(np.hstack(thumbs[i : i + cols]))
        grid = np.vstack(rows)
        cv2.imwrite(str(OUT_DIR / "summary_grid_20frames.jpg"), grid)

    (OUT_DIR / "dino_full_predictions.json").write_text(
        json.dumps(all_results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("Done! Totals:", dict(sorted(all_results["label_totals"].items(), key=lambda kv: -kv[1])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
