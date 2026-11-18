"""Tạo ảnh review cho một trường hợp cần người duyệt (chỉ đọc, không ghi CVAT).

Ảnh gồm: toàn khung (trái) + vùng phóng to (phải), annotation hiện tại, điểm cần chú ý được tô đậm,
tiêu đề, vấn đề ngắn, và tối đa 3 lựa chọn A/B/C. Mọi điểm chưa chắc chắn ghi IN ĐẬM.

  python -X utf8 scripts/w2_review_image.py --job 1623 --frame 101 --out reports/W2_FINAL_REVIEW/REVIEW_02.png \
      --tag "UNCERTAIN - MISSING LANDMARK" --problem "..." --focus 2 4 --opt A="..." --opt B="..." --opt C="..."
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")

POSE_EDGES = [(6, 8), (8, 10), (7, 9), (9, 11), (6, 7), (6, 12), (7, 13), (12, 13), (12, 14), (14, 16), (13, 15), (15, 17),
              (1, 2), (1, 3), (2, 4), (3, 5)]
FONT = "C:/Windows/Fonts/arial.ttf"
FONT_B = "C:/Windows/Fonts/arialbd.ttf"


def load_points(job: int, frame: int):
    data = json.loads((ROOT / "reports" / "w2_current" / f"job{job}.json").read_text(encoding="utf8"))
    return data["frames"].get(str(frame), {})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", type=int, required=True)
    ap.add_argument("--frame", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--tag", required=True, help="Nhãn in đậm, ví dụ: UNCERTAIN - LEFT/RIGHT")
    ap.add_argument("--problem", required=True)
    ap.add_argument("--focus", nargs="*", default=[], help="Tên điểm cần tô đậm, ví dụ 2 4 (pose) hoặc 30 31 (face)")
    ap.add_argument("--opt", action="append", default=[], help="A=..., B=..., C=... (tối đa 3)")
    a = ap.parse_args()

    img_path = ROOT / "data" / "jobs" / "edufun" / str(a.job) / "frames" / f"G06_{a.frame + 1:03d}.jpg"
    base = Image.open(img_path).convert("RGB")
    W, H = base.size
    pts = load_points(a.job, a.frame)
    overlay = base.copy()
    d = ImageDraw.Draw(overlay)

    all_pts = []
    for skel, plist in pts.items():
        for name, v in plist.items():
            all_pts.append((name, skel, v))

    if a.job == 1623:
        person = pts.get("person_vf17", {})
        for p, q in POSE_EDGES:
            u, v = person.get(str(p)), person.get(str(q))
            if u and v and not u["outside"] and not v["outside"]:
                d.line([(u["x"], u["y"]), (v["x"], v["y"])], fill=(60, 120, 255), width=max(2, W // 400))
    r = max(3, W // 220)
    for name, skel, v in all_pts:
        focus = name in a.focus
        col = (255, 0, 0) if focus else ((255, 170, 0) if v["outside"] else (0, 200, 90))
        rr = r * (2 if focus else 1)
        d.ellipse([v["x"] - rr, v["y"] - rr, v["x"] + rr, v["y"] + rr], fill=col, outline=(0, 0, 0))
        if focus or a.job == 1975 and W < 2000:
            d.text((v["x"] + rr + 2, v["y"] - rr), name, fill=(255, 255, 0), font=ImageFont.truetype(FONT_B, max(12, W // 80)))

    # vùng phóng to quanh điểm cần chú ý, hoặc toàn skeleton nếu không có điểm nào
    sel = [v for name, _, v in all_pts if name in a.focus] or [v for _, _, v in all_pts]
    if sel:
        xs = [v["x"] for v in sel]; ys = [v["y"] for v in sel]
        pad = max(60, (max(xs) - min(xs) + max(ys) - min(ys)) * 0.25)
        box = (max(0, min(xs) - pad), max(0, min(ys) - pad), min(W, max(xs) + pad), min(H, max(ys) + pad))
    else:
        box = (0, 0, W, H)
    crop = overlay.crop(tuple(int(round(b)) for b in box))
    scale = min(640 / crop.width, 640 / crop.height)
    crop = crop.resize((int(crop.width * scale), int(crop.height * scale)), Image.LANCZOS)
    full = overlay.copy()
    full.thumbnail((700, 700), Image.LANCZOS)

    header_h = 200
    canvas = Image.new("RGB", (full.width + crop.width + 60, max(full.height, crop.height) + header_h + 40), (255, 255, 255))
    canvas.paste(full, (20, header_h + 20))
    canvas.paste(crop, (full.width + 40, header_h + 20))
    dr = ImageDraw.Draw(canvas)
    f_b = ImageFont.truetype(FONT_B, 30)
    f_m = ImageFont.truetype(FONT, 20)
    f_s = ImageFont.truetype(FONT_B, 22)
    dr.text((20, 14), a.tag.upper(), fill=(200, 0, 0), font=f_b)
    dr.text((20, 56), f"Job {a.job} · Frame {a.frame} (file G06_{a.frame + 1:03d}.jpg)", fill=(0, 0, 0), font=f_s)
    dr.text((20, 90), a.problem, fill=(0, 0, 0), font=f_m)
    y = 124
    for o in a.opt[:3]:
        dr.text((20, y), o, fill=(0, 0, 0), font=f_m)
        y += 26
    dr.text((full.width + 40, header_h - 6), "Vùng phóng to (điểm đỏ = cần chú ý)", fill=(60, 60, 60), font=f_m)
    dr.text((20, canvas.height - 26), "NEEDS HUMAN DECISION. Ảnh là đề xuất để xem, không phải ground truth.", fill=(200, 0, 0), font=f_s)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(a.out)
    print(f"saved {a.out} {canvas.size}")


if __name__ == "__main__":
    main()
