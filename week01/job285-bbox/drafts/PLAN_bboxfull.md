# Nháp bbox/polygon job 285 (27 hình, chưa ghi CVAT)

Ghi sau khi duyệt: `python scripts/bbox_all_draft.py --job 285 --apply-draft latest`
Ảnh duyệt: `tools/cvat-seg-copilot/out/bboxfull_job285/overlay_<frame>.jpg` (trắng = hộp tay, màu = nháp).

| label (hình) | số nháp |
|---|---|
| fence (polygon) | 4 |
| pole (polygon) | 12 |
| sidewalk (polygon) | 9 |
| terrain (polygon) | 2 |

Loại trừ vì trùng nghĩa/không có model: lane/double other, lane/single other, person, traffic_light, traffic_sign.
