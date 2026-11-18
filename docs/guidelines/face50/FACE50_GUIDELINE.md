# FACE50_GUIDELINE — Task 473 / Job 1975 (Week 2 G06)

> **Phân biệt nguồn gốc quy tắc:**
> - `BTC_OFFICIAL`: Quy định trực tiếp trong `weeks/guidelines/w2-face50-pose17.md` (theo `Face_Landmark50_Annotation_Guideline_V1.docx`).
> - `GEOMETRIC_INFERENCE`: Quy chuẩn kiểm tra hình học theo hệ tọa độ cục bộ của khuôn mặt (`face50_engine.py`).
> - `TEAM_CLARIFICATION`: Quy ước nội bộ đang chờ mentor chốt (`needs_mentor`).
> - Mọi bản sửa đã sync bởi hệ thống được gắn trạng thái `ai_reviewed_synced_not_human_approved`, **không tự gắn `human_approved`**.

---

## 1. Cấu trúc 7 Skeleton (50 Keypoint, ID 0–49)

| Skeleton Label | IDs | Số điểm | Quy tắc giải phẫu (`BTC_OFFICIAL`) |
|---|---:|---:|---|
| `longmaytrai` | 0–4 | 5 | Bờ **trên** lông mày bên trái ảnh: từ đuôi ngoài (0) -> đầu trong (4). Không đặt lên da trán. |
| `longmayphai` | 5–9 | 5 | Bờ **trên** lông mày bên phải ảnh: từ đầu trong (5) -> đuôi ngoài (9). |
| `songmui` | 10–13 | 4 | Chia 3 đoạn gần bằng nhau: 10 (đỉnh lõm giữa 2 mắt) -> 13 (chân sống mũi, chưa chạm chóp mũi). |
| `mattrai` | 14–21 | 8 | Mắt trái ảnh: 14 khóe ngoài, 15–17 bờ mí trên, 18 khóe trong, 19–21 bờ mí dưới. |
| `matphai` | 22–29 | 8 | Mắt phải ảnh: 22 khóe trong, 23–25 bờ mí trên, 26 khóe ngoài, 27–29 bờ mí dưới. |
| `moingoai` | 30–41 | 12 | Mép ngoài môi: 30 khóe trái, 31–35 viền trên, 36 khóe phải, 37–41 viền dưới. |
| `moitrong` | 42–49 | 8 | Mép trong khe miệng: 42 khóe trái, 43–45 trên, 46 khóe phải, 47–49 dưới. **Không được chạm hoặc vượt ra ngoài `moingoai` (`30..41`).** |

---

## 2. Bài học thực nghiệm & Quality Gates từ Job 1975 (30 frame `90–119`)

1. **Vòng môi trong (`42..49`) vs vòng môi ngoài (`30..41`) (`F50-R02`):**
   - Trong 28 frame đã có nhãn, phát hiện các điểm góc môi trong (`42` hoặc `46`) bị nhô `1–3 px` ra ngoài đa giác `moingoai` (`f099, f101, f108`, cũng như `f094, f095, f111, f118`).
   - **Cách sửa chuẩn:** Chỉ dịch phẫu thuật điểm `42`/`46` vào trong `>= 1.2 px` dọc trục tâm miệng; giữ nguyên 100% các điểm còn lại.
2. **Đánh giá hình học theo trục khuôn mặt (`F50-R06`):**
   - Các ảnh fisheye nằm ngang 90° (`f092`, `f116`) xoay trục mặt nằm ngang; kiểm tra `y`-tuyệt đối gây báo lỗi giả. Phải chiếu qua `_face_rotation_basis` (trục nối tâm mắt trái `14..21` -> tâm mắt phải `22..29`).
3. **Cờ trạng thái `V` vs `Q` (`F50-R04`, `F50-R05`):**
   - Kính râm tối trong ảnh IR (`f104`): mắt `14..29` đặt theo gọng/tròng và gắn `Q` (`occluded`).
   - Tay/ngón tay che miệng & sống mũi dưới (`f107`): lông mày `0..9` lộ rõ phải để `V`, còn `11..13` và `30..49` sau ngón tay phải gắn `Q`.
   - Miệng lộ rõ (`f096`): `30..49` để `V`, không gắn `Q`.
4. **Cơ chế Review Queue cho ca mơ hồ (`F50-R07`):**
   - Không tự bịa tọa độ cho frame trống hoặc profile cực đoan / fisheye xoay 90° khi chưa qua kiểm định: đưa vào Review Queue kèm ảnh zoom crop (`artifacts/face50_research/evidence/crops/`) để người gán nhãn hoặc mentor quyết định.
   - Sau vòng đối soát F02–F06 trên Job 1975: `f094, f095, f102, f105, f106, f118` đã đạt `0` lỗi trong `validate_face50_frame` (`ai_reviewed_eligible`); `f100, f111, f112` giữ ở `needs_human_decision`; và `f116` giữ ở `needs_mentor_decision` (chốt quy ước trái/phải `89.0°` fisheye theo `F50-R07`).

---

## 3. Quy trình căn chỉnh `CLAHE + Gamma + FAN2D + BrowEdgeSnap + InnerLipClamp` (`F50-R09..R11`)

Quy trình căn chỉnh chuẩn cho ảnh IR tối, ngược sáng hoặc xoay ngang 90°/270° được đóng gói trong `align_face50_clahe_fan(img_bgr, try_rotations=True, landmarker=None)` (`src/cvat_tools/pose/face50_engine.py`):

1. **Tiền xử lý quang trắc thích ứng (Adaptive Gamma + LAB CLAHE):**
   - Tính mean luma BT.601 trên ảnh đầu vào. Trong `align_face50_clahe_fan`, áp dụng Gamma LUT `gamma = 0.55` khi `mean_luma < 90` (trong benchmark F02: `0.55` cho IR tối `< 50` và `0.65` cho RGB/sáng; trường hợp đặc biệt quá tối bị tay che như `f102` dùng `gamma = 0.45` + `clipLimit = 4.0` để đọc trực quan).
   - Chuyển không gian màu sang LAB và chạy CLAHE trên kênh `L` (`clipLimit = 2.5` trong engine, `tileGridSize = (8, 8)`).
2. **Phát hiện đa góc xoay (`FAN2D`, `try_rotations=True`):**
   - Gọi `FaceLandmarker.landmarks68(enh, try_rotations=True)` và ánh xạ `map68_to_50` sang 50 điểm Face50.
   - Áp dụng **Quality Gate** lọc false positive: loại bỏ candidate có `face_score < 0.90` hoặc `mean_kp_score < 0.55` (chặn được ca nhận nhầm thân người ở `180°` trên `f095` `face_score=0.773` và ca IR suy giảm trên `f110` `face_score=0.846, mean_kp_score=0.452`).
3. **`BrowEdgeSnap` (`F50-R09`):**
   - Bám biên gradient Sobel bờ trên lông mày (`0..4` và `5..9`) trong vùng tìm kiếm `±4 px` dọc theo vector hướng xuống cục bộ `v` của khuôn mặt.
   - Ràng buộc **bắt buộc**: giữ thứ tự đơn điệu theo trục ngang cục bộ `u` (`BROW_NON_MONOTONIC_LOCAL`) và đảm bảo mọi điểm lông mày nằm **trên** bờ mí mắt trên `15..17` / `23..25` (`BROW_BELOW_EYE`).
4. **Kiểm tra tự cắt vòng môi (`LIP_SELF_INTERSECT`, `F50-R10`):**
   - Hàm `_polygon_self_intersects` kiểm tra mọi cặp cạnh không kề của đa giác `moingoai` (`30..41`) và `moitrong` (`42..49`). Nếu phát hiện tự cắt (ví dụ điểm trùng tọa độ `43/49` trên `f094`), ca lỗi bị chặn sync tự động và phải tách tọa độ hoặc đẩy vào Review Queue.
5. **`TightInnerLipContainment` & `InnerLipClamp` (`F50-R11`):**
   - `validate_face50_frame` siết ngưỡng lọt biên vòng môi trong từ `-0.3 px` xuống **`-0.05 px`** (phát hiện các ca lọt nhẹ mức sub-pixel như `f105` `-0.22 px` và `f112` `-0.16 px`).
   - `InnerLipClamp` (`_nudge_inner_lip_point`) dịch nhẹ các điểm `42..49` về tâm miệng để nằm hoàn toàn bên trong đa giác `moingoai`.

---

## 4. Cách giải quyết hai ca thiếu nhãn trọng điểm (`f102`, `f106`)

| Frame | Vấn đề ban đầu (`pre-goal`) | Phương pháp giải quyết (F02 / F04 / F05) | Trạng thái & Visibility |
|---|---|---|---|
| **`f102`** (`G06_103.jpg`) | Thiếu nhãn (`0 shapes`), IR tối (`luma=29.9`); hai tay chỉnh kính che nửa dưới sống mũi và toàn bộ miệng, khiến FAN2D trả về `None`. | Đọc trực quan trên ảnh tăng cường **CLAHE (`clipLimit=4.0`) + Gamma (`0.45`)** kết hợp nội suy tỷ lệ spline bằng `w2_face_propose.py`. Đạt `0` findings trong `validate_face50_frame`. | `ai_reviewed_eligible` (`create`). Proposal F05: `16 V / 34 Q / 0 O` (`0..9, 10, 22..29` = `V`; `11..13, 14..21, 30..49` sau tay/ngón tay/kính = `Q`; không dùng `O` theo BTC V1 §2.1 & §5, ghi nhận `ATTRIBUTE_CHECK`). |
| **`f106`** (`G06_107.jpg`) | Thiếu nhãn (`0 shapes`), ảnh IR fisheye xoay ngang **`90°`** (`luma=15.1`) có kính tối/phản quang. | Khôi phục thành công bằng **CLAHE + Gamma (`0.55`) + FAN2D (`try_rotations=True`, `rot=90°`, `face_score=0.9987–0.9994`) + gỡ xoắn `moitrong`**. Đối chiếu khớp hoàn toàn hướng xoay của `f116` (`89.0°`: `mattrai` ở trên `y≈541`, `matphai` ở dưới `y≈635`, `songmui` từ phải sang trái). Đạt `0` findings. | `ai_reviewed_eligible` (`create`). F04 khuyến nghị gắn `Q` cho hai mắt `14..29` sau tròng kính phản quang (`23 V / 27 Q / 0 O`, `0 O`) và ghi nhận `UNCERTAIN_CLASS` / `LOW_VISIBILITY` đồng bộ với `f116`. |

---

## 5. Tổng hợp trạng thái Case khó Job 1975 (`FACE50_DIFFICULT_CASES.csv`)

- **Đã sync & verify (`6` frames):** `96, 99, 101, 104, 107, 108` (`ai_reviewed_synced_not_human_approved`).
- **Đủ điều kiện sync (`ai_reviewed_eligible`, `6` frames):** `94, 95, 102, 105, 106, 118` (đều đạt `0` findings trên `validate_face50_frame`).
- **Chờ người gán nhãn quyết định (`needs_human_decision`, `3` frames):** `100` (profile `-35.8°`, `BROW_NON_MONOTONIC_LOCAL`), `111` (IR tối `luma=33.4`, `kp 5` `BROW_BELOW_EYE`), `112` (IR rất tối `luma=15.7`, mặt nhỏ `47×38 px`).
- **Chờ mentor chốt (`needs_mentor_decision`, `1` frame):** `116` (fisheye IR xoay `89.0°` — chốt quy ước trái/phải `F50-R07` và visibility mắt sau tròng kính lóa IR).

- Bảng rule máy đọc: [`FACE50_RULES.csv`](FACE50_RULES.csv)
- Danh sách case khó: [`FACE50_DIFFICULT_CASES.csv`](FACE50_DIFFICULT_CASES.csv)
