# VERSION_HISTORY — Job 1623 (Task 402 / Week 2 G06 Pose17)

> Tài liệu tổng hợp từ bằng chứng thực tế trong git history, `week02/task402-pose/job1623-pose17/{backups,drafts}/`, `reports/w2_recovery/snapshots/`, và CVAT API (`artifacts/pose17_research/snapshots/job_1623_annotations_raw.json`).  
> Không suy diễn phiên bản `v1`/`v2` khi thiếu bằng chứng; các mốc không truy xuất được lịch sử được ghi rõ `history_unavailable`.

---

## 1. Phân biệt 3 trục phiên bản độc lập

1. **Annotation Version (Trạng thái dữ liệu nhãn trên CVAT):**
   - **Pre-label (`source=file`)**: 10 shape (`id=1163231..1163240`) trên các frame `91, 92, 97, 98, 103, 104, 109, 110, 115, 116` (`140 visible`, `30 occluded`, `0 outside`). Nguồn gốc trước `2026-11-16 17:50:14`: `history_unavailable` (CVAT `/api/events` trả HTTP 500, `/api/tasks/402` trả HTTP 403; tài liệu nội bộ `w2-face50-pose17.md` §6 và `week02/issues.md` A6 ghi là pre-label từ BTC).
   - **Tool Drafts (`source=auto`)**: Các lượt đẩy tự động từ `spm` (`run_20261116_175015.json`, 15 shape) và `person17.py` (`run_20261117_100210.json`, `101354`, `102337`, tối đa 18 shape).
   - **Converted Manual (`source=manual` pre-human-edit, 17/11 19:29–19:30)**: Toàn bộ 10 shape `file` (`before_manual_20261117_192910.json` -> `1319662..1319671`) và 18 shape `auto` (`before_manual_20261117_193049.json` -> `1320579..1320596`) được tạo lại với `source=manual`, giữ nguyên tọa độ và trạng thái điểm.
   - **Post-19:46 Anomaly (`2026-11-18 08:24:15`, `live_1623_20261118_082415.json`)**: Xuất hiện 29 shape (28 `manual` khớp 0.0 px với `before_manual_*` + 1 shape `source=file` `id=1163232` trùng trên frame 92 với 5 keypoint đã chỉnh tay).
   - **Current Live CVAT (`2026-11-18 09:18`, `job_1623_annotations_raw.json`)**: 28 shape `source=manual` (476 keypoints: `359 visible`, `59 occluded_only`, `36 outside_only`, `22 occluded+outside`). Shape trùng `1163232` trên frame 92 đã bị xóa. Người dùng đã chỉnh sửa **25/28 frame** so với `before_manual_*` (**148 lượt dời tọa độ**, **51 lượt đổi visibility**); chỉ 3 frame (`90, 91, 95`) giữ nguyên và 2 frame (`100, 118`) vẫn chưa có skeleton.
   - **CVAT Server History**: `history_unavailable` (`version=0` trong `/api/jobs/1623/annotations`, `/api/events` HTTP 500).

2. **Guideline Version (Tài liệu quy chuẩn gán nhãn):**
   - **Pre-BTC Internal (`3f5391cb`, 16/11/2026)**: Quy ước trái/phải theo giải phẫu người.
   - **BTC V1 + G06 Internal (`cd129065`, 17/11/2026, `weeks/guidelines/w2-face50-pose17.md`)**: Quy ước trái/phải **theo ảnh** (chẵn=R=phải ảnh, lẻ=L=trái ảnh), quy định `v0` (`outside`) cho tay/chân che hẳn, sai số `±5 px` (visible) / `±20 px` (occluded).
   - **Pose17 Gold Reference & Engine (`2026-11-18`)**:
     - Tier A: `docs/guidelines/pose17/G06_POSE17_GUIDELINE.md`
     - Tier B: `docs/guidelines/pose17/POSE17_GENERAL_GUIDELINE.md` (`P17-G01`..`P17-G30`)

3. **Tool / Pipeline Version (Công cụ sinh nháp & kiểm thử):**
   - **v1 (`spm` Day 4, 16/11 17:22–17:50)**: `yolo11l-pose.pt`, `LOW_CONF_Q=0.5`, chưa xoay 4 hướng.
   - **v2 (`person17.py` `yolo` / `vitpose`, 16/11 19:01–19:53)**: Thêm `usyd-community/vitpose-base-simple`.
   - **v3 (`person17.py` `auto` consensus, 16/11 19:55–17/11 10:02)**: Hợp nhất YOLO + ViTPose (`AGREE_FRAC=0.35`), xoay 4 hướng, `push_policy.json` bỏ qua `[100, 118]`.
   - **v4 (`V0_CONF=0.3` global -> `LIMB_IDX` + `enforce_image_lr`, 17/11 10:13–10:23)**: Chỉ đánh `v0` cho tay/chân (`{7,8,9,10,13,14,15,16}`), giữ mặt/vai/hông `Q`, ép R/L theo ảnh.
   - **v5 (`cvat_tools.pose.validate` / `tools.pose17`, 18/11/2026)**: Bổ sung validator 5 lớp (L1–L5), rule engine CSV và audit read-only.

---

## 2. Dữ liệu đối chiếu định lượng

- Bảng tổng hợp 13 phép so sánh snapshot: [`version_comparison.csv`](version_comparison.csv)
- Nhật ký chi tiết 1,605 dòng biến đổi keypoint `(dx, dy, euclidean_distance, visibility_before, visibility_after)`: [`annotation_change_log.csv`](annotation_change_log.csv)
- Nguồn tính toán: [`A02_deltas.json`](agents/A02_deltas.json) và [`A06_geometry_metrics.json`](agents/A06_geometry_metrics.json)
