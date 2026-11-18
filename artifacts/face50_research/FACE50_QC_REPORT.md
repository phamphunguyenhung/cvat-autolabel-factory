# FACE50_QC_REPORT — Job 1975 (Task 473 / Week 2 G06)

> **Chế độ thực thi:** Image-first inspection trên đủ 30 frame (`90..119`), Quality Gate trước khi ghi, PATCH minimal update + POST create cho các ca đạt chuẩn qua 2 vòng (Round 1 + Round 2), và Read-back verification 100% sau mỗi lần sync.

---

## 1. Số liệu tổng kết thực tế (Round 1 + Round 2)

| Chỉ số | Giá trị thực tế | Ghi chú / Bằng chứng |
|---|---:|---|
| Trạng thái phủ frame trên CVAT | **30 / 30** (`90..119`) | **210** shapes, **1,500** keypoints, **0** frame trống |
| Round 1 — PATCH update | **72** keypoints (trên **6** frame, **12** shapes) | `f096` (20 V/Q), `f099` (kp 42), `f101` (kp 42), `f104` (16 V->Q), `f107` (33 V/Q), `f108` (kp 42) |
| Round 1 — Read-back verification | **6 / 6** (`readback_mismatches = 0`) | `before_face50_sync_20261118_104118.json` & `run_face50_sync_20261118_104118.json` |
| Round 2 — PATCH update | **49** keypoints (trên **4** frame, **7** shapes) | `f094` (4), `f095` (5), `f105` (7), `f118` (33) |
| Round 2 — POST create (frame trống) | **100** keypoints (trên **2** frame, **14** shapes) | `f102` (50 kp, 7 shapes) & `f106` (50 kp, 7 shapes); IDs `1453124..1453137` |
| Round 2 — Read-back verification | **6 / 6** (`readback_mismatches = 0`) | `before_face50_sync_20261118_141219.json` & `run_face50_sync_20261118_141219.json` |
| Tổng cộng thay đổi đã sync (R1 + R2) | **221** keypoints (trên **12** frame) | **121** cập nhật + **100** tạo mới (`FACE50_CORRECTION_HISTORY.csv`: 221 dòng) |
| Số case giữ nguyên trong Review Queue | **3** frame | `f100` (profile gắt), `f111` (IR tối, `BROW_BELOW_EYE`), `f112` (IR rất tối, mặt nhỏ 47x38) |
| Post-sync `validate_face50_frame` (30 frame) | **0 lỗi** trên cả **6** frame Round 2 | Toàn bộ 30 frame: **12 errors** (7 lỗi thuộc 3 frame Review Queue `f100, f111, f112`; 5 lỗi `LIP_SELF_INTERSECT` ở các frame baseline `f090, f096, f101, f107, f114`), **4 warnings** |
| Trạng thái QC của các điểm đã sync | `readback_verified_not_human_approved` | Chưa tự gán `human_approved` cho đến khi bạn xác nhận |

---

## 2. Những gì thực sự tốt hơn baseline

1. **Phủ đủ 30/30 frame (`210` shapes, `1,500` keypoints):** `f102` và `f106` đã được dựng đủ 7 skeleton (`longmaytrai`, `longmayphai`, `songmui`, `mattrai`, `matphai`, `moingoai`, `moitrong`) với `source="manual"` và `0` lỗi hình học.
2. **`f094, f095, f105, f118` (Round 2 surgical updates):** Tất cả 4 frame sau khi cập nhật đều đạt `0 errors, 0 warnings` trên `validate_face50_frame`.
3. **Round 1 (`f099, f101, f108, f096, f104, f107`):** Đã chuẩn hóa inner-lip containment và các cờ `V/Q` rõ ràng theo `BTC V1 §5`.

---

## 3. Những gì còn lại cần bạn quyết định trên VS Code

1. **Review Queue (`f100, f111, f112`):** Chưa tự động ghi đè để tránh suy đoán tọa độ trên profile gắt / ảnh IR rất tối.
2. **Baseline `LIP_SELF_INTERSECT` (`f090, f096, f101, f107, f114`):** 5 frame baseline còn cảnh báo/lỗi tự cắt đa giác môi chưa nằm trong scope Round 2.

- Chi tiết lịch sử sửa từng điểm (221 dòng): [`FACE50_CORRECTION_HISTORY.csv`](FACE50_CORRECTION_HISTORY.csv)
- Contact sheet Round 2 đã mở trong VS Code: [`00_FINAL_CONTACT_SHEET.jpg`](evidence/final_proposals/00_FINAL_CONTACT_SHEET.jpg)
- Contact sheet Round 1: [`00_FACE50_CONTACT_SHEET.jpg`](evidence/before_after/00_FACE50_CONTACT_SHEET.jpg)
