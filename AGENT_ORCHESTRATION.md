# Agent Orchestration (`AGENT_ORCHESTRATION.md`)

## 6 Logical Agent Roles (Max 3 Concurrent Heavy Workers on 16GB RAM)
- **Agent A — Ground Truth & Metrics**: Kiểm tra gold set duyệt độc lập, tách sequence dev/eval, tính BBox/Seg/Boundary F1/Invalid geometry.
- **Agent B — Semantic Perception**: Đánh giá model local (`YOLO26l`, `SegFormer-B2`, `SegFormer-Lane-Marking`) trên CPU/16GB RAM, phân loại FP, không tải model mới khi chưa cần.
- **Agent C — Geometry Refinement**: Tối ưu polygon (`geomrefine.py`), giữ topology (`invalid=0`), không ép `building` thành rectangle khi hình học không hỗ trợ.
- **Agent D — CVAT Integration**: Tương thích CVAT v2.74.1, bảo toàn schema (`shape_type`, `label`, `attributes`, `frame`, `occluded`, `z_order`), dry-run/backup/diff/rollback.
- **Agent E — Visual QA**: Đối chiếu RGB gốc vs output (ưu tiên `f69` và cảnh đêm), liệt kê lỗi theo severity.
- **Agent F — Optimizer & Benchmark**: Benchmark, ablation, tối ưu latency/RAM, chọn checkpoint tốt nhất.

## Execution & Fallback Notes
- Môi trường hỗ trợ `invoke_subagent` chạy tối đa **3 worker nặng đồng thời**; nếu không hỗ trợ, chạy tuần tự từng module qua CLI `python -m cvat_tools ...`.
- **Lưu ý Cron / Scheduler**: Local scheduler (`scheduler/optimize_loop.py`) phụ thuộc vòng đời process/VS Code (nếu đóng VS Code hoặc dừng process thì scheduler dừng). Không thay thế runtime agent bằng cron giả.
