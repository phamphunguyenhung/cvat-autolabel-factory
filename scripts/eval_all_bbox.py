"""Independent evaluation & regression-audit script for Job 285 bounding-box pipelines.

Loads ground-truth human annotations (CVAT job 285 snapshot JSON) and compares
any prediction JSON against it, computing overall and per-label metrics split by
Day (SANG) vs Night (TOI):
  - Recall, Precision, F1 (at IoU >= threshold, default 0.5)
  - Label accuracy (among IoU >= threshold matches)
  - Mean IoU (box tightness)
  - Edge-truncated object recall (GT boxes touching border <= 5 px)
  - Tiny object recall (GT boxes with area < 32x32 px = 1024 px^2)
  - Latency (s/frame)

Also loads and compares directly against the vehicle baseline computed from
`data/jobs/285/previews/cars/xe_report.csv`.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GT_PATH = ROOT.parent / "tools" / "cvat-seg-copilot" / "frames" / "j285_ann.json"
DEFAULT_BASELINE_PATH = ROOT / "data" / "jobs" / "285" / "previews" / "cars" / "xe_report.csv"

VEHICLES = frozenset({"car", "truck", "bus", "motorcycle", "bicycle"})

# Default Day/Night split for Job 285 (frames 60-79) matching xe_report.csv / cars_first.py
DEFAULT_DAY_NIGHT: dict[int, str] = {
    60: "toi",
    61: "sang",
    62: "toi",
    63: "sang",
    64: "toi",
    65: "toi",
    66: "toi",
    67: "toi",
    68: "toi",
    69: "sang",
    70: "sang",
    71: "sang",
    72: "toi",
    73: "sang",
    74: "toi",
    75: "toi",
    76: "toi",
    77: "sang",
    78: "toi",
    79: "toi",
}


@dataclass(frozen=True)
class Box:
    """Normalized bounding box on a single frame."""

    frame: int
    label: str
    x1: float
    y1: float
    x2: float
    y2: float
    conf: float = 1.0

    @classmethod
    def from_points(
        cls,
        frame: int,
        label: str,
        points: Iterable[float],
        conf: float = 1.0,
    ) -> "Box":
        pts = [float(v) for v in points]
        if len(pts) != 4:
            raise ValueError(f"Expected 4 coordinates for rectangle, got {len(pts)}")
        x1, y1, x2, y2 = min(pts[0], pts[2]), min(pts[1], pts[3]), max(pts[0], pts[2]), max(pts[1], pts[3])
        return cls(frame=int(frame), label=str(label), x1=x1, y1=y1, x2=x2, y2=y2, conf=float(conf))

    @property
    def width(self) -> float:
        return max(0.0, self.x2 - self.x1)

    @property
    def height(self) -> float:
        return max(0.0, self.y2 - self.y1)

    @property
    def area(self) -> float:
        return self.width * self.height

    def is_tiny(self, area_thresh: float = 32.0 * 32.0) -> bool:
        return self.area < area_thresh

    def is_edge_truncated(self, width: int = 1280, height: int = 720, margin_px: float = 5.0) -> bool:
        return (
            self.x1 <= margin_px
            or self.y1 <= margin_px
            or self.x2 >= (width - margin_px)
            or self.y2 >= (height - margin_px)
        )


@dataclass
class MatchRecord:
    frame: int
    gt: Box
    pred: Box
    iou: float

    @property
    def label_correct(self) -> bool:
        return self.gt.label == self.pred.label


@dataclass
class MetricBucket:
    """Aggregated detection metrics for a slice (overall or per-label, in all/sang/toi)."""

    gt_count: int = 0
    pred_count: int = 0
    matched: int = 0
    label_correct: int = 0
    fp: int = 0
    fn: int = 0
    recall: float = 0.0
    precision: float = 0.0
    f1: float = 0.0
    label_accuracy: float = 0.0
    mean_iou: float = 0.0
    edge_gt: int = 0
    edge_matched: int = 0
    edge_recall: float | None = None
    tiny_gt: int = 0
    tiny_matched: int = 0
    tiny_recall: float | None = None
    latency_s_per_frame: float | None = None


@dataclass
class SplitReport:
    """Evaluation report for one lighting split ('all', 'sang', or 'toi')."""

    split: str
    frames: list[int] = field(default_factory=list)
    overall: MetricBucket = field(default_factory=MetricBucket)
    per_label: dict[str, MetricBucket] = field(default_factory=dict)


def compute_iou(a: Box, b: Box) -> float:
    ix1 = max(a.x1, b.x1)
    iy1 = max(a.y1, b.y1)
    ix2 = min(a.x2, b.x2)
    iy2 = min(a.y2, b.y2)
    iw = max(0.0, ix2 - ix1)
    ih = max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0.0:
        return 0.0
    union = a.area + b.area - inter
    return inter / union if union > 0.0 else 0.0


def parse_frames(spec: str) -> list[int]:
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, _, b = part.partition("-")
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return sorted(set(out))


def _extract_label(shape: dict[str, Any], label_map: dict[int, str]) -> str:
    for key in ("label", "_label", "name", "class_name"):
        val = shape.get(key)
        if isinstance(val, str) and val:
            return val
    lid = shape.get("label_id")
    if lid is not None and int(lid) in label_map:
        return label_map[int(lid)]
    raise ValueError(f"Shape missing label information: {shape}")


def _extract_conf(shape: dict[str, Any]) -> float:
    for key in ("_conf", "conf", "confidence", "score"):
        if key in shape and shape[key] is not None:
            return float(shape[key])
    return 1.0


def _parse_label_map(raw: Any) -> dict[int, str]:
    out: dict[int, str] = {}
    if isinstance(raw, dict):
        for k, v in raw.items():
            out[int(k)] = str(v)
    elif isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict) and "id" in item and "name" in item:
                out[int(item["id"])] = str(item["name"])
    return out


def load_boxes_json(
    path: Path | str,
    allowed_labels: set[str] | frozenset[str] | None = None,
    frames: set[int] | None = None,
) -> tuple[list[Box], dict[int, float], dict[int, str]]:
    """Load rectangle boxes and optional per-frame latency / day_night metadata from JSON.

    Supports:
      - List of CVAT-like shape dicts (`j285_ann.json`)
      - Dict with `"shapes"` list (`LATEST_bboxall.json`, `frame71_target.json`, CVAT export)
      - Dict keyed by frame id (`{"60": [...], "61": [...]}` or `{"frames": {...}}`)
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    latencies: dict[int, float] = {}
    day_night: dict[int, str] = {}
    label_map: dict[int, str] = {}
    shapes: list[dict[str, Any]] = []

    if isinstance(data, list):
        shapes = data
    elif isinstance(data, dict):
        label_map = _parse_label_map(data.get("labels"))
        raw_lat = data.get("latencies") or data.get("per_frame_latency") or data.get("latency_by_frame")
        if isinstance(raw_lat, dict):
            latencies = {int(k): float(v) for k, v in raw_lat.items()}
        elif isinstance(data.get("latency_s_per_frame"), (int, float)):
            # Will be applied to all frames if per-frame latencies aren't provided
            latencies = {-1: float(data["latency_s_per_frame"])}

        raw_dn = data.get("sang_toi") or data.get("day_night")
        if isinstance(raw_dn, dict):
            day_night = {int(k): str(v).lower() for k, v in raw_dn.items()}

        if "shapes" in data and isinstance(data["shapes"], list):
            default_frame = data.get("frame")
            for s in data["shapes"]:
                if "frame" not in s and default_frame is not None:
                    s = {**s, "frame": default_frame}
                shapes.append(s)
        elif "frames" in data and isinstance(data["frames"], dict):
            for fkey, items in data["frames"].items():
                for s in items:
                    shapes.append({**s, "frame": int(fkey)})
        else:
            # Frame-keyed dict fallback: {"60": [...], ...}
            for k, v in data.items():
                if str(k).isdigit() and isinstance(v, list):
                    for s in v:
                        shapes.append({**s, "frame": int(k)})
    else:
        raise ValueError(f"Unsupported JSON root type in {path}: {type(data).__name__}")

    boxes: list[Box] = []
    for s in shapes:
        stype = s.get("type", "rectangle")
        if stype != "rectangle":
            continue
        frame = int(s["frame"])
        if frames is not None and frame not in frames:
            continue
        label = _extract_label(s, label_map)
        if allowed_labels is not None and label not in allowed_labels:
            continue
        pts = s.get("points") or s.get("bbox") or s.get("box")
        if pts is None:
            continue
        boxes.append(Box.from_points(frame=frame, label=label, points=pts, conf=_extract_conf(s)))

    return boxes, latencies, day_night


def match_frame_boxes(
    gt_boxes: list[Box],
    pred_boxes: list[Box],
    iou_thresh: float = 0.5,
) -> tuple[list[MatchRecord], list[Box], list[Box]]:
    """Greedy confidence-descending matching on a single frame (IoU >= iou_thresh)."""
    sorted_preds = sorted(enumerate(pred_boxes), key=lambda item: (-item[1].conf, item[0]))
    used_gt: set[int] = set()
    matches: list[MatchRecord] = []
    false_positives: list[Box] = []

    for _, pred in sorted_preds:
        best_iou = 0.0
        best_idx = -1
        for gi, gt in enumerate(gt_boxes):
            if gi in used_gt:
                continue
            score = compute_iou(pred, gt)
            if score > best_iou:
                best_iou = score
                best_idx = gi
        if best_idx >= 0 and best_iou >= iou_thresh:
            used_gt.add(best_idx)
            matches.append(MatchRecord(frame=pred.frame, gt=gt_boxes[best_idx], pred=pred, iou=best_iou))
        else:
            false_positives.append(pred)

    false_negatives = [gt for gi, gt in enumerate(gt_boxes) if gi not in used_gt]
    return matches, false_positives, false_negatives


def _finalize_bucket(
    gt_boxes: list[Box],
    pred_boxes: list[Box],
    matches_for_gt: list[MatchRecord],
    matched_pred_count: int,
    width: int,
    height: int,
    edge_px: float,
    tiny_area: float,
    latency_s_per_frame: float | None,
) -> MetricBucket:
    gt_count = len(gt_boxes)
    pred_count = len(pred_boxes)
    matched = len(matches_for_gt)
    label_correct = sum(1 for m in matches_for_gt if m.label_correct)
    fp = max(0, pred_count - matched_pred_count)
    fn = max(0, gt_count - matched)

    recall = matched / gt_count if gt_count > 0 else 0.0
    precision = matched_pred_count / pred_count if pred_count > 0 else 0.0
    f1 = (2.0 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    label_acc = label_correct / matched if matched > 0 else 0.0
    mean_iou = (sum(m.iou for m in matches_for_gt) / matched) if matched > 0 else 0.0

    matched_gt_ids = {id(m.gt) for m in matches_for_gt}
    edge_gts = [g for g in gt_boxes if g.is_edge_truncated(width=width, height=height, margin_px=edge_px)]
    edge_matched = sum(1 for g in edge_gts if id(g) in matched_gt_ids)
    edge_recall = (edge_matched / len(edge_gts)) if edge_gts else None

    tiny_gts = [g for g in gt_boxes if g.is_tiny(area_thresh=tiny_area)]
    tiny_matched = sum(1 for g in tiny_gts if id(g) in matched_gt_ids)
    tiny_recall = (tiny_matched / len(tiny_gts)) if tiny_gts else None

    return MetricBucket(
        gt_count=gt_count,
        pred_count=pred_count,
        matched=matched,
        label_correct=label_correct,
        fp=fp,
        fn=fn,
        recall=recall,
        precision=precision,
        f1=f1,
        label_accuracy=label_acc,
        mean_iou=mean_iou,
        edge_gt=len(edge_gts),
        edge_matched=edge_matched,
        edge_recall=edge_recall,
        tiny_gt=len(tiny_gts),
        tiny_matched=tiny_matched,
        tiny_recall=tiny_recall,
        latency_s_per_frame=latency_s_per_frame,
    )


def evaluate_predictions(
    gt_boxes: list[Box],
    pred_boxes: list[Box],
    day_night: dict[int, str] | None = None,
    latencies: dict[int, float] | None = None,
    frames: list[int] | None = None,
    iou_thresh: float = 0.5,
    width: int = 1280,
    height: int = 720,
    edge_px: float = 5.0,
    tiny_area: float = 32.0 * 32.0,
) -> dict[str, SplitReport]:
    """Evaluate predictions against ground truth and return 'all', 'sang', and 'toi' reports."""
    dn_map = dict(DEFAULT_DAY_NIGHT)
    if day_night:
        dn_map.update({int(k): str(v).lower() for k, v in day_night.items()})

    gt_by_frame: dict[int, list[Box]] = defaultdict(list)
    pred_by_frame: dict[int, list[Box]] = defaultdict(list)
    for b in gt_boxes:
        gt_by_frame[b.frame].append(b)
    for b in pred_boxes:
        pred_by_frame[b.frame].append(b)

    if frames is None:
        all_frames = sorted(set(gt_by_frame.keys()) | set(pred_by_frame.keys()))
    else:
        all_frames = sorted(set(frames))

    matches_by_frame: dict[int, list[MatchRecord]] = {}
    for f in all_frames:
        m, _, _ = match_frame_boxes(gt_by_frame.get(f, []), pred_by_frame.get(f, []), iou_thresh=iou_thresh)
        matches_by_frame[f] = m

    reports: dict[str, SplitReport] = {}
    for split in ("all", "sang", "toi"):
        split_frames = [f for f in all_frames if split == "all" or dn_map.get(f, "unknown") == split]
        split_gt = [b for f in split_frames for b in gt_by_frame.get(f, [])]
        split_pred = [b for f in split_frames for b in pred_by_frame.get(f, [])]
        split_matches = [m for f in split_frames for m in matches_by_frame.get(f, [])]

        avg_lat: float | None = None
        if latencies and split_frames:
            frame_lats = [latencies[f] for f in split_frames if f in latencies]
            if frame_lats:
                avg_lat = sum(frame_lats) / len(frame_lats)
            elif -1 in latencies:
                avg_lat = latencies[-1]

        overall = _finalize_bucket(
            gt_boxes=split_gt,
            pred_boxes=split_pred,
            matches_for_gt=split_matches,
            matched_pred_count=len(split_matches),
            width=width,
            height=height,
            edge_px=edge_px,
            tiny_area=tiny_area,
            latency_s_per_frame=avg_lat,
        )

        labels = sorted({b.label for b in split_gt} | {b.label for b in split_pred})
        per_label: dict[str, MetricBucket] = {}
        for lab in labels:
            l_gt = [b for b in split_gt if b.label == lab]
            l_pred = [b for b in split_pred if b.label == lab]
            l_matches_gt = [m for m in split_matches if m.gt.label == lab]
            l_matched_pred = sum(1 for m in split_matches if m.pred.label == lab)
            per_label[lab] = _finalize_bucket(
                gt_boxes=l_gt,
                pred_boxes=l_pred,
                matches_for_gt=l_matches_gt,
                matched_pred_count=l_matched_pred,
                width=width,
                height=height,
                edge_px=edge_px,
                tiny_area=tiny_area,
                latency_s_per_frame=avg_lat,
            )

        reports[split] = SplitReport(
            split=split,
            frames=split_frames,
            overall=overall,
            per_label=per_label,
        )

    return reports


def load_xe_report_baseline(csv_path: Path | str) -> tuple[dict[str, MetricBucket], dict[int, str]]:
    """Compute baseline metrics directly from `xe_report.csv` for all, sang, and toi."""
    rows: list[dict[str, str]] = []
    with open(csv_path, "r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    day_night: dict[int, str] = {}
    for r in rows:
        day_night[int(r["frame"])] = r["sang_toi"].strip().lower()

    baseline: dict[str, MetricBucket] = {}
    for split in ("all", "sang", "toi"):
        sub = [r for r in rows if split == "all" or r["sang_toi"].strip().lower() == split]
        gt = sum(int(r["hop_nguoi"]) for r in sub)
        pred = sum(int(r["hop_may"]) for r in sub)
        matched = sum(int(r["khop_IoU0.5"]) for r in sub)
        label_ok = sum(int(r["dung_nhan"]) for r in sub)
        fp = sum(int(r["may_thua"]) for r in sub)
        fn = sum(int(r["may_bo_sot"]) for r in sub)
        recall = matched / gt if gt > 0 else 0.0
        precision = matched / pred if pred > 0 else 0.0
        f1 = (2.0 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        label_acc = label_ok / matched if matched > 0 else 0.0
        avg_lat = (sum(float(r["giay"]) for r in sub) / len(sub)) if sub else None

        baseline[split] = MetricBucket(
            gt_count=gt,
            pred_count=pred,
            matched=matched,
            label_correct=label_ok,
            fp=fp,
            fn=fn,
            recall=recall,
            precision=precision,
            f1=f1,
            label_accuracy=label_acc,
            mean_iou=0.0,  # Not recorded in xe_report.csv
            latency_s_per_frame=avg_lat,
        )
    return baseline, day_night


def _fmt_pct(val: float | None) -> str:
    return f"{val * 100:.1f}%" if val is not None else "n/a"


def _fmt_lat(val: float | None) -> str:
    return f"{val:.2f}s" if val is not None else "n/a"


def format_report(
    reports: dict[str, SplitReport] | None,
    baseline: dict[str, MetricBucket] | None,
) -> str:
    lines: list[str] = []
    if baseline is not None:
        lines.append("=== BASELINE (xe_report.csv - Vehicles Only) ===")
        lines.append(
            f"{'Split':<6} {'GT':>5} {'Pred':>5} {'Match':>5} {'LblOK':>5} "
            f"{'Recall':>8} {'Prec':>8} {'F1':>8} {'LblAcc':>8} {'Lat/f':>7}"
        )
        for split in ("all", "sang", "toi"):
            b = baseline[split]
            lines.append(
                f"{split.upper():<6} {b.gt_count:>5} {b.pred_count:>5} {b.matched:>5} {b.label_correct:>5} "
                f"{_fmt_pct(b.recall):>8} {_fmt_pct(b.precision):>8} {_fmt_pct(b.f1):>8} "
                f"{_fmt_pct(b.label_accuracy):>8} {_fmt_lat(b.latency_s_per_frame):>7}"
            )

    if reports is not None:
        for split in ("all", "sang", "toi"):
            rep = reports[split]
            o = rep.overall
            lines.append("")
            lines.append(f"=== EVALUATION [{split.upper()}] ({len(rep.frames)} frames) ===")
            lines.append(
                f"Overall: GT={o.gt_count} Pred={o.pred_count} Match={o.matched} LblOK={o.label_correct} "
                f"FP={o.fp} FN={o.fn} | Recall={_fmt_pct(o.recall)} Prec={_fmt_pct(o.precision)} "
                f"F1={_fmt_pct(o.f1)} LblAcc={_fmt_pct(o.label_accuracy)} mIoU={o.mean_iou:.3f} | "
                f"EdgeRec={_fmt_pct(o.edge_recall)} ({o.edge_matched}/{o.edge_gt}) | "
                f"TinyRec={_fmt_pct(o.tiny_recall)} ({o.tiny_matched}/{o.tiny_gt}) | "
                f"Lat={_fmt_lat(o.latency_s_per_frame)}"
            )
            if baseline is not None and split in baseline:
                b = baseline[split]
                d_rec = (o.recall - b.recall) * 100
                d_prec = (o.precision - b.precision) * 100
                d_f1 = (o.f1 - b.f1) * 100
                d_acc = (o.label_accuracy - b.label_accuracy) * 100
                d_lat = (
                    f"{o.latency_s_per_frame - b.latency_s_per_frame:+.2f}s"
                    if o.latency_s_per_frame is not None and b.latency_s_per_frame is not None
                    else "n/a"
                )
                lines.append(
                    f"vs xe_report.csv: dRecall={d_rec:+.1f}pp dPrec={d_prec:+.1f}pp "
                    f"dF1={d_f1:+.1f}pp dLblAcc={d_acc:+.1f}pp dLat={d_lat}"
                )

            if rep.per_label:
                lines.append(
                    f"{'Label':<16} {'GT':>4} {'Pred':>4} {'Match':>5} {'Rec':>7} {'Prec':>7} "
                    f"{'F1':>7} {'LblAcc':>7} {'mIoU':>6} {'EdgeRec':>11} {'TinyRec':>11}"
                )
                for lab, m in rep.per_label.items():
                    edge_str = f"{_fmt_pct(m.edge_recall)}({m.edge_matched}/{m.edge_gt})" if m.edge_gt else "n/a"
                    tiny_str = f"{_fmt_pct(m.tiny_recall)}({m.tiny_matched}/{m.tiny_gt})" if m.tiny_gt else "n/a"
                    lines.append(
                        f"{lab:<16} {m.gt_count:>4} {m.pred_count:>4} {m.matched:>5} "
                        f"{_fmt_pct(m.recall):>7} {_fmt_pct(m.precision):>7} {_fmt_pct(m.f1):>7} "
                        f"{_fmt_pct(m.label_accuracy):>7} {m.mean_iou:>6.3f} {edge_str:>11} {tiny_str:>11}"
                    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    ap = argparse.ArgumentParser(description="Independent Job 285 BBox Evaluation & Regression Auditor")
    ap.add_argument("--gt", type=Path, default=DEFAULT_GT_PATH, help="Ground truth snapshot JSON path")
    ap.add_argument("--pred", type=Path, default=None, help="Prediction JSON path")
    ap.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE_PATH, help="xe_report.csv baseline path")
    ap.add_argument("--iou", type=float, default=0.5, help="IoU threshold for matching (default 0.5)")
    ap.add_argument("--width", type=int, default=1280, help="Frame width in pixels")
    ap.add_argument("--height", type=int, default=720, help="Frame height in pixels")
    ap.add_argument("--edge-px", type=float, default=5.0, help="Border margin px for edge-truncated boxes")
    ap.add_argument("--tiny-area", type=float, default=1024.0, help="Area threshold px^2 for tiny boxes (32x32=1024)")
    ap.add_argument("--labels", type=str, default=None, help="Comma-separated label filter, or 'vehicles'")
    ap.add_argument("--frames", type=str, default=None, help="Frame filter, e.g. '60-79'")
    ap.add_argument("--baseline-only", action="store_true", help="Only print xe_report.csv baseline")
    ap.add_argument("--out-json", type=Path, default=None, help="Optional path to save JSON report")
    args = ap.parse_args(argv)

    allowed_labels: set[str] | frozenset[str] | None = None
    if args.labels:
        if args.labels.strip().lower() == "vehicles":
            allowed_labels = VEHICLES
        else:
            allowed_labels = {s.strip() for s in args.labels.split(",") if s.strip()}

    frame_list = parse_frames(args.frames) if args.frames else None
    frame_set = set(frame_list) if frame_list is not None else None

    baseline: dict[str, MetricBucket] | None = None
    day_night = dict(DEFAULT_DAY_NIGHT)
    if args.baseline and args.baseline.exists():
        baseline, csv_dn = load_xe_report_baseline(args.baseline)
        day_night.update(csv_dn)

    reports: dict[str, SplitReport] | None = None
    if not args.baseline_only:
        if args.pred is None:
            ap.error("--pred is required unless --baseline-only is specified")
        if not args.gt.exists():
            ap.error(f"Ground truth JSON not found: {args.gt}")
        gt_boxes, _, gt_dn = load_boxes_json(args.gt, allowed_labels=allowed_labels, frames=frame_set)
        pred_boxes, latencies, pred_dn = load_boxes_json(args.pred, allowed_labels=allowed_labels, frames=frame_set)
        day_night.update(gt_dn)
        day_night.update(pred_dn)
        reports = evaluate_predictions(
            gt_boxes=gt_boxes,
            pred_boxes=pred_boxes,
            day_night=day_night,
            latencies=latencies,
            frames=frame_list,
            iou_thresh=args.iou,
            width=args.width,
            height=args.height,
            edge_px=args.edge_px,
            tiny_area=args.tiny_area,
        )

    print(format_report(reports, baseline))

    if args.out_json:
        payload: dict[str, Any] = {}
        if baseline is not None:
            payload["baseline"] = {k: asdict(v) for k, v in baseline.items()}
        if reports is not None:
            payload["evaluation"] = {
                split: {
                    "split": rep.split,
                    "frames": rep.frames,
                    "overall": asdict(rep.overall),
                    "per_label": {lab: asdict(b) for lab, b in rep.per_label.items()},
                }
                for split, rep in reports.items()
            }
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
