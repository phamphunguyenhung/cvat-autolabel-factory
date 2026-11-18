# VERSION_ANALYSIS — Phân tích lịch sử & tiến hóa Job 1623

> Nguồn dữ liệu: [`VERSION_HISTORY.md`](VERSION_HISTORY.md), [`version_comparison.csv`](version_comparison.csv), [`annotation_change_log.csv`](annotation_change_log.csv), [`A02_deltas.json`](agents/A02_deltas.json), [`A06_geometry_metrics.json`](agents/A06_geometry_metrics.json).

---

## 1. Tóm tắt chuỗi phiên bản Annotation trên Job 1623

| Giai đoạn | Thời điểm | Nguồn bằng chứng | Số shape | Mô tả & Thay đổi định lượng |
|---|---|---|---:|---|
| **Pre-label (`file`)** | Trước `2026-11-16 17:50:14` | `before_20261116_175014.json` | 10 | 10 frame (`91,92,97,98,103,104,109,110,115,116`), `140 visible / 30 occluded / 0 outside`. Nguồn gốc tạo file trước thời điểm này: `history_unavailable`. |
| **Push #1 (`spm` YOLO)** | `2026-11-16 17:50:15` | `run_20261116_175015.json` | 25 | Thêm 15 shape `source=auto` từ `yolo11l-pose.pt` (`LOW_CONF_Q=0.5`). |
| **Push #2 (`auto` consensus)** | `2026-11-17 10:02:10` | `run_20261117_100210.json` | 28 | Thêm 18 shape `auto` (YOLO+ViTPose, xoay 4 hướng), bỏ qua `f100, f118`. |
| **Human edits đợt 1** | `10:02`–`19:29` `17/11` | `before_1117_101353`, `before_manual_192910` | 28 | Sửa `f90 kpt 17` (+210.56 px), `f91 kpts 14,16` (`occluded->outside`), `f91 kpts 5,13`. |
| **Push #3 & #4 (`LIMB_IDX` + `R/L`)** | `17/11 10:13–10:23` | `run_20261117_101354.json`, `102337` | 28 | Áp `V0_CONF=0.3` cho `LIMB_IDX` và `enforce_image_lr` (bảo vệ `f90` đã sửa). |
| **Đổi `source -> manual`** | `17/11 19:29–19:30` | `before_manual_*.json`, `after_manual_*.json` | 28 | `w2_source_manual.py` tạo lại 10 `file` + 18 `auto` thành `manual` (`0.0 px` dịch chuyển). |
| **Bất thường `08:24:15`** | `2026-11-18 08:24:15` | `live_1623_20261118_082415.json` | 29 | Xuất hiện thêm 1 shape `file` trùng trên `f92` (`id=1163232`) với 5 điểm đã sửa (35.6–193.1 px). |
| **Trạng thái hiện tại CVAT** | `2026-11-18 09:18` | `job_1623_annotations_raw.json` | 28 | Shape trùng `1163232` đã xóa. So với `before_manual_*`, người dùng đã sửa **25/28 frame**: **148 lượt dời tọa độ**, **51 lượt đổi visibility** (trung bình `75.15 px`, tối đa `545.55 px`). |

---

## 2. Kết luận về v1 / v2 và giới hạn lịch sử

- **Không đánh đồng 3 trục phiên bản:**
  1. **Annotation**: `source=file` (pre-label) -> `source=auto` (nháp tool) -> `source=manual` (chuyển đổi 17/11) -> `manual` đã qua chỉnh sửa tay 25/28 frame (18/11).
  2. **Guideline**: Pre-BTC 16/11 (giải phẫu) -> BTC V1 + G06 17/11 (theo ảnh) -> Pose17 Engine 18/11 (Tầng A + Tầng B).
  3. **Tool/Pipeline**: `spm` (v1) -> `person17.py` `yolo/vitpose` (v2) -> `auto` consensus (v3) -> `LIMB_IDX + enforce_image_lr` (v4) -> `pose17_validate` 5 lớp (v5).
- **Giới hạn truy vết:** CVAT `/api/events` trả HTTP 500 và `/api/tasks/402` trả HTTP 403, nên lịch sử trước `2026-11-16 17:50:14` và log thao tác từng click trên UI CVAT là `history_unavailable`. Mọi delta định lượng trong [`annotation_change_log.csv`](annotation_change_log.csv) đều được tính trực tiếp từ các snapshot JSON thực tế.
