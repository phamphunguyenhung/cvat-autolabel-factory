# Pose17 Guideline Changelog & Rule Governance Protocol

> Tài liệu theo dõi lịch sử thay đổi của hệ thống guideline Pose17 (`Tier A: G06_POSE17_GUIDELINE.md` và `Tier B: POSE17_GENERAL_GUIDELINE.md`) và quy trình đề xuất quy tắc mới từ các job sau.

---

## 1. Lịch sử phiên bản theo 3 trục độc lập

### 1.1 Trục Guideline Version
| Version | Ngày | Commit / Tài liệu | Thay đổi chính |
|---|---|---|---|
| **v0.1 (Pre-BTC)** | `2026-11-16` | `3f5391cb` (`weeks/guidelines/w2-face50-pose17.md`, `SPEC.md`) | Bản tự viết nội bộ trước khi có BTC V1; dùng **trái/phải giải phẫu** theo người; chưa có chính sách `v0` cho tay/chân. |
| **v1.0 (BTC V1 + G06)** | `2026-11-17` | `cd129065` (`w2-face50-pose17.md`, `week02/issues.md`) | Đồng bộ `HumanPose17_Annotation_Guideline_V1.docx`: chuyển sang **trái/phải theo ảnh** (kể cả xoay 90°), thêm `outside` (`v0`) cho tay/chân không suy ra được, sai số `±5 px` (V) / `±20 px` (Q), bỏ qua frame không có tài xế, quy trình issue `UNCERTAIN_CLASS`. |
| **v2.0 (Tier A/B + Evidence)** | `2026-11-18` | `G06_POSE17_GUIDELINE.md` (Tier A), `POSE17_GENERAL_GUIDELINE.md` (Tier B), `GUIDELINE_CHANGELOG.md` | Tách rõ quy tắc đặc thù Job 1623 (Tier A) và quy tắc tái sử dụng (`P17-G01`–`P17-G30`, Tier B); phân tách nghiêm ngặt 4 nguồn (`BTC_OFFICIAL`, `USER_OBSERVED`, `GEOMETRIC_INFERENCE`, `AI_RECOMMENDATION`); tích hợp kiểm toán định lượng 30 frames (`A01`–`A06`). |

### 1.2 Trục Annotation Version (Job 1623 — tham chiếu đồng bộ)
1. **Pre-label (`source=file`)**: 10 shapes (`1163231..1163240`) trên `[91, 92, 97, 98, 103, 104, 109, 110, 115, 116]` trước `2026-11-16 17:50:14`.
2. **Tool Drafts (`source=auto`)**: Push #1 (`17:50:15`, 15 shapes) -> Push #2 (`17/11 10:02:10`, 18 shapes) -> Push #3 (`10:13:54`, thêm `V0_CONF`) -> Push #4 (`10:23:37`, giới hạn `LIMB_IDX` + `enforce_image_lr`, bảo vệ `f90`).
3. **Source-Converted (`source=manual`)**: 28 shapes (`1319662..1319671`, `1320579..1320596`) lúc `17/11 19:29–19:30`; chưa duyệt chất lượng.
4. **Live Partial Human Edits (`18/11 09:17`)**: Xóa bản trùng `1163232` ở `f92`, sửa tay `25/28` frames (`148` dịch chuyển, `51` đổi trạng thái), `f100`/`f118` còn trống, `gold = 0`.

### 1.3 Trục Tool / Pipeline Version
1. **Day 4 `spm` (`16/11`, `138543e1`)**: `week2.py` + `yolo11l-pose.pt`, `LOW_CONF_Q=0.5`, không xoay 4 hướng.
2. **`person17.py` Single/Consensus (`16/11 19:01–19:57`)**: `yolo` / `vitpose`, xoay 4 hướng `detect()`, `merge_consensus` (`AGREE_FRAC=0.35`, `DISAGREE_CONF=0.4`).
3. **`person17.py` BTC-V1 Aligned (`17/11 10:13–10:23`, `cd129065`)**: `V0_CONF=0.3` giới hạn trong `LIMB_IDX = {7,8,9,10,13,14,15,16}` + `enforce_image_lr` (`LR_MIN_SEP=0.12`).

---

## 2. Quy trình đề xuất & phê duyệt quy tắc mới (Future Pose17 Jobs)

Mọi quy tắc mới phát sinh từ các job tiếp theo phải đi qua 4 bước bắt buộc:

1. **Đề xuất (`status: proposed`):**
   - Gán `rule_id` mới kế tiếp trong `POSE17_GENERAL_GUIDELINE.md` (ví dụ `P17-G31`).
   - Ghi rõ `source_type` (`USER_OBSERVED`, `GEOMETRIC_INFERENCE`, hoặc `AI_RECOMMENDATION`), `source_ref` (job ID, frame, script/commit), và `confidence` (`low`/`medium`/`high`).
   - **Cấm** tự động gắn nhãn `BTC_OFFICIAL` hoặc `status: approved` cho các hành vi mới quan sát từ người gán (`USER_OBSERVED`).
2. **Đối chiếu bằng chứng (Evidence Review):**
   - Kiểm tra xem đề xuất có xung đột với `BTC_OFFICIAL` (`P17-G01`–`P17-G07`, `P17-G10`–`P17-G16`, `P17-G18`–`P17-G22`) hay không.
   - Đính kèm bằng chứng định lượng (số frame bị ảnh hưởng, overlay minh họa, hoặc delta trên `gold` nếu có).
3. **Phân nhánh quyết định:**
   - Nếu là quy tắc kỹ thuật/QC không trái BTC và có bằng chứng nhất quán -> nâng lên **`approved`**.
   - Nếu liên quan đến cách hiểu guideline BTC (như R/L ảnh xoay 90°, chuẩn hóa sai số theo độ phân giải, ngưỡng mặt tối thiểu) -> đặt **`needs_mentor`**, tạo CVAT issue tương ứng (`UNCERTAIN_CLASS`, `ATTRIBUTE_CHECK`, `LOW_VISIBILITY`).
4. **Cập nhật Changelog & Đồng bộ công cụ:**
   - Ghi 1 dòng vào mục 1 của `GUIDELINE_CHANGELOG.md`, cập nhật `pose17_rules.csv`, và đồng bộ logic kiểm tra vào `scripts/w2_qc_rules.py` / `scripts/eval_pose17.py`.
