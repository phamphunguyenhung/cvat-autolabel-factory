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
- 11/11 22:05: scripts/building_draft.py thêm 19 mask building (SegFormer) cho frame 60-63, 76-79 (SAM 2.1b so sánh: viền không tốt hơn, IoU với mask tay 0.56 vs 0.60 của SegFormer nên không dùng). Backup `backups/job987_building_20261111_220523.json`. Xóa 3 shape thừa frame 64 do trùng bản vẽ tay (backup `job987_building64_removed.json`).
- 11/11 22:09: scripts/audit_fix.py tự sửa 81 shape + xóa 6 (chồng lấn theo ưu tiên, trùng, mảnh vụn, source auto). Backup `tools/cvat-seg-copilot/backups/job987_auditfix_20261111_220928.json`. Điểm 0.975. Còn 31 mục cần mắt người: `metrics/audit_job987.json`.
- Bản nháp luôn lưu ở `drafts/` (draftstore.py); áp lại bằng `--apply-draft latest`.
- 11/11 22:32: scripts/stuff_draft.py thêm 216 mask: sidewalk 37, terrain 22, wall 5, fence 20, pole 132 (frame chưa có label đó, trừ phần đã có shape khác). Backup `tools/cvat-seg-copilot/backups/job987_stuff_20261111_223231.json`, đọc lại 400 -> 616. TTA (đa tỉ lệ + lật) đo IoU 0.564 vs gốc 0.567 trên mask building tay: không hơn nên bỏ.
- `road` CHƯA ghi: SegFormer gán cả capo/taplo xe mình thành đường (frame 60, 61, 75...). Nháp `drafts/road_pending_hood_*.json` (29 mask), cần cắt capo trước khi ghi.
- 11/11 22:57: ghi 29 mask road đã cắt capo/taplo bằng quy hoạch động (stuff_draft.py), backup `backups/job987_stuff_20261111_225711.json`, đọc lại 616 -> 645, điểm 0.975. Viền building: scripts/edge_refine_eval.py, trên 11 frame mask tay IoU gốc 0.603, làm sạch 0.608, GrabCut vành biên 0.620 (tăng nhỏ, chưa áp lên server).
