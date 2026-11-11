# Job 987 (task 227) - week1-seg/G06, frame 60-79 (20 ảnh 1280x720)

URL: https://cvat.edufun.ai/tasks/227/jobs/987

## Phạm vi (nguồn: data/active/job987/classes.json của tool + nhóm đối tượng)
- Vạch kẻ đường `lane/*` (single white/yellow/other, double white/yellow, crosswalk, road curb): **polyline**, giữ nguyên, không đổi mask.
- `traffic sign`, `sky`: **mask**.
- Đối tượng: car, truck, bus, motorcycle, bicycle, pedestrian, rider, traffic light: **mask** (từng instance).
- `vegetation`: **mask**, người dùng yêu cầu vẽ thêm (11/11 21:38). KHÔNG thuộc job này: road, sidewalk, building, terrain...
- Cố ý KHÔNG làm (ghi trong `skipped_labels` của metric): `area/drivable`, `area/alternative` (chưa có model), `person`, `traffic_light`, `traffic_sign` (trùng nghĩa).
- Lưu ý label trùng nghĩa: `traffic light`/`traffic_light`, `traffic sign`/`traffic_sign` (31 label, phân trang API).

## Trạng thái đo được (11/11/2026)
- 310 shape: 255 mask + 55 polyline, 0 polygon, 0 bbox. Điểm hoàn thiện 0.925 (qua cổng cron 0.9).
- Còn: frame 61, 63, 66 chồng lấn >0.5%; 8 cặp nghi trùng contain 0.85-0.96 (cần xem mắt, có thể là xe sát nhau); frame 63, 68, 77 chưa có polyline lane (cần người xem ảnh có vạch không).
- Metric: `python scripts/mask_metrics.py --job 987 --json ...` (chỉ đọc).

## Nhật ký thay đổi trên server
- 11/11 04:25 UTC: replace-boxes xóa 116 bbox (backup `backups/job987_20261111_112501.json`).
- 11/11 18:54 (giờ máy): to-mask 260 polygon -> mask (backup `backups/job987_tomask_20261111_185433.json`, đã đọc lại khớp).
- 11/11 19:16: scripts/dedupe_masks.py xóa 5 mask car trùng hẳn (contain >=0.99), backup `tools/cvat-seg-copilot/backups/job987_dedupe_20261111_191634.json`, đọc lại khớp.
- 11/11 21:38: scripts/vegetation_draft.py thêm 55 mask vegetation (SegFormer, 19 frame; frame 72 đã có sẵn), backup `tools/cvat-seg-copilot/backups/job987_vegetation_20261111_213817.json`, đọc lại 56 khớp.
