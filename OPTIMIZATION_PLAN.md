# Optimization Plan (`OPTIMIZATION_PLAN.md`)

## Iteration Loop (`scheduler/optimize_loop.py`)
1. Đọc `checkpoints/best.json` (hoặc tạo `reports/baseline.json` ở iter 0).
2. Thu thập metrics mới nhất qua `cvat_tools.quality.metrics_eval` trên dev (`60–69`) và held-out eval (`70–79`).
3. Xác định top 3 failure patterns theo thứ tự ưu tiên:
   - Priority 1: `building` false positives (`fp_area_rate <= 0.02`)
   - Priority 2: `area/direct` geometry (`f69`, night frames)
   - Priority 3: `lane/*` Boundary F1 @ 3px & cross-frame consistency
4. Ghi `reports/iterations/iter_NNN.json` với đầy đủ: `iteration_id, hypothesis, changed_module, baseline, candidate, delta, regression_result, runtime, peak_ram, decision, next_action`.
5. Chạy `python -m pytest -q`; chỉ giữ thay đổi khi metrics cải thiện và không phá invariant (`invalid_geometry == 0`).
6. Dừng khi đạt `STOP_SUCCESS` hoặc `STOP_LIMIT` (xuất `reports/final_gap_report.md`).

## Resource & Safety Limits
- Max concurrent heavy workers: `3`
- Max iterations: `30` | Max consecutive non-improving: `5`
- Wall-clock budget: `4h` (20 min/experiment) | RAM soft `12GB`, hard `14GB`
- CVAT remote writes: **DISABLED** trong suốt optimization loop.
