"""Ve overlay skeleton (diem + so thu tu + canh) len frame cua 1 job CVAT, de doc/khao sat guideline. Chi doc CVAT.

  python scripts/render_skeleton_overlay.py --job 1975 --profile edufun --frames 91 97 --out data/jobs/edufun/1975/overlay
  python scripts/render_skeleton_overlay.py --job 1975 --profile edufun --template   # ve khung mau cua tung label
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cvat_tools.core.client import Cvat  # noqa: E402


def _hex(c: str):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (4, 2, 0))  # BGR


def _edges(svg: str):
    return [(int(a), int(b)) for a, b in re.findall(r'data-node-from="(\d+)" data-node-to="(\d+)"', svg)]


def _template_nodes(svg: str):
    return {int(e): (float(x), float(y)) for x, y, e in re.findall(r'cx="([\d.]+)" cy="([\d.]+)"[^>]*data-element-id="(\d+)"', svg)} or \
           {int(e): (float(x), float(y)) for e, x, y in re.findall(r'data-element-id="(\d+)"[^>]*cx="([\d.]+)" cy="([\d.]+)"', svg)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", type=int, required=True); ap.add_argument("--profile", default="edufun")
    ap.add_argument("--frames", type=int, nargs="*", default=[]); ap.add_argument("--out", default=None)
    ap.add_argument("--template", action="store_true"); ap.add_argument("--scale", type=float, default=1.0)
    a = ap.parse_args()
    c = Cvat.from_env(a.profile)
    labs = c.labels(a.job)
    out = Path(a.out or f"data/jobs/{a.profile}/{a.job}/overlay"); out.mkdir(parents=True, exist_ok=True)
    if a.template:
        S = 8; img = np.full((100 * S, 100 * S, 3), 255, np.uint8)
        for l in labs:
            col = _hex(l["color"]); nodes = _template_nodes(l["svg"]); sub = {i + 1: s["name"] for i, s in enumerate(l["sublabels"])}
            for u, v in _edges(l["svg"]):
                cv2.line(img, tuple(int(k * S) for k in nodes[u]), tuple(int(k * S) for k in nodes[v]), col, 1)
            for i, (x, y) in nodes.items():
                cv2.circle(img, (int(x * S), int(y * S)), 4, col, -1)
                cv2.putText(img, f"{sub.get(i, i)}", (int(x * S) + 5, int(y * S) - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        cv2.imwrite(str(out / "template.png"), img); print(out / "template.png")
    if a.frames:
        ann = c.annotations(a.job); start = c.job(a.job)["start_frame"]
        names = {l["id"]: l["name"] for l in labs}; subn = {s["id"]: s["name"] for l in labs for s in l["sublabels"]}
        colors = {l["id"]: _hex(l["color"]) for l in labs}
        for fr in a.frames:
            im = cv2.imdecode(np.frombuffer(c.frame(a.job, fr), np.uint8), cv2.IMREAD_COLOR)
            for sh in (s for s in ann["shapes"] if s["frame"] == fr):
                col = colors[sh["label_id"]]
                for e in sh["elements"]:
                    x, y = e["points"]; cv2.circle(im, (int(x), int(y)), 3, col, -1)
                    cv2.putText(im, subn.get(e["label_id"], "?"), (int(x) + 3, int(y) - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.35, col, 1)
            if a.scale != 1.0:
                im = cv2.resize(im, None, fx=a.scale, fy=a.scale)
            cv2.imwrite(str(out / f"frame_{fr}.png"), im); print(out / f"frame_{fr}.png")


if __name__ == "__main__":
    main()
