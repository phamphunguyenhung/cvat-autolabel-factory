# Standard Workflows (Mọi CVAT Job Mới)

```powershell
# 1. Kiểm tra môi trường & kết nối (read-only)
python -m cvat_tools doctor
python -m cvat_tools tools list
python -m cvat_tools models list

# 2. Khảo sát job & lưu nhãn gốc hiện có (nếu có) vào ShapeStore local
python -m cvat_tools job preflight --job <JOB_ID>
python -m cvat_tools store capture --job <JOB_ID>

# 3. Sinh draft tự động (local-only, không ghi CVAT) & xem preview
python -m cvat_tools run --job <JOB_ID>
python -m cvat_tools full-bbox --job 285 --open

# 4. Kiểm tra thống kê & dry-run trước khi đồng bộ
python -m cvat_tools store stats --job <JOB_ID>
python -m cvat_tools store push --job <JOB_ID>         # dry-run mặc định

# 5. Chỉ ghi thật khi đã duyệt kỹ; có thể rollback an toàn
python -m cvat_tools store push --job <JOB_ID> --yes
python -m cvat_tools store rollback --latest --job <JOB_ID>      # dry-run
python -m cvat_tools store rollback --latest --job <JOB_ID> --yes
```
