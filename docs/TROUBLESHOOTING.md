# Xử lý sự cố

| Triệu chứng | Nguyên nhân / cách xử lý |
|---|---|
| `CVAT: khong ket noi duoc` | Docker CVAT chưa chạy (`http://localhost:8080`). Các test và phần đọc cache/fixture vẫn chạy. |
| `Thieu CVAT_PAT` | Tạo `cvat\.env` (xem `.env.example`) hoặc đặt `$env:CVAT_PAT`. Fallback: `tools\mot-track-manager\.env`. |
| `GET /api/jobs/N -> 404` | job id trong `projects/<p>/project.yaml` sai; liệt kê bằng `cvat_tools inspect` hoặc client `jobs()`. MOT17-09 hiện là job 15 (task 17). |
| `DUNG: ... --allow-ai-draft` | Lệnh sinh dự đoán AI bị khóa theo luật Day 5. Chỉ thêm cờ khi được phép hoặc chỉ để đo hiệu năng. |
| `BLOCKED: INT8 can calibration` | INT8 cần dữ liệu hiệu chuẩn đại diện, và cần GT để biết có mất người không. |
| `model=... is not a supported model format` | Thư mục OpenVINO phải kết thúc bằng `_openvino_model` (đã xử lý trong `export_path`). |
| Số đo nhiễu | Tiến trình khác chiếm CPU (`scene_model_eval.py`...). CSV có `cpu_load_before`/`noisy`; dùng `--idle-wait <giây>` để chờ CPU rảnh. |
| OpenVINO tạo `kernel.errors.txt` ở thư mục chạy | Cảnh báo của plugin, vô hại; xóa file. |
| ReID BLOCKED | Thiếu trọng số `models/checkpoints/osnet_x0_25.onnx`. |
