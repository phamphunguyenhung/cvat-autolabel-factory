# Job 285 (task 87) - week1-bbox/G06, frame 60-79 (20 ảnh 1280x720)

URL: https://cvat.edufun.ai/tasks/87/jobs/285

## Phạm vi
- Loại bbox: **rectangle** cho từng đối tượng (car, truck, bus, motorcycle, pedestrian, rider...). Không đổi sang mask/polygon.
- Chung bộ 31 label với job 987, nhưng job này chỉ cần hộp.

## Trạng thái đo được (11/11/2026, chỉ đọc)
- 161 rectangle: car 158, motorcycle 1, truck 2. Stage annotation, state in progress.


## Metric (11/11/2026 22:12, `scripts/bbox_metrics.py`, kết quả ở `metrics/metrics_job285.json`)
- Sau dedupe: 138 rectangle: car 136, motorcycle 1, truck 1. Không còn trùng, không hộp nhỏ/ra ngoài ảnh, source đều manual.
- Phân loại so với YOLO26l: 97 hộp ghép được (IoU>=0.5), đúng nhãn 94.8% (car bị YOLO gọi truck 4, bus 1). 41 hộp tay YOLO không thấy (ảnh đêm, xe xa).
- YOLO thấy mà thiếu hộp tay (conf>=0.35): 36 (car 20, traffic light 10, pedestrian 5, truck 1), lưu nháp `drafts/missingboxes_*.json`, CHƯA ghi CVAT, chờ duyệt.
- Cố ý không làm: giống job 987 (area/*, person, traffic_light, traffic_sign), vegetation bbox chờ quyết định.

## Nhật ký thay đổi trên server
- 11/11 22:11: xóa 23 rectangle trùng hệt (IoU 1.0), backup `tools/cvat-seg-copilot/backups/job285_dedupe_20261111_221117.json`, đọc lại 161 -> 138.
