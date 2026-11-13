# Kiểm kê và migrate

## Inventory (đo ngày 2026-11-13)
| Tool | Đường dẫn | Mục đích | Lệnh | Phụ thuộc | Trạng thái | Tái dùng | Rủi ro |
|---|---|---|---|---|---|---|---|
| mot-track-manager | `tools/mot-track-manager` (git riêng, 1 commit checkpoint) | nháp track MOT, QA, MOT 1.1, ghi CVAT an toàn | `mtm inspect/draft/bench/apply/check/export/rollback` | requests numpy opencv ultralytics pyyaml | chạy; 9 test đạt | cao | thấp (đã copy, bản gốc giữ nguyên) |
| skeleton-pose-manager | `tools/skeleton-pose-manager` (git riêng, gitignored ở repo gốc) | nháp skeleton Day 4 | `spm ...` | như trên | chạy; job 12/13 đã ghi | client/writer trùng ~90% với mtm | trung bình (chưa hợp nhất, chỉ adapter) |
| cvat-seg-copilot | `tools/cvat-seg-copilot` (git riêng, **tiến trình nền đang dùng**) | segmentation Day 3 (SegFormer/SAM, bbox, audit) | `cvat-seg ...`, `scripts/*.py` | typer, cvat-sdk, ultralytics, shapely... | chạy; nhiều thay đổi chưa commit | draftstore/auth/audit | cao: không đụng |
| tools/legacy | `tools/legacy` | script Day 2/3 cũ | — | — | lưu trữ | thấp | — |
| week01 | `cvat/week01` | nháp job285/987, metrics, SPEC | — | — | giữ nguyên | dữ liệu | không đụng |
| Checkpoint | `tools/cvat-seg-copilot/*-seg.pt`, `skeleton-pose-manager/models/yolo11l-pose.pt` | seg/pose | — | — | **không có yolo26 detect/yolo26n** trước đây | — | không commit |

## Đã làm
- `core/client.py` ← `mtm.cvat` + `spm.cvat` (gộp, thêm khóa chỉ-đọc, profile, tasks/jobs).
- `core/transactions.py` ← logic backup/run-log/rollback của `mtm.writer`/`spm.writer`.
- `core/draftstore.py` ← `scripts/draftstore.py` (seg-copilot) + `mtm.draft.save_draft`. `core/cache.py`: mới.
- `tracking/{geometry,draft,writer,cli}.py` ← `mtm.{core,draft,writer,cli}` (geometry copy nguyên, 9 test cũ chạy nguyên văn ở `tests/legacy_mtm`).
- `src/mtm/*`: wrapper `python -m mtm` -> `cvat_tools.tracking`.

## Chưa làm (inventory + adapter mỏng)
- Pose (`spm`): hợp nhất client/writer vào core; giữ `schema/templates/transforms/validator` làm `cvat_tools/pose`.
- Segmentation (`cvat_seg`): chỉ đọc; không move vì tiến trình nền dùng `scene_model_eval.py`/`bbox_all_draft.py`.
- `training/`, `export/`: thư mục trống.

## Rollback
Bản gốc `tools/mot-track-manager` giữ nguyên (commit checkpoint `05355cf` trong repo của nó). Để quay lại: dùng `python -m mtm` từ thư mục đó
(`$env:PYTHONPATH="src"`), hoặc `git reset --hard HEAD~1` ở repo gốc để bỏ commit CET (không đụng week01).
