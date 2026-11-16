# Metrics Specification (`METRICS.md`)

## Ground Truth & Split Discipline
- Ground truth hợp lệ: `human_final` đã được annotator duyệt độc lập (tách khỏi `rule_draft` / `ai_draft`).
- Không tối ưu trực tiếp trên held-out eval set:
  - **Dev set**: frames `60–69`
  - **Held-out Eval set**: frames `70–79`

## Implemented Metrics (`src/cvat_tools/quality/metrics_eval.py`)
1. **BBox (`rectangle`)**: IoU, `mAP@0.50`, per-label Precision / Recall (chỉ chấm draft AI đối chiếu GT, không tự chấm `cvat_human`).
2. **Segmentation (`polygon`)**: Rasterized mask `IoU`, `Macro mIoU`, `Boundary F1 @ 3px`, `building` FP area rate (`FP_px / frame_px`).
3. **Lane & Area**: `lane/*` Boundary F1 @ 3px; `area/direct` IoU và containment trong `road`.
4. **Geometry Integrity**: Số shape invalid (`shapely.is_valid == False` hoặc `< 3` đỉnh) — bắt buộc `= 0`.
5. **Telemetry**: Runtime (s), Peak RSS (MB) qua `psutil`.
