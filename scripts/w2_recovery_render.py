"""Render so sánh nhiều phiên bản annotation trên 1 frame (crop phóng to quanh vùng điểm). Chỉ đọc file local.

  python -X utf8 scripts/w2_recovery_render.py --job 1975 --frame 91 --ver live --ver draft:face50_20261117_111604 --out x.png
`--ver` khớp theo tiền tố tên phiên bản trong w2_recovery_compare.versions (lấy bản cuối cùng khớp). `raw` = ảnh gốc không điểm.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")
import w2_recovery_compare as w  # noqa: E402

PALETTE = ["#ff3b30", "#0a84ff", "#34c759", "#ff9f0a", "#bf5af2", "#00c7be", "#ff2d92"]
FONT = "C:/Windows/Fonts/arialbd.ttf"


def frame_path(job: int, frame: int) -> Path:
    cands = sorted((ROOT / f"data/jobs/edufun/{job}/frames").glob(f"*_{frame + 1:03d}.jpg"))
    if not cands:
        raise SystemExit(f"không có ảnh frame {frame} job {job}")
    return cands[0]


def pick(V: dict, key: str):
    ms = [n for n in V if n.startswith(key) or n.split(":", 1)[-1].startswith(key)]
    return V[ms[-1]] if ms else None, (ms[-1] if ms else key)


def render(job: int, frame: int, vers: list[str], out: Path, scale: int = 5, labels: bool = True, pad: int = 24, box=None) -> None:
    V = w.versions(job)
    img0 = Image.open(frame_path(job, frame)).convert("RGB")
    sets = []
    for k in vers:
        if k == "raw":
            sets.append((k, None))
            continue
        v, name = pick(V, k)
        sets.append((name, (v or {}).get(frame)))
    pts = [(p[0], p[1]) for _, s in sets if s for sk in s.values() for kk, p in sk.items() if kk != "_source"]
    if box:
        x0, y0, x1, y1 = box
    elif pts:
        xs, ys = zip(*pts)
        x0, y0, x1, y1 = min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad
    else:
        x0, y0, x1, y1 = 0, 0, img0.width, img0.height
    x0, y0 = max(0, int(x0)), max(0, int(y0))
    x1, y1 = min(img0.width, int(x1)), min(img0.height, int(y1))
    sc = max(1, min(scale, 700 // max(1, (x1 - x0)), 700 // max(1, (y1 - y0))))
    tiles = []
    f = ImageFont.truetype(FONT, 13)
    for name, s in sets:
        im = img0.crop((x0, y0, x1, y1)).resize(((x1 - x0) * sc, (y1 - y0) * sc), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        if s:
            for ci, (lab, sk) in enumerate(sorted(s.items())):
                col = PALETTE[ci % len(PALETTE)]
                for kk, p in sk.items():
                    if kk == "_source":
                        continue
                    X, Y = (p[0] - x0) * sc, (p[1] - y0) * sc
                    r = 4
                    if p[3]:
                        d.line([X - r, Y - r, X + r, Y + r], fill=col, width=2)
                        d.line([X - r, Y + r, X + r, Y - r], fill=col, width=2)
                    else:
                        d.ellipse([X - r, Y - r, X + r, Y + r], outline=col, width=2 if not p[2] else 1)
                    if labels:
                        d.text((X + 5, Y - 6), kk, fill=col, font=f, stroke_width=2, stroke_fill="white")
        bar = Image.new("RGB", (im.width, 22), "white")
        ImageDraw.Draw(bar).text((4, 3), f"{name}"[:60], fill="black", font=f)
        t = Image.new("RGB", (im.width, im.height + 22), "white")
        t.paste(bar, (0, 0))
        t.paste(im, (0, 22))
        tiles.append(t)
    W = sum(t.width for t in tiles) + 6 * (len(tiles) - 1)
    H = max(t.height for t in tiles)
    canvas = Image.new("RGB", (W, H), "#888")
    x = 0
    for t in tiles:
        canvas.paste(t, (x, 0))
        x += t.width + 6
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    print(out, canvas.size, "crop", (x0, y0, x1, y1), "scale", sc)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", type=int, required=True)
    ap.add_argument("--frame", type=int, required=True)
    ap.add_argument("--ver", action="append", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--scale", type=int, default=5)
    ap.add_argument("--no-labels", action="store_true")
    ap.add_argument("--box", type=int, nargs=4)
    a = ap.parse_args()
    render(a.job, a.frame, a.ver, a.out, a.scale, not a.no_labels, box=a.box)
