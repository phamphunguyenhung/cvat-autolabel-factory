# Job 987 (task 227) - week1-seg/G06, frame 60-79 (20 ảnh 1280x720)

URL: https://cvat.edufun.ai/tasks/227/jobs/987

## Phạm vi (nguồn: data/active/job987/classes.json của tool + nhóm đối tượng)
- Vạch kẻ đường `lane/*` (single white/yellow/other, double white/yellow, crosswalk, road curb): **polyline**, giữ nguyên, không đổi mask.
- `traffic sign`, `sky`: **mask**.
- Đối tượng: car, truck, bus, motorcycle, bicycle, pedestrian, rider, traffic light: **mask** (từng instance).
- KHÔNG thuộc job này: road, sidewalk, building, vegetation, terrain... (label có trong task nhưng không phải việc phải vẽ).
- Lưu ý label trùng nghĩa: `traffic light`/`traffic_light`, `traffic sign`/`traffic_sign` (31 label, phân trang API).

## Trạng thái đo được (11/11/2026)
- 315 shape: 260 mask + 55 polyline, 0 polygon, 0 bbox. Điểm hoàn thiện 0.875 (cổng cron 0.9).
- Còn: frame 61, 63, 67, 73 chồng lấn >0.5%; 13 cặp nghi shape trùng (chủ yếu car); frame 63, 68, 77 chưa có polyline lane.
- Metric: `python scripts/mask_metrics.py --job 987 --json ...` (chỉ đọc).

## Nhật ký thay đổi trên server
- 11/11 04:25 UTC: replace-boxes xóa 116 bbox (backup `backups/job987_20261111_112501.json`).
- 11/11 18:54 (giờ máy): to-mask 260 polygon -> mask (backup `backups/job987_tomask_20261111_185433.json`, đã đọc lại khớp).
