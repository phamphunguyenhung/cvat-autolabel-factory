# Quality Goals & Stop Gates (`GOALS.md`)

## Hard Quality Goals (Held-Out Evaluation Set)
- **BBox**: `mAP@0.50 >= 0.90`, `mAP@0.50:0.95 >= 0.75`, `Mean IoU >= 0.88`
- **Segmentation**: `Macro mIoU >= 0.85`, `Boundary F1 @ 3px >= 0.90`
- **Building**: `False-positive area rate <= 0.02`; không tự sinh từ shape chữ nhật thuần túy; không ép thành rectangle khi hình học thực tế không hỗ trợ.
- **Lane**: `Boundary F1 @ 3px >= 0.92`; giữ polygon hẹp.
- **Area / Direct**: `IoU >= 0.90`; kiểm tra continuity, topology và semantic consistency.
- **General**: `Wrong-label rate <= 0.01`, `Invalid geometry = 0`, `Human correction rate <= 0.10`, `Human correction time reduction >= 70%`, không thiếu hoàn toàn nhãn trọng yếu.

## Priority Order (Job 285 -> General)
1. **Building false positives** (`fp_area_rate <= 0.02`, không mất chi tiết hình học thật)
2. **Area/direct geometry** (đặc biệt frame 69 & các cảnh đêm)
3. **Lane boundary** (`Boundary F1 @ 3px`, yellow/white/double/crosswalk)
4. **Cross-frame consistency** (tách dev/eval theo sequence, tối thiểu >= 20 gold frames đa dạng cảnh)

## Stop Conditions
- **STOP_SUCCESS**: Toàn bộ gates đạt trên held-out eval, `Invalid geometry = 0`, regression pass, CVAT schema pass, có final before/after report.
- **STOP_LIMIT**: Đạt 30 iterations, 5 vòng không cải thiện, hết budget (4h / RAM 14GB), hoặc chưa đủ gold set/chất lượng -> xuất `reports/final_gap_report.md` (tuyệt đối không đổi thành `STOP_SUCCESS`).
