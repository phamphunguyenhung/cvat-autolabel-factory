# An toàn ghi CVAT

1. `Cvat` client mặc định **chỉ đọc**: `create_*`/`delete_*` ném `WriteNotAuthorized` nếu không khởi tạo `write_enabled=True` (có test).
2. Không có lệnh nào của `python -m cvat_tools` ghi lên CVAT. Ghi thật chỉ qua `python -m mtm apply --yes` (hai khóa: `--yes` và client write_enabled).
3. `apply`: dry-run mặc định; backup annotation trước khi ghi (`data/backups`); chỉ `PATCH action=create`; bỏ qua track trùng người đã có
   (cùng box ≥10 frame); đọc lại và xác minh; run log (`data/runs`) ghi `created_ids` và `provenance: ai_draft`.
4. `rollback` chỉ xóa đúng id trong run log; track của người dùng không bao giờ bị xóa (có test).
5. Track ghi lên CVAT có `source: manual` để người gán sửa như nhãn của mình; nguồn gốc AI chỉ lưu trong run log/draft. Không dùng nó để
   khai báo nhãn AI là nhãn người.
6. PAT chỉ đọc từ `.env` (gitignored) hoặc biến môi trường, không in. `*.pt`, `*.onnx`, `models/`, `data/` bị gitignore.
7. Ground truth: không có `gt.txt` thì không báo IDF1/MOTA/HOTA; chỉ số heuristic được gắn nhãn "heuristic".
8. Kho shape cục bộ (`data/store/shapes.sqlite`, gitignore): `python -m cvat_tools store push` dry-run mặc định, ghi thật cần `--yes` (client write_enabled); chỉ thêm, dedupe, backup + run log (`kind: shapes`), rollback giữ shape người đã sửa. `store capture` chỉ đọc CVAT.
