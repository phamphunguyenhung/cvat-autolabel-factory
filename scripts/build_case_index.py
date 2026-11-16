"""Biến bảng nhóm edge case (EDGE_CASES.md của task) thành chỉ mục theo TỪNG frame: cases.json + cases_by_frame.md.

  python scripts/build_case_index.py --md week02/task473-face/EDGE_CASES.md --out week02/task473-face --frames 150

Dòng bảng: `| Tên nhóm | f5, f8, f13–f16, f7? |` ; dấu `?` = chưa chắc (ghi `uncertain`).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def parse_frames(cell: str):
    out = []
    for tok in re.split(r"[,;]\s*", cell.strip()):
        m = re.fullmatch(r"f(\d+)(?:[–-]f?(\d+))?(\?)?", tok.strip())
        if not m:
            continue
        a, b, q = int(m.group(1)), int(m.group(2) or m.group(1)), bool(m.group(3))
        out += [(n, q) for n in range(a, b + 1)]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True); ap.add_argument("--out", required=True); ap.add_argument("--frames", type=int, default=150)
    a = ap.parse_args()
    idx: dict[int, list] = {n: [] for n in range(a.frames)}
    for line in Path(a.md).read_text(encoding="utf8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 2 or cells[0] in ("Nhóm", "---") or cells[1].startswith("---"):
            continue
        for n, q in parse_frames(cells[1]):
            if n in idx:
                idx[n].append({"case": cells[0], "uncertain": q})
    out = Path(a.out)
    (out / "cases.json").write_text(json.dumps({str(k): v for k, v in idx.items()}, ensure_ascii=False, indent=1), encoding="utf8")
    rows = ["# Edge case theo từng frame (sinh tự động từ EDGE_CASES.md, không sửa tay)\n",
            "`?` = chưa chắc. Frame không có nhóm nào = ảnh bình thường.\n", "| Frame | File | Trường hợp |", "|---|---|---|"]
    for n, cs in idx.items():
        text = "; ".join(c["case"] + ("?" if c["uncertain"] else "") for c in cs) or "bình thường"
        rows.append(f"| f{n} | G06_{n + 1:03d} | {text} |")
    (out / "cases_by_frame.md").write_text("\n".join(rows) + "\n", encoding="utf8")
    print(f"{sum(1 for v in idx.values() if v)}/{a.frames} frame có ít nhất một trường hợp")


if __name__ == "__main__":
    main()
