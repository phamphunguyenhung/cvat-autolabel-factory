"""Export full-label BBOX (Things + Lanes + Areas + Stuff) previews for Job 285 (frames 60-79).

Combines:
- Objects (car, truck, bus, motorcycle, pedestrian, traffic light, traffic sign) from CVAT human + latest YOLO26l all_bbox drafts
- Lanes & Areas (lane/single yellow, lane/double yellow, lane/single white, lane/double white, lane/crosswalk, area/direct, area/alternative) from cvat_tools.lanes.framegen
- Scene/Stuff (pole, building, road, sidewalk, sky, vegetation, fence, terrain, lane/road curb) from LATEST_bboxfull.json

All polygons are converted to [x1, y1, x2, y2] bounding boxes and rendered locally.
"""
from __future__ import annotations

import glob
import json
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import cv2
import numpy as np

CVAT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CVAT_ROOT / "src"))

from cvat_tools.lanes.framegen import generate_frame  # noqa: E402

FRAMES_DIR = CVAT_ROOT.parent / "tools" / "cvat-seg-copilot" / "frames"
JOB_DIR = CVAT_ROOT / "week01" / "job285-bbox"
DRAFTS_DIR = JOB_DIR / "drafts"
ALL_BBOX_DRAFTS = CVAT_ROOT / "data" / "jobs" / "285" / "previews" / "all_bbox" / "drafts"
OUT_DIR = JOB_DIR / "previews_full_bbox"

# Exact CVAT Job 285 label colors (#RRGGBB -> BGR)
PALETTE: dict[str, tuple[int, int, int]] = {
    "pedestrian": (96, 224, 128),        # #80e060
    "rider": (0, 0, 255),                # #FF0000
    "car": (142, 0, 0),                  # #00008E
    "truck": (70, 0, 0),                 # #000046
    "bus": (100, 60, 0),                 # #003C64
    "train": (100, 80, 0),               # #005064
    "motorcycle": (230, 0, 0),           # #0000E6
    "bicycle": (32, 11, 119),            # #770B20
    "traffic light": (0, 160, 208),      # #d0a000
    "traffic sign": (128, 32, 80),       # #502080
    "traffic_sign": (0, 220, 220),       # #DCDC00
    "area/alternative": (178, 196, 98),  # #62c4b2
    "area/direct": (106, 55, 64),        # #40376a
    "lane/crosswalk": (140, 242, 125),   # #7df28c
    "lane/double white": (19, 196, 216), # #d8c413
    "lane/double yellow": (253, 61, 186),# #ba3dfd
    "lane/road curb": (137, 1, 110),     # #6e0189
    "lane/single other": (96, 31, 255),  # #ff1f60
    "lane/single white": (164, 250, 164),# #a4faa4
    "lane/single yellow": (240, 77, 84), # #544df0
    "road": (128, 64, 128),              # #804080
    "sidewalk": (232, 35, 244),          # #F423E8
    "building": (70, 70, 70),            # #464646
    "wall": (156, 102, 102),             # #66669C
    "fence": (153, 153, 190),            # #BE9999
    "pole": (153, 153, 153),             # #999999
    "vegetation": (35, 142, 107),        # #6B8E23
    "terrain": (152, 251, 152),          # #98FB98
    "sky": (180, 130, 70),               # #4682B4
}


def poly_to_bbox(pts: list[float]) -> list[float]:
    arr = np.asarray(pts, dtype=np.float32).reshape(-1, 2)
    return [
        round(float(arr[:, 0].min()), 1),
        round(float(arr[:, 1].min()), 1),
        round(float(arr[:, 0].max()), 1),
        round(float(arr[:, 1].max()), 1),
    ]


LABEL_ID_MAP: dict[int, str] = {
    941: "pedestrian",
    942: "rider",
    943: "car",
    944: "truck",
    945: "bus",
    946: "motorcycle",
    947: "bicycle",
    948: "train",
    949: "traffic light",
    950: "traffic sign",
    951: "area/alternative",
    952: "area/direct",
    953: "lane/crosswalk",
    954: "lane/double white",
    955: "lane/double yellow",
    956: "lane/road curb",
    958: "lane/single white",
    959: "lane/single yellow",
    1942: "road",
    1943: "sidewalk",
    1944: "building",
    1945: "wall",
    1946: "fence",
    1947: "pole",
    1950: "vegetation",
    1951: "terrain",
    1952: "sky",
}


def load_all_bbox_drafts() -> dict[int, list[dict[str, Any]]]:
    by_frame: dict[int, list[dict[str, Any]]] = {}
    files = sorted(ALL_BBOX_DRAFTS.glob("all_bbox_*.json"))
    if not files:
        return by_frame
    latest = json.loads(files[-1].read_text(encoding="utf-8"))
    for s in latest.get("shapes", []):
        if s.get("type") != "rectangle":
            continue
        f = int(s["frame"])
        lbl = s.get("_label") or LABEL_ID_MAP.get(s.get("label_id", -1), f"id_{s.get('label_id')}")
        by_frame.setdefault(f, []).append(
            {
                "label": lbl,
                "box": [round(float(x), 1) for x in s["points"]],
                "source": "yolo26l_draft",
            }
        )
    return by_frame


def _iou(a: list[float], b: list[float]) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    if inter <= 0.0:
        return 0.0
    ua = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
    ub = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
    return inter / max(1e-6, ua + ub - inter)


def _iomin(a: list[float], b: list[float]) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    if inter <= 0.0:
        return 0.0
    ua = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
    ub = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
    return inter / max(1e-6, min(ua, ub))


def _canon_label(lbl: str) -> str:
    return "traffic sign" if lbl == "traffic_sign" else lbl


def _has_visual_evidence(img_bgr: np.ndarray, poly: list[float], lbl: str) -> bool:
    """Reject pitch-black night-sky/void hallucinations for seg_stuff (requires actual visual texture/luma)."""
    if lbl not in {"building", "vegetation", "terrain", "pole"}:
        return True
    H, W = img_bgr.shape[:2]
    m = np.zeros((H, W), np.uint8)
    pts = np.round(np.float32(poly).reshape(-1, 2)).astype(np.int32)
    cv2.fillPoly(m, [pts], 1)
    idx = m > 0
    if not idx.any():
        return False
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    vals = gray[idx]
    mean_l = float(vals.mean())
    p90_l = float(np.percentile(vals, 90))
    edges = cv2.Canny(gray, 40, 120)
    edge_dens = float((edges[idx] > 0).mean())
    if lbl == "building" and mean_l < 18.0 and p90_l < 34.0 and edge_dens < 0.025:
        return False
    if lbl in {"vegetation", "terrain"} and mean_l < 14.0 and p90_l < 26.0:
        return False
    return True


def _dedupe_boxes(items: list[dict[str, Any]], iou_thresh: float = 0.50, iomin_thresh: float = 0.72) -> list[dict[str, Any]]:
    white_lanes = {"lane/single white", "lane/double white"}
    yellow_lanes = {"lane/single yellow", "lane/double yellow"}
    kept: list[dict[str, Any]] = []
    for item in sorted(items, key=lambda x: (0 if x.get("source") == "cvat_human" else 1, -float(x.get("conf", 1.0)))):
        cl = _canon_label(item["label"])
        conflict = False
        for k in kept:
            kl = _canon_label(k["label"])
            same_group = (
                (kl == cl)
                or (kl in white_lanes and cl in white_lanes)
                or (kl in yellow_lanes and cl in yellow_lanes)
            )
            if same_group and (_iou(k["box"], item["box"]) >= iou_thresh or _iomin(k["box"], item["box"]) >= iomin_thresh):
                conflict = True
                break
        if conflict:
            continue
        kept.append(item)
    return kept


def load_stuff_drafts() -> dict[int, list[dict[str, Any]]]:
    from cvat_tools.segmentation import geomrefine

    by_frame: dict[int, list[dict[str, Any]]] = {}
    p = DRAFTS_DIR / "LATEST_bboxfull.json"
    if not p.exists():
        return by_frame
    data = json.loads(p.read_text(encoding="utf-8"))
    for s in data.get("shapes", []):
        lbl = s.get("_label", "")
        if not lbl or lbl.startswith("area/") or (lbl.startswith("lane/") and lbl != "lane/road curb"):
            continue
        if lbl in {"car", "truck", "bus", "motorcycle", "pedestrian", "traffic light", "traffic sign"}:
            continue
        f = int(s["frame"])
        pts = s.get("points", [])
        if len(pts) < 4:
            continue
        if s.get("type") == "polygon" and len(pts) >= 6:
            pts = geomrefine.refine(pts, geomrefine.kind_for_label(lbl))
            if len(pts) < 6:
                continue
        box = [round(float(x), 1) for x in pts[:4]] if s.get("type") == "rectangle" else poly_to_bbox(pts)
        bw, bh = box[2] - box[0], box[3] - box[1]
        if bw < 4.0 or bh < 4.0:
            continue
        if lbl == "road" and box[1] < 180.0:
            continue
        if lbl == "sky" and box[3] > 360.0:
            continue
        if lbl == "pole" and (bw * bh) < 120.0:
            continue
        by_frame.setdefault(f, []).append(
            {"label": lbl, "box": box, "polygon": pts if s.get("type") == "polygon" else None, "source": "seg_stuff"}
        )
    return by_frame


def _text_color(bgr: tuple[int, int, int]) -> tuple[int, int, int]:
    b, g, r = bgr
    luma = 0.114 * b + 0.587 * g + 0.299 * r
    return (0, 0, 0) if luma > 135 else (255, 255, 255)


def _luma(bgr: tuple[int, int, int]) -> float:
    return 0.114 * bgr[0] + 0.587 * bgr[1] + 0.299 * bgr[2]


def _draw_dashed_line(img: np.ndarray, p1: tuple[int, int], p2: tuple[int, int], color: tuple[int, int, int], thick: int, dash: int = 8, gap: int = 5) -> None:
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    dist = float(np.hypot(dx, dy))
    if dist < 1.0:
        return
    ux, uy = dx / dist, dy / dist
    pos = 0.0
    while pos < dist:
        end = min(dist, pos + dash)
        a = (int(round(p1[0] + ux * pos)), int(round(p1[1] + uy * pos)))
        b = (int(round(p1[0] + ux * end)), int(round(p1[1] + uy * end)))
        cv2.line(img, a, b, color, thick, cv2.LINE_AA)
        pos += dash + gap


def _draw_dashed_rect(img: np.ndarray, x1: int, y1: int, x2: int, y2: int, color: tuple[int, int, int], thick: int) -> None:
    for p1, p2 in (((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)), ((x2, y2), (x1, y2)), ((x1, y2), (x1, y1))):
        _draw_dashed_line(img, p1, p2, color, thick)


def _draw_dashed_poly(img: np.ndarray, pts: np.ndarray, color: tuple[int, int, int], thick: int) -> None:
    n = len(pts)
    for i in range(n):
        p1 = (int(pts[i][0]), int(pts[i][1]))
        p2 = (int(pts[(i + 1) % n][0]), int(pts[(i + 1) % n][1]))
        _draw_dashed_line(img, p1, p2, color, thick)


def _place_tag(
    placed: list[tuple[int, int, int, int]],
    ax: int,
    ay: int,
    tw: int,
    th: int,
    W: int,
    H: int,
    box_y2: int,
) -> tuple[int, int]:
    """Find a non-overlapping label tag position near anchor (ax, ay)."""
    candidates = [
        (ax, ay - th - 4),
        (ax, ay + 2),
        (ax, box_y2 + 2),
    ]
    for step in range(1, 5):
        candidates.append((ax, ay - th - 4 - step * (th + 5)))
        candidates.append((ax, ay + 2 + step * (th + 5)))
    for cx, cy in candidates:
        tx = max(0, min(cx, W - tw - 6))
        ty = max(0, min(cy, H - th - 6))
        r = (tx, ty, tx + tw + 4, ty + th + 4)
        if not any(min(r[2], p[2]) > max(r[0], p[0]) and min(r[3], p[3]) > max(r[1], p[1]) for p in placed):
            placed.append(r)
            return tx, ty
    tx = max(0, min(ax, W - tw - 6))
    ty = max(0, min(ay - th - 4, H - th - 6))
    placed.append((tx, ty, tx + tw + 4, ty + th + 4))
    return tx, ty


def draw_frame(
    img_bgr: np.ndarray,
    frame_idx: int,
    is_night: bool,
    boxes: list[dict[str, Any]],
    *,
    compact: bool = False,
) -> np.ndarray:
    """Render annotations in CVAT Web UI style: per-layer translucent fills, solid=human vs dashed=AI draft."""
    H, W = img_bgr.shape[:2]
    vis = img_bgr.copy()

    def layer_rank(lbl: str) -> int:
        if lbl.startswith("area/") or lbl.startswith("lane/"):
            return 1
        if lbl in {"car", "truck", "bus", "motorcycle", "bicycle", "pedestrian", "rider", "traffic light", "traffic sign", "traffic_sign"}:
            return 2
        return 0

    ordered = sorted(boxes, key=lambda x: layer_rank(x["label"]))

    # Pass 1: per-layer translucent fills so dark roads & car bodies stay clear
    for rank_target, alpha in ((0, 0.16), (1, 0.26), (2, 0.12)):
        ov = vis.copy()
        drawn = False
        for item in ordered:
            lbl = item["label"]
            if layer_rank(lbl) != rank_target:
                continue
            color = PALETTE.get(lbl, (200, 200, 200))
            if item.get("polygon") and len(item["polygon"]) >= 6:
                pts = np.round(np.float32(item["polygon"]).reshape(-1, 2)).astype(np.int32)
                cv2.fillPoly(ov, [pts], color)
                drawn = True
            elif rank_target == 2:
                x1, y1, x2, y2 = [int(round(v)) for v in item["box"]]
                cv2.rectangle(ov, (x1, y1), (x2, y2), color, -1)
                drawn = True
        if drawn:
            vis = cv2.addWeighted(ov, alpha, vis, 1.0 - alpha, 0.0)

    # Pass 2: crisp CVAT-style borders & non-overlapping label tags (light halo on dark night colors)
    placed_tags: list[tuple[int, int, int, int]] = []
    for item in ordered:
        lbl = item["label"]
        color = PALETTE.get(lbl, (200, 200, 200))
        rank = layer_rank(lbl)
        x1, y1, x2, y2 = [int(round(v)) for v in item["box"]]
        need_halo = is_night and _luma(color) < 75.0
        thick = 2 if (rank >= 1 or need_halo) else 1

        if item.get("polygon") and len(item["polygon"]) >= 6:
            pts = np.round(np.float32(item["polygon"]).reshape(-1, 2)).astype(np.int32)
            if need_halo:
                cv2.polylines(vis, [pts], True, (220, 220, 220), thick + 1, cv2.LINE_AA)
            cv2.polylines(vis, [pts], True, color, thick, cv2.LINE_AA)
        else:
            if need_halo:
                cv2.rectangle(vis, (x1, y1), (x2, y2), (220, 220, 220), thick + 1)
            cv2.rectangle(vis, (x1, y1), (x2, y2), color, thick)

        if not compact and rank >= 1 and ((x2 - x1) >= 22 or (y2 - y1) >= 22):
            (tw, th), _ = cv2.getTextSize(lbl, cv2.FONT_HERSHEY_SIMPLEX, 0.36, 1)
            if rank == 1 and item.get("polygon") and len(item["polygon"]) >= 6:
                arr = np.float32(item["polygon"]).reshape(-1, 2)
                ax, ay = int(arr[:, 0].mean()) - tw // 2, int(np.percentile(arr[:, 1], 65))
            else:
                ax, ay = x1, y1
            tx, ty = _place_tag(placed_tags, ax, ay, tw, th, W, H, y2)
            cv2.rectangle(vis, (tx, ty), (tx + tw + 4, ty + th + 4), color, -1)
            cv2.putText(vis, lbl, (tx + 2, ty + th + 1), cv2.FONT_HERSHEY_SIMPLEX, 0.36, _text_color(color), 1, cv2.LINE_AA)

    if compact:
        return vis

    mode = "NIGHT" if is_night else "DAY"
    cnt = Counter(b["label"] for b in boxes)
    lane_n = sum(v for k, v in cnt.items() if k.startswith("lane/"))
    area_n = sum(v for k, v in cnt.items() if k.startswith("area/"))
    rect_n = sum(v for k, v in cnt.items() if layer_rank(k) == 2)
    header = f"CVAT Job 285 | Frame {frame_idx} ({mode}) | rects={rect_n} lanes={lane_n} areas={area_n} total={len(boxes)}"
    bar = np.full((30, W, 3), 24, dtype=np.uint8)
    cv2.putText(bar, header, (10, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.54, (255, 255, 255), 1, cv2.LINE_AA)
    return np.vstack([bar, vis])


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ann = json.loads((FRAMES_DIR / "j285_ann.json").read_text(encoding="utf-8"))
    yolo_drafts = load_all_bbox_drafts()
    stuff_drafts = load_stuff_drafts()

    label_totals: Counter[str] = Counter()
    export_json: dict[str, Any] = {"job": 285, "frames": {}, "label_totals": {}}
    thumbs: list[np.ndarray] = []

    t_start = time.perf_counter()
    for f in range(60, 80):
        img = cv2.imread(str(FRAMES_DIR / f"j285_f{f}.jpg"), cv2.IMREAD_COLOR)
        if img is None:
            continue

        frame_boxes: list[dict[str, Any]] = []

        thing_items: list[dict[str, Any]] = []
        # 1. Human object rectangles from CVAT j285_ann.json
        for x in ann:
            if x["frame"] == f and x["type"] == "rectangle":
                thing_items.append({"label": x["label"], "box": [round(float(v), 1) for v in x["points"]], "source": "cvat_human"})

        # 2. Additional YOLO26l object rectangles from all_bbox draft (filter road traffic-light & hood FPs)
        H, W = img.shape[:2]
        for yd in yolo_drafts.get(f, []):
            bx = yd["box"]
            cy = (bx[1] + bx[3]) / 2.0
            area = (bx[2] - bx[0]) * (bx[3] - bx[1])
            if yd["label"] == "traffic light" and cy > 0.55 * H:
                continue
            if yd["label"] == "car" and bx[1] > 500.0 and area < 2500.0:
                continue
            thing_items.append(yd)
        frame_boxes.extend(_dedupe_boxes(thing_items, iou_thresh=0.50, iomin_thresh=0.72))

        # 3. Lanes & Areas from cvat_tools.lanes.framegen -> filtered & deduped BBOX
        roads = [x["points"] for x in ann if x["frame"] == f and x["label"] == "road" and x["type"] == "polygon"]
        g = generate_frame(img, roads)
        lane_items: list[dict[str, Any]] = []
        for s in g["shapes"]:
            poly = s["polygon"]
            box = poly_to_bbox(poly)
            box = [max(0.0, box[0]), max(0.0, box[1]), min(float(W), box[2]), min(float(H), box[3])]
            bw, bh = box[2] - box[0], box[3] - box[1]
            if bw < 4.0 or bh < 4.0:
                continue
            if s["label"] == "area/alternative" and (bw * bh < 2500.0 or bw < 20.0 or bh < 20.0):
                continue
            if float(s.get("conf", 1.0)) < 0.25:
                continue
            lane_items.append(
                {
                    "label": s["label"],
                    "box": box,
                    "polygon": poly,
                    "conf": float(s.get("conf", 1.0)),
                    "source": "lanes_framegen",
                }
            )
        frame_boxes.extend(_dedupe_boxes(lane_items, iou_thresh=0.70))

        # 4. Stuff / Scene polygons (prefer CVAT human polygons, fill missing from stuff_drafts)
        human_stuff_labels: set[str] = set()
        for x in ann:
            if x["frame"] == f and x["type"] == "polygon" and not x["label"].startswith("area/") and not x["label"].startswith("lane/"):
                human_stuff_labels.add(x["label"])
                frame_boxes.append({"label": x["label"], "box": poly_to_bbox(x["points"]), "polygon": x["points"], "source": "cvat_human"})
        for sd in stuff_drafts.get(f, []):
            if sd["label"] not in human_stuff_labels:
                if sd.get("polygon") and not _has_visual_evidence(img, sd["polygon"], sd["label"]):
                    continue
                frame_boxes.append(sd)

        vis = draw_frame(img, f, bool(g["dark"]), frame_boxes)
        out_img = OUT_DIR / f"f{f}_full_bbox.jpg"
        cv2.imwrite(str(out_img), vis)

        # Crisp grid thumbnail: render shapes without tiny tags, resize with INTER_AREA, then draw crisp 640px header
        tile_raw = draw_frame(img, f, bool(g["dark"]), frame_boxes, compact=True)
        tile = cv2.resize(tile_raw, (640, 360), interpolation=cv2.INTER_AREA)
        tbar = np.full((24, 640, 3), 22, dtype=np.uint8)
        mode = "NIGHT" if g["dark"] else "DAY"
        cv2.putText(tbar, f"Frame {f} ({mode}) | {len(frame_boxes)} shapes", (8, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)
        thumbs.append(np.vstack([tbar, tile]))

        from cvat_tools.segmentation.layers import z_order as _z_order
        for b in frame_boxes:
            label_totals[b["label"]] += 1
        export_json["frames"][str(f)] = [
            {
                "label": b["label"],
                "shape_type": "polygon" if (b.get("polygon") and len(b["polygon"]) >= 6) else "rectangle",
                "points": b["polygon"] if (b.get("polygon") and len(b["polygon"]) >= 6) else b["box"],
                "box": b["box"],
                "z_order": _z_order(b["label"]),
                "stage": "human_final" if b.get("source") == "cvat_human" else "rule_draft",
                "source": b["source"],
            }
            for b in frame_boxes
        ]
        print(f"Frame {f}: {len(frame_boxes)} shapes -> {out_img.name}")

    # Summary 4x5 grid
    if thumbs:
        while len(thumbs) % 4 != 0:
            thumbs.append(np.zeros_like(thumbs[0]))
        rows = [np.hstack(thumbs[i : i + 4]) for i in range(0, len(thumbs), 4)]
        cv2.imwrite(str(OUT_DIR / "summary_grid_20frames.jpg"), np.vstack(rows))

    export_json["label_totals"] = dict(sorted(label_totals.items(), key=lambda kv: -kv[1]))
    (OUT_DIR / "full_bbox_job285.json").write_text(
        json.dumps(export_json, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Done in {time.perf_counter() - t_start:.2f}s! Totals:", export_json["label_totals"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
