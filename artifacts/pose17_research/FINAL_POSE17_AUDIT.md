# FINAL_POSE17_AUDIT — Job 1623 (Task 402 / Week 2 G06 Pose17)

> **Chế độ thực thi:** READ-ONLY tuyệt đối trên CVAT (`write_enabled=False`). Không có bất kỳ thay đổi nào được ghi lên server CVAT.  
> **Snapshot tham chiếu:** [`job_1623_annotations_raw.json`](snapshots/job_1623_annotations_raw.json) (`sha256: 0fc88cfb9396cb022fb5f4572effb2d0ffc884153e02164b0bc4c6efccc38bbc`)

---

## 1. Tổng hợp số liệu kiểm kê & kiểm chứng

| Chỉ số | Giá trị thực tế | Nguồn xác minh |
|---|---:|---|
| Phạm vi Task 402 / Job 1623 | Task 402 trả **HTTP 403**; Job 1623 có **30 frame** (`90..119`, `G06_091.jpg`–`G06_120.jpg`) | `job_1623.json`, `job_1623_meta.json`, `api_probe.json` |
| Tổng số frame đọc thành công | **30** (`18` IR, `12` RGB; `1280x1024`: 15, `960x540`: 12, `512x424`: 3) | `frame_manifest.csv` |
| Tổng số skeleton | **28** (`person_vf17`, `source="manual"`; frame `100` và `118` có `0` skeleton) | `job_1623_annotations_raw.json` |
| Tổng số keypoint đã kiểm tra | **476** (`359 visible`, `59 occluded_only`, `36 outside_only`, `22 occluded+outside`, `0 hidden`) | `A04_visibility_audit.json` |
| Tổng số case khó | **30** frame (`critical`: 8, `high`: 12, `medium`: 8, `low`: 2) | `docs/guidelines/pose17/difficult_cases.csv` |
| Tổng số findings từ Validator 5 lớp | **157** (`error`: 35, `warning`: 53, `info`: 69) — `L1=2, L2=7, L3=79, L4=19, L5=50` | `VALIDATION_RESULTS.csv` |
| Trạng thái frame (Validator) | `pass`: **2** (`f90, f115`), `warn`: **11**, `fail`: **17** | `FRAME_COVERAGE.csv` |
| Số case đã liên kết guideline | **30 / 30** (`0` thiếu `rule_id`) | `A09_independent_qa.md` |
| Số case thiếu ảnh bằng chứng | **0 / 30** (`30` overlay trong `evidence/overlays/`, `6` before/after trong `evidence/before_after/`) | `A09_independent_qa.md` |
| Số đề xuất sửa lỗi (Read-only) | **39** (`status=proposed_for_human_review`) | `proposed_corrections.csv` |
| Số rule trong hệ thống | **30** (`P17-G01`..`P17-G30`) | `docs/guidelines/pose17/pose17_rules.csv` |
| Rule trên Guideline chung (`POSE17_GENERAL_GUIDELINE.md`) | **25** `approved` (`19 BTC_OFFICIAL`, `1 GEOMETRIC_INFERENCE`, `5 AI_RECOMMENDATION`); **2** `needs_mentor`; **3** `proposed` | `POSE17_GENERAL_GUIDELINE.md` |
| Tình trạng truy vết v1/v2 | Truy vết được **13** cặp chuyển đổi cục bộ (`1,605` dòng delta); lịch sử CVAT `/api/events` (**HTTP 500**) và trước `2026-11-16 17:50:14` ghi `history_unavailable` | `VERSION_HISTORY.md`, `version_comparison.csv` |
| Kết quả Unit Tests (`pytest`) | **283 passed** toàn repo (`tests/test_pose17_validate.py`: **8 passed**) | `A10_integration_engineer.md`, `A09_independent_qa.md` |

---

## 2. Phân bố findings theo lớp kiểm tra (Validator L1–L5)

| Lớp kiểm tra | Số lượng | Nội dung chính phát hiện trên Job 1623 |
|---|---:|---|
| `L1_STRUCTURAL` | 2 | Frame `100` (`G06_101.jpg`) và frame `118` (`G06_119.jpg`) thiếu skeleton (`0` shape) |
| `L2_GEOMETRIC` | 7 | Trùng điểm `< 3 px` (`f101` `2=4` cách `0.27 px`, `f091` `3/5` ~2 px, `f104` `2/4` ~2.2 px); đảo/chéo R-L thật theo trục thân (`f93` gối `14/15`, `f113` cổ tay `10/11`, `f110` cổ tay `10/11`, `f112` cổ tay `10/11`); `f114` `forearm_R` `48.83 px` (`0.139x` thân) |
| `L3_SEMANTIC` | 79 | `22` xung đột `occluded=True AND outside=True`; `1` skeleton-level bulk `occluded=True` (`f93`); `9` điểm mắt/tai (`2,3,4,5`) đặt `outside` sâu trong khung hình; `56` điểm `outside` nằm sâu trong khung (`dist >= 8 px`) |
| `L4_CROSS_CASE` | 19 | Xác định dataset gồm ảnh độc lập đa độ phân giải (`512x424`, `960x540`, `1280x1024`), không giả định liên tục thời gian; cảnh báo xoay ngang / side-view |
| `L5_EVIDENCE_QA` | 50 | Cờ tham khảo (advisory-only) từ độ sáng thấp (`18` frame IR `mean_luma` 12.8–36.4), nhòe chuyển động (`f100`), và đối chiếu VLM (`0` tự động nâng lên ground truth) |

---

## 3. Những điểm còn chưa chắc chắn & cần chốt

1. **Phạm vi Task 402 (`0..89`)**: Tài khoản `2A202604062` bị **HTTP 403** với `/api/tasks/402`, chỉ đọc được Job 1623 (`90..119`). Không suy diễn dữ liệu của các job khác.
2. **Gold Reference (`gold=0`)**: Chưa có tập gold độc lập được mentor/người gán nhãn duyệt qua từng điểm; trạng thái `source="manual"` hiện tại vẫn chứa 39 lỗi đề xuất trong `proposed_corrections.csv`.
3. **Rule `needs_mentor`**:
   - `P17-G08`: Quy ước phân định R/L khi thân người nằm ngang 90° (`f103, f106, f110, f112`) mà hai bên cùng tọa độ `x`.
   - `P17-G26`: Có scale ngưỡng sai số `±5 px / ±20 px` theo độ phân giải thực tế (`512x424`, `960x540`, `1280x1024`) hay giữ cố định theo BTC V1.
4. **Cơ chế cập nhật**: Chạy lại `python -m tools.pose17 validate --job 1623` và `python -m tools.pose17 build-guideline --job 1623` đảm bảo idempotent (không sinh trùng dòng) và bảo toàn các rule `approved`.

---

## 4. Báo cáo thành phần & Đường dẫn kết quả

- Guideline G06 (Tầng A): [`docs/guidelines/pose17/G06_POSE17_GUIDELINE.md`](../../docs/guidelines/pose17/G06_POSE17_GUIDELINE.md)
- Guideline chung Pose17 (Tầng B): [`docs/guidelines/pose17/POSE17_GENERAL_GUIDELINE.md`](../../docs/guidelines/pose17/POSE17_GENERAL_GUIDELINE.md)
- Changelog & cơ chế đề xuất rule: [`docs/guidelines/pose17/GUIDELINE_CHANGELOG.md`](../../docs/guidelines/pose17/GUIDELINE_CHANGELOG.md)
- Machine-readable rules & cases: [`pose17_rules.csv`](../../docs/guidelines/pose17/pose17_rules.csv), [`difficult_cases.csv`](../../docs/guidelines/pose17/difficult_cases.csv)
- Đề xuất sửa lỗi (Read-only): [`proposed_corrections.csv`](proposed_corrections.csv)
- Báo cáo chi tiết đi kèm: [`DIFFICULT_CASE_REPORT.md`](DIFFICULT_CASE_REPORT.md), [`VERSION_ANALYSIS.md`](VERSION_ANALYSIS.md), [`VERSION_HISTORY.md`](VERSION_HISTORY.md)
- Báo cáo 10 subagent: [`agents/A01_cvat_reader.md`](agents/A01_cvat_reader.md) .. [`agents/A10_integration_engineer.md`](agents/A10_integration_engineer.md)
