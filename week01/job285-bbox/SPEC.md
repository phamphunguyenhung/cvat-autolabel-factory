# Job 285 (task 87) - week1-bbox/G06, frame 60-79 (20 ảnh 1280x720)

URL: https://cvat.edufun.ai/tasks/87/jobs/285

## Phạm vi
- Loại bbox: **rectangle** cho từng đối tượng (car, truck, bus, motorcycle, pedestrian, rider...). Không đổi sang mask/polygon.
- Chung bộ 31 label với job 987, nhưng job này chỉ cần hộp.

## Trạng thái đo được (11/11/2026, chỉ đọc)
- 161 rectangle: car 158, motorcycle 1, truck 2. Stage annotation, state in progress.
- Việc cần làm: viết `bbox_metrics.py` (số bbox theo label, bbox trùng, bbox quá nhỏ, recall so với YOLO), chưa chỉnh gì trên server.
