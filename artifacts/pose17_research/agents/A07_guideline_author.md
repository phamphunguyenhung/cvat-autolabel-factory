# A07 — Guideline Author Report

**Task:** Pose17 Gold Reference & Guideline Engine (`Task 402` / `Job 1623`)  
**Role:** A07 — Guideline Author | **Date:** 2026-11-18  

---

## 1. Files Created
1. **Tier A (G06-specific):** [G06_POSE17_GUIDELINE.md](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/docs/guidelines/pose17/G06_POSE17_GUIDELINE.md)
   - Đầy đủ 13 mục theo yêu cầu: bối cảnh Task 402/Job 1623, cấu hình CVAT (`person_vf17`, 18 SVG edges vs 19 COCO edges, sublabels `12323..12339`), đặc điểm dataset (18 IR + 12 RGB, 3 độ phân giải, low-light/fisheye), bảng 17 keypoint, quy tắc R/L (BTC image-based + caveat ảnh xoay 90°), quy tắc visibility (cấm `hidden`, cấm `occ+out`, cấm bulk-occlude), occlusion & inference (`±5/±20 px`), truncation/out-of-frame, 7 nhóm lỗi thường gặp (`f093`, `f100/f118`, `f101`, `f117`, `f116`, `f113`, `22` `occ+out`), case khó đã xử lý & chưa kết luận, liên kết overlay trực quan, thay đổi qua các version (3 trục), và bài học từ human-edit deltas (`25/28` frames, `148` dịch chuyển, `51` đổi trạng thái).
2. **Tier B (General Pose17):** [POSE17_GENERAL_GUIDELINE.md](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/docs/guidelines/pose17/POSE17_GENERAL_GUIDELINE.md)
   - Định nghĩa **30 rule ID ổn định (`P17-G01` – `P17-G30`)** phân loại rõ `source_type` (`BTC_OFFICIAL`, `USER_OBSERVED`, `GEOMETRIC_INFERENCE`, `AI_RECOMMENDATION`), `source_ref`, `confidence`, và `status`.
3. **Changelog & Governance:** [GUIDELINE_CHANGELOG.md](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/docs/guidelines/pose17/GUIDELINE_CHANGELOG.md)
   - Ghi nhận lịch sử theo 3 trục phiên bản (Guideline, Annotation, Tool/Pipeline) và quy trình 4 bước đề xuất rule mới (`proposed` -> evidence review -> `approved` / `needs_mentor`).
4. **Agent Report:** [A07_guideline_author.md](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/agents/A07_guideline_author.md)

---

## 2. Assigned Rule IDs (`P17-G01` – `P17-G30`)
- **`BTC_OFFICIAL` (`19` rules, `approved`):** `P17-G01`–`P17-G07`, `P17-G10`–`P17-G16`, `P17-G18`–`P17-G22`.
- **`GEOMETRIC_INFERENCE` (`5` rules):** `P17-G23` (`approved`), `P17-G24` (`proposed`), `P17-G25` (`proposed`), `P17-G08` (`needs_mentor`), `P17-G26` (`needs_mentor`).
- **`AI_RECOMMENDATION` (`5` rules, `approved`):** `P17-G09`, `P17-G27`, `P17-G28`, `P17-G29`, `P17-G30`.
- **`USER_OBSERVED` (`1` rule, `proposed`):** `P17-G17` (ghi nhận anomaly `eye/ear outside` trong khung và `occ+out`, không promote thành rule chính thức).

---

## 3. Open `needs_mentor` Items
1. **`P17-G08` (Horizontal / 90°-rotated R/L):** Tiêu chí chọn R/L khi hai bên gần trùng tọa độ `x` (`f96, f103, f105, f106, f110, f112`).
2. **`P17-G26` (Resolution-normalized tolerance):** Có scale ngưỡng `±5 px` / `±20 px` theo độ phân giải (`1280×1024`, `512×424` vs `960×540` của BTC) hay giữ nguyên pixel tuyệt đối (`issues.md` A1).
3. **Label naming & `source=file` policy (`issues.md` A3, A6):** Xác nhận `person_vf17` tương đương `person` của BTC, và quy tắc chỉnh sửa/vẽ lại 10 frame gốc `source=file`.
4. **Scoring & minimum size (`w2-face50-pose17.md` §8 Q4, Q8):** Cách chấm điểm `outside` và ngưỡng kích thước người tối thiểu trong IR tối (`MIN_PERSON_PX=60`).
