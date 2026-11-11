# CVAT tuần 1 (cvat.edufun.ai, org cohort-5a)

Gán nhãn thực hành trên server CVAT của lớp. Mỗi tuần một thư mục, mỗi job một thư mục con có `SPEC.md`
(yêu cầu thật của job). **Không áp taxonomy của lab Day 3 (road/sidewalk/building...) vào các job này.**

| Job | Task | Ảnh | Loại | Trạng thái |
|---|---|---|---|---|
| [987](job987-seg/SPEC.md) | 227 | `week1-seg/G06`, frame 60-79 | seg: mask + polyline lane | polygon đã đổi sang mask (19:00 11/11/2026), cron đo metric |
| [285](job285-bbox/SPEC.md) | 87 | `week1-bbox/G06`, frame 60-79 | bbox (rectangle) | 138 bbox (đã dedupe 23), metric `bbox_metrics.py`, 36 hộp YOLO thấy mà thiếu đang chờ duyệt |

Tool: `tools/cvat-seg-copilot` (CLI `cvat-seg`, `scripts/mask_metrics.py`). Chọn server bằng file env
(`.env.edufun` cho cvat.edufun.ai, `.env.localhost` cho CVAT local), copy thành `.env.local` của tool.
Backup và metric của từng job nằm trong `backups/` và `metrics/` cạnh `SPEC.md` (không commit backup).
