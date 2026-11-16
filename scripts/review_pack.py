"""Sinh review pack cho nhap job (chi doc nhap + anh cache; khong ghi CVAT, khong ghi de nhap).

  python scripts/review_pack.py --frames 61,63,69
  python scripts/review_pack.py --frames 61 --apply edits.json     # ap dung lenh sua -> ban sua rieng + validate lai
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import cv2  # noqa: E402

from cvat_tools.review import apply as A  # noqa: E402
from cvat_tools.review import pack as P  # noqa: E402
from cvat_tools.review import validators as V  # noqa: E402

DRAFTS = ROOT / "week01" / "job285-bbox" / "drafts"
FRAMES = ROOT.parent / "tools" / "cvat-seg-copilot" / "frames"      # j285_f<N>.jpg (chi doc)
DEFAULT_DRAFTS = ["bboxfull", "bboxbright", "bboxbright2", "bboxbright3", "lanearea", "lanearea61"]


def load_frame_shapes(names, frame, rs):
    raw = []
    for n in names:
        f = Path(n) if Path(n).suffix else DRAFTS / f"LATEST_{n}.json"
        raw += [s for s in json.loads(f.read_text(encoding="utf8")).get("shapes", []) if s.get("_label")]
    return V.shapes_from_draft(raw, frame=frame, rs=rs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", type=int, default=285)
    ap.add_argument("--frames", default="61,63,69")
    ap.add_argument("--drafts", default=",".join(DEFAULT_DRAFTS), help="ten LATEST_<ten>.json hoac duong dan, phay")
    ap.add_argument("--frames-dir", default=str(FRAMES))
    ap.add_argument("--out", default=str(ROOT / "data" / "jobs" / "285" / "previews" / "review"))
    ap.add_argument("--max-shapes", type=int, default=12)
    ap.add_argument("--apply", default="", help="file JSON lenh sua (list); ghi ban sua vao <out>/edited")
    ap.add_argument("--snap", type=float, default=None, help="dai bam canh mac dinh sau moi lenh doi hinh (px)")
    a = ap.parse_args()
    rs = V.load_ruleset(a.job)
    names = [x for x in a.drafts.split(",") if x]
    total: dict = {}
    for fr in [int(x) for x in a.frames.split(",")]:
        img = cv2.imread(str(Path(a.frames_dir) / f"j{a.job}_f{fr}.jpg"))
        if img is None:
            print(f"frame {fr}: thieu anh", file=sys.stderr)
            continue
        shapes = load_frame_shapes(names, fr, rs)
        if a.apply:
            cmds = json.loads(Path(a.apply).read_text(encoding="utf8"))
            res = A.apply_edits(shapes, cmds, img=img, rs=rs, default_snap=a.snap)
            saved = A.save_result(res, Path(a.out) / "edited", tag=f"frame{fr}_edit")
            print(f"frame {fr}: truoc {res['counts_before']} -> sau {res['counts_after']}; con loi {len(res['remaining'])} shape; {saved['shapes']}")
            shapes = res["shapes"]
        doc = P.build_pack(fr, shapes, img, a.out, rs, max_shapes=a.max_shapes)
        for k, v in doc["counts_by_code"].items():
            total[k] = total.get(k, 0) + v
        print(f"frame {fr}: {len(shapes)} shape, {doc['counts_by_severity']}, nghi ngo {doc['flagged_shapes']} (hien {doc['shown']}) -> {Path(a.out) / f'frame_{fr}'}")
    print("TONG theo ma:", json.dumps(dict(sorted(total.items(), key=lambda kv: -kv[1])), ensure_ascii=False))


if __name__ == "__main__":
    main()
