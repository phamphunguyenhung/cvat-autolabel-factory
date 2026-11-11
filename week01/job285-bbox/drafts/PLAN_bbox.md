# Nháp bbox job 285 (29 hộp, chưa ghi CVAT)

Ghi lên CVAT sau khi duyệt: `python scripts/bbox_draft.py --job 285 --apply-draft latest`
Ảnh duyệt: `tools/cvat-seg-copilot/out/bboxall_job285/overlay_<frame>.jpg` (trắng = hộp tay, màu = nháp).

| label | số hộp nháp | nguồn |
|---|---|---|
| car | 15 | YOLO26l |
| traffic light | 14 | YOLO26l |

Không vẽ: lane/* (label polyline), area/drivable, area/alternative (chưa có model), person/traffic_light/traffic_sign (trùng nghĩa).
Vegetation/terrain/wall/fence bỏ vùng tối (độ sáng TB < 40) vì ảnh đêm model nhận nhầm.
Bỏ hộp trùng hộp tay (IoU>=0.5). Hộp SegFormer là hộp bao vùng stuff, cần duyệt kỹ.
