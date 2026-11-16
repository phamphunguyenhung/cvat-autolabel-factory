# Job 1623 (task 402) — week2-human-pose/G06, frame 90–119 (30 ảnh 1280×1024)

URL: https://cvat.edufun.ai/tasks/402/jobs/1623
Gán cho: mình. Trạng thái lúc đọc (16/11/2026): `new`, stage `annotation`.

## Phạm vi
- 1 skeleton `person_vf17` mỗi ảnh, 17 điểm thứ tự COCO (tên điểm trên CVAT là số 1–17). Chế độ Shape.
- Trái/phải theo người (điểm chẵn nằm bên phải ảnh trong khung mẫu quay mặt). Ảnh trong cabin, có ảnh hồng ngoại xám.

## Hiện trạng
- Có sẵn 10 skeleton `source=file` ở frame 91, 92, 97, 98, 103, 104, 109, 110, 115, 116, nhiều điểm lệch khỏi khớp (nháp thô).
- 20 frame còn lại chưa có nhãn. Chưa biết được phép xóa hay sửa nháp không.

## Chưa làm
- Nháp AI: chờ xác nhận được dùng AI hay không.
- Xem nhãn: `python scripts/render_skeleton_overlay.py --job 1623 --profile edufun --frames 91`
