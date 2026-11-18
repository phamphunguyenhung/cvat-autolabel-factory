# Lessons Learned (Job 285 -> General Pipeline)

1. **SegFormer-Lane-Marking vs `brighten_for_paint` (`enh`)**:
   - Đưa `enh` (gamma 0.3 + CLAHE 2.5) vào SegFormer làm mất vạch trên frame đêm rất tối (vd `f64`: `0` px trên `enh` vs `2,024` px trên `img` gốc).
   - **Quy tắc**: luôn chạy `_segformer_lane_mask(img, rm)` trên ảnh gốc `img`.
2. **Crosswalk không dùng chung mask vạch dọc**:
   - `SegFormer-Lane-Marking` train cho vạch dọc nên không bắt sọc ngang ngựa vằn và hay gộp thành 1 blob ngang hoặc tạo FP.
   - **Quy tắc**: `detect_crosswalk_stripes` dùng top-hat riêng (`paint_m=None`) + lọc `reg >= 0.45`.
3. **Vạch vàng (`single/double yellow`) bị rửa màu khi lấy median trên tia giãn**:
   - **Quy tắc**: lấy `percentile(..., 75)` trong dải `±2px` quanh tia trên ảnh gốc `img`.
4. **Preview CVAT-style**:
   - Không vẽ `cv2.rectangle` bao quanh `polygon` (`road`, `building`, `area/*`, `lane/*`); dùng polygon tô mờ + viền màu CVAT chuẩn.
   - Không gắn tag `[AI]` hoặc nét đứt làm rối mắt nếu quy trình xuất là `manual`-style preview.
5. **Box lồng nhau & đèn giao thông giả ban đêm**:
   - Dùng `_iomin >= 0.72` để khử box con lồng trong box cha và loại `traffic light` có `cy > 0.55 * H`.
6. **Pose17 Proposal & Sync (`pose17_sync.py`, Job 1623)**:
   - Không bao giờ suy diễn đảo cổ tay/chi từ ảnh nhìn nghiêng để auto-swap tọa độ hay hardcode theo số frame (`f113`, `f093`).
   - Khi người dùng bấm `O` (`outside`) trên tay/chân bị dính sẵn `Q` (`Q+O`), ý định là `O`: phải xóa `Q` giữ `O`, không ép ngược về `Q`.
   - `propose` mặc định đọc live CVAT qua PAT token (chỉ đọc local khi `--offline`), và `sync --yes` phải có staleness guard kiểm tra CVAT live khớp `before_shape` trước khi ghi.
