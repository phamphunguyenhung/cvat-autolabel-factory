# TODO job 987 (cập nhật 11/11/2026, điểm 0.925)

## Cần làm
- [ ] Lane: frame 63, 68, 77 chưa có polyline `lane/*`. Xem ảnh xác nhận có vạch không; có thì vẽ (nháp bằng `predict-scene`, duyệt rồi mới sync).
- [ ] Chồng lấn >0.5%: frame 61 (0.78), 63 (1.5), 66 (0.59). Cắt phần chồng hoặc xóa shape thừa.
- [ ] 8 cặp nghi trùng (contain 0.85-0.96), xem mắt từng cặp, vd frame 60 ids 222629/222637, frame 63 ids 222683/222674. Trùng thật thì xóa, xe sát nhau thật thì giữ.
- [x] Label trùng nghĩa (`person`, `traffic_light`, `traffic_sign`) và `area/drivable`, `area/alternative` (chưa có model): KHÔNG làm, đã ghi `skipped_labels` trong metric.
- [ ] Soát cuối bằng mắt trên CVAT (F5), rồi chạy lại `scripts/mask_metrics.py --job 987`.

## Quy trình đề xuất (để chốt)
1. Đo metric (chỉ đọc) -> 2. sửa hàng loạt bằng script có backup + đọc lại -> 3. soát mắt phần nghi ngờ -> 4. đo lại, cập nhật SPEC, commit.
- Mọi ghi lên server đi qua script dry-run mặc định, `--apply` mới ghi.
- Không đổi lane polyline sang mask.

## Đã xong
- [x] Polygon -> mask (260), backup `backups/job987_tomask_20261111_185433.json`
- [x] Xóa 116 bbox trùng mask
- [x] Xóa 5 mask car trùng hẳn
