"""Đổi shape source=file (pre-label) thành source=manual, GIỮ NGUYÊN tọa độ, label, trạng thái điểm.

Quy trình an toàn (chỉ khi --yes mới ghi CVAT):
  1. Dry-run mặc định: in danh sách shape sẽ đổi.
  2. Backup toàn bộ shape cũ (kèm id) vào <job>/backups/before_manual_<ts>.json trước khi ghi.
  3. Tạo shape mới source=manual.
  4. Xác minh: số shape manual mới khớp số shape file cũ, rồi mới xóa shape file cũ.
  5. Đọc lại CVAT và in kết quả.

  python -X utf8 scripts/w2_source_manual.py --job 1623 --job 1975            # dry-run
  python -X utf8 scripts/w2_source_manual.py --job 1623 --job 1975 --yes      # ghi thật
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(ROOT / "src"))
from cvat_tools.core.client import Cvat  # noqa: E402
from cvat_tools.pose import week2  # noqa: E402

SHAPE_KEYS = ("label_id", "type", "frame", "points", "occluded", "attributes", "group", "z_order", "rotation")
ELEM_KEYS = ("label_id", "type", "frame", "points", "occluded", "outside", "attributes", "group", "z_order", "rotation")


def to_manual_body(shape: dict) -> dict:
    body = {k: shape[k] for k in SHAPE_KEYS if k in shape}
    body["source"] = "manual"
    body["elements"] = []
    for e in shape.get("elements", []):
        el = {k: e[k] for k in ELEM_KEYS if k in e}
        el["source"] = "manual"
        body["elements"].append(el)
    return body


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", type=int, action="append", required=True)
    ap.add_argument("--profile", default="edufun")
    ap.add_argument("--yes", action="store_true", help="Ghi thật lên CVAT. Không có cờ này thì chỉ dry-run.")
    ap.add_argument("--from-source", default="file", help="Nguồn cần đổi sang manual: file (mặc định) hoặc auto.")
    ap.add_argument("--recover-from", type=Path, help="Chạy sau lỗi giữa chừng: KHÔNG tạo lại, chỉ xóa shape file có id nằm trong backup, sau khi kiểm tra đủ bản manual.")
    a = ap.parse_args()

    c = Cvat.from_env(a.profile, write_enabled=a.yes)
    if a.recover_from:
        backup_shapes = json.loads(a.recover_from.read_text(encoding="utf8"))
        job = a.job[0]
        current = c.annotations(job)["shapes"]
        cur_file_ids = {s["id"] for s in current if s.get("source") == "file"}
        manual_frames = Counter(s["frame"] for s in current if s.get("source") == "manual")
        backup_frames = Counter(s["frame"] for s in backup_shapes)
        if not {s["id"] for s in backup_shapes} <= cur_file_ids:
            raise SystemExit("Backup có id không còn là shape file trên CVAT, DỪNG.")
        if any(manual_frames[f] < n for f, n in backup_frames.items()):
            raise SystemExit("Chưa đủ shape manual cho mọi frame trong backup, DỪNG, không xóa.")
        if not a.yes:
            print(f"DRY-RUN recover job {job}: sẽ xóa {len(backup_shapes)} shape file cũ. Thêm --yes để thực hiện.")
            return
        c.delete_shapes(job, backup_shapes)
        after = c.annotations(job)["shapes"]
        print(f"job {job} recover: file còn {sum(s.get('source') == 'file' for s in after)}, manual {sum(s.get('source') == 'manual' for s in after)}")
        return
    plan = {}
    for job in a.job:
        shapes = c.annotations(job)["shapes"]
        file_shapes = [s for s in shapes if s.get("source") == a.from_source]
        plan[job] = file_shapes
        frames = sorted({s["frame"] for s in file_shapes})
        print(f"job {job}: {len(file_shapes)} shape source=file trên frame {frames}")
        print(f"  tổng shape hiện có: {len(shapes)}, nguồn: {dict(Counter(s.get('source') for s in shapes))}")

    if not a.yes:
        print("\nDRY-RUN: chưa ghi gì. Thêm --yes để thực hiện.")
        return

    ts = time.strftime("%Y%m%d_%H%M%S")
    for job, file_shapes in plan.items():
        if not file_shapes:
            print(f"job {job}: không có shape file, bỏ qua")
            continue
        folder = week2.job_folder(job)
        backup = folder / "backups" / f"before_manual_{ts}.json"
        backup.parent.mkdir(exist_ok=True)
        backup.write_text(json.dumps(file_shapes, ensure_ascii=False, indent=1), encoding="utf8")
        print(f"job {job}: đã backup {len(file_shapes)} shape -> {backup}")

        bodies = [to_manual_body(s) for s in file_shapes]
        for b, s in zip(bodies, file_shapes):
            b["frame"] = s["frame"]
        created = c.create_shapes(job, bodies)
        new_ids = [s["id"] for s in created.get("shapes", [])]
        if len(new_ids) != len(file_shapes):
            raise SystemExit(f"job {job}: tạo {len(new_ids)}/{len(file_shapes)} shape, DỪNG, chưa xóa bản cũ. Backup: {backup}")

        c.delete_shapes(job, file_shapes)  # cần đủ type/label_id/frame, chỉ truyền id sẽ bị 400

        after = c.annotations(job)["shapes"]
        remain_file = sum(1 for s in after if s.get("source") == "file")
        manual_now = sum(1 for s in after if s.get("source") == "manual")
        print(f"job {job}: đọc lại -> file còn {remain_file}, manual {manual_now}")
        (folder / "backups" / f"after_manual_{ts}.json").write_text(
            json.dumps({"created_ids": new_ids, "deleted_ids": [s["id"] for s in file_shapes]}, indent=1), encoding="utf8")


if __name__ == "__main__":
    main()
