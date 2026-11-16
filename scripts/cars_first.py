"""Bước 1 của quy trình theo từng nhãn: XE (car/truck/bus/motorcycle) trước, đo và xuất ảnh để người dùng xem.

  python scripts/cars_first.py --job 285 [--frames 60-79]

Khác bbox_draft.py: KHÔNG bỏ hộp trùng hộp tay. Hiện đủ đầu ra của máy để so với hộp người vẽ.
  xanh lá = máy và người khớp (IoU>=0.5) | đỏ = chỉ máy có (thừa hoặc xe người chưa vẽ)
  vàng = chỉ người vẽ (máy bỏ sót)
Chỉ ĐỌC CVAT (hộp người). Không ghi CVAT. Dùng lại detect() của tools/cvat-seg-copilot (chỉ import, không sửa).
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

import cv2
import numpy as np

REPO = Path(__file__).resolve().parents[2]
COPILOT = REPO / "tools" / "cvat-seg-copilot"
sys.path[:0] = [str(COPILOT / "src"), str(COPILOT / "scripts")]
sys.stdout.reconfigure(encoding="utf-8")

VEHICLES = ("car", "truck", "bus", "motorcycle", "bicycle")
OUT = REPO / "cvat" / "data" / "jobs" / "285" / "previews" / "cars"


def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    i = ix * iy
    u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i
    return i / u if u > 0 else 0.0


def parse_frames(s):
    a, _, b = s.partition("-")
    return list(range(int(a), int(b or a) + 1))


def keep_box(label, box, conf):
    """Cùng bộ lọc với bbox_draft: bỏ tâm ở đáy ảnh (phản chiếu capo), hộp quá nhỏ/quá to."""
    bw, bh = box[2] - box[0], box[3] - box[1]
    if (box[1] + box[3]) / 2 > 0.88 * 720 and label != "traffic light":
        return False
    return not (bw < 10 or bh < 10 or (bw * bh > 0.2 * 1280 * 720 and conf < 0.6))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", type=int, default=285)
    ap.add_argument("--frames", default="60-79")
    ap.add_argument("--conf", type=float, default=0.25)
    ap.add_argument("--night-conf", type=float, default=0.2)
    ap.add_argument("--imgsz", type=int, default=1280)
    a = ap.parse_args()
    from bbox_draft import detect  # noqa: E402  (import chỉ lấy hàm, không chạy main)
    from cvat_seg.cli import get_adapter  # noqa: E402
    from ultralytics import YOLO  # noqa: E402

    ad = get_adapter()
    names = {l["id"]: l["name"] for l in ad.get_job_labels(a.job)}
    human: dict[int, list] = {}
    for s in ad.get_annotations(a.job)["shapes"]:
        if s["type"] == "rectangle" and names[s["label_id"]] in VEHICLES:
            human.setdefault(s["frame"], []).append((names[s["label_id"]], s["points"]))
    yolo = YOLO(str(COPILOT / "yolo26l-seg.pt"))
    OUT.mkdir(parents=True, exist_ok=True)
    rows, thumbs = [], []
    for f in parse_frames(a.frames):
        p = COPILOT / "frames" / f"j{a.job}_f{f}.jpg"
        img = cv2.imread(str(p)) if p.exists() else cv2.imdecode(np.frombuffer(ad.get_frame_image_bytes(a.job, f), np.uint8), 1)
        night = float(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).mean()) < 70
        t0 = time.time()
        dets = [d for d in detect(yolo, img, a.night_conf if night else a.conf, a.imgsz, True)
                if d[0] in VEHICLES and keep_box(*d[:2], d[2])]
        sec = time.time() - t0
        hum = human.get(f, [])
        used, matched, extra = set(), [], []
        for lab, b, c in sorted(dets, key=lambda d: -d[2]):
            best = max(((iou(b, h[1]), i) for i, h in enumerate(hum) if i not in used), default=(0, -1))
            if best[0] >= 0.5:
                used.add(best[1]); matched.append((lab, b, c, hum[best[1]][0]))
            else:
                extra.append((lab, b, c))
        missed = [h for i, h in enumerate(hum) if i not in used]
        vis = img.copy()
        for lab, b, c, hl in matched:
            cv2.rectangle(vis, tuple(map(int, b[:2])), tuple(map(int, b[2:])), (0, 200, 0), 2)
        for lab, b, c in extra:
            cv2.rectangle(vis, tuple(map(int, b[:2])), tuple(map(int, b[2:])), (0, 0, 255), 2)
            cv2.putText(vis, f"{lab} {c:.2f}", (int(b[0]) + 2, int(b[1]) + 14), 0, 0.45, (0, 0, 255), 1, cv2.LINE_AA)
        for lab, b in missed:
            cv2.rectangle(vis, tuple(map(int, b[:2])), tuple(map(int, b[2:])), (0, 255, 255), 2)
            cv2.putText(vis, f"nguoi:{lab}", (int(b[0]) + 2, int(b[1]) + 14), 0, 0.45, (0, 200, 255), 1, cv2.LINE_AA)
        title = (f"f{f} {'TOI' if night else 'SANG'} | khop {len(matched)}  thua(do) {len(extra)}  "
                 f"bo sot(vang) {len(missed)} | nguoi {len(hum)}  {sec:.1f}s")
        cv2.rectangle(vis, (0, 0), (1280, 30), (255, 255, 255), -1)
        cv2.putText(vis, title, (8, 22), 0, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.imwrite(str(OUT / f"f{f}_xe.jpg"), vis)
        thumbs.append(cv2.resize(vis, (640, 360)))
        label_ok = sum(1 for m in matched if m[0] == m[3])
        rows.append([f, "toi" if night else "sang", len(hum), len(dets), len(matched), label_ok, len(extra), len(missed), round(sec, 1)])
        print(rows[-1], flush=True)
    with open(OUT / "xe_report.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["frame", "sang_toi", "hop_nguoi", "hop_may", "khop_IoU0.5", "dung_nhan", "may_thua", "may_bo_sot", "giay"])
        w.writerows(rows)
    cols = 4
    while len(thumbs) % cols:
        thumbs.append(np.full_like(thumbs[0], 255))
    cv2.imwrite(str(OUT / "xe_contact_sheet.jpg"), np.vstack([np.hstack(thumbs[i:i + cols]) for i in range(0, len(thumbs), cols)]))
    tot = np.array([r[2:8] for r in rows]).sum(0)
    print(f"TỔNG: hộp người {tot[0]} | máy {tot[1]} | khớp {tot[2]} (đúng nhãn {tot[3]}) | máy thừa {tot[4]} | máy bỏ sót {tot[5]}")
    print(f"recall = {tot[2] / max(1, tot[0]):.0%} | precision = {tot[2] / max(1, tot[1]):.0%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
