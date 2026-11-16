"""Tải frame của các job CVAT (chỉ đọc) và ghép thành contact sheet có nhãn frame, để khảo sát edge case.

  python scripts/make_contact_sheets.py --jobs 1972 1973 1974 1975 1976 --profile edufun --out data/jobs/edufun/task473/sheets
  python scripts/make_contact_sheets.py --jobs 1623 --profile edufun --out data/jobs/edufun/1623/sheets --cols 3 --rows 2 --tile 420

Frame gốc lưu cache ở <out>/../frames/. Mặc định 4 cột × 3 hàng, tile rộng 320 px.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cvat_tools.core.client import Cvat  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, nargs="+", required=True); ap.add_argument("--profile", default="edufun")
    ap.add_argument("--out", required=True); ap.add_argument("--cols", type=int, default=4); ap.add_argument("--rows", type=int, default=3)
    ap.add_argument("--tile", type=int, default=320)
    a = ap.parse_args()
    c = Cvat.from_env(a.profile)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    cache = out.parent / "frames"; cache.mkdir(exist_ok=True)
    tiles = []
    for jid in a.jobs:
        j, meta = c.job(jid), c.meta(jid)["frames"]
        for i, mf in enumerate(meta):
            n = j["start_frame"] + i
            f = cache / f"{mf['name'].split('/')[-1]}"
            if not f.exists():
                f.write_bytes(c.frame(jid, n))
            im = cv2.imdecode(np.fromfile(str(f), np.uint8), cv2.IMREAD_COLOR)
            h = int(im.shape[0] * a.tile / im.shape[1])
            im = cv2.resize(im, (a.tile, h))
            label = f"f{n} {f.stem}"
            cv2.rectangle(im, (0, 0), (a.tile, 18), (0, 0, 0), -1)
            cv2.putText(im, label, (4, 13), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
            tiles.append(im)
    per = a.cols * a.rows
    for s in range(0, len(tiles), per):
        chunk = tiles[s:s + per]
        H = max(t.shape[0] for t in chunk)
        chunk = [cv2.copyMakeBorder(t, 0, H - t.shape[0], 0, 0, cv2.BORDER_CONSTANT) for t in chunk]
        while len(chunk) < per:
            chunk.append(np.zeros_like(chunk[0]))
        sheet = np.vstack([np.hstack(chunk[r * a.cols:(r + 1) * a.cols]) for r in range(a.rows)])
        p = out / f"sheet_{s // per + 1:02d}.jpg"
        cv2.imwrite(str(p), sheet, [cv2.IMWRITE_JPEG_QUALITY, 88]); print(p)


if __name__ == "__main__":
    main()
