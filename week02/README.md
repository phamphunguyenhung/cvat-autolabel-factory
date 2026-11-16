# CVAT tuần 2 (cvat.edufun.ai, org cohort-5a, nhóm G06)

Mỗi tuần một thư mục, mỗi task một thư mục con (có `TASK.md`), mỗi job một thư mục con (có `SPEC.md`).
Danh sách job máy đọc nằm ở `../weeks/2026-W47.yaml`; guideline ở `../weeks/guidelines/w2-face50-pose17.md`.

| Task | Tên | Job của mình | Loại | Ghi chú |
|---|---|---|---|---|
| [473](task473-face/TASK.md) | `W2-FACE-G6-T1` | [1975](task473-face/job1975-face50/SPEC.md) (frame 90–119) | face landmark 50 điểm, 7 skeleton | mình là leader, task có 5 job |
| [402](task402-pose/TASK.md) | `week2-human-pose/G06` | [1623](task402-pose/job1623-pose17/SPEC.md) (frame 90–119) | pose COCO 17 điểm | chỉ thấy job này (task trả 403) |

Mỗi thư mục job: `backups/` (backup trước khi ghi lên CVAT, không commit), `drafts/` (nháp local), `metrics/`, `review/` (ảnh overlay, ghi chú QC).
Dữ liệu máy sinh (labels.json, overlay) nằm ở `../data/jobs/edufun/<job_id>/`.

Xem nhanh job: `python -m cvat_tools week status`.
