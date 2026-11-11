# Nháp bbox job 285 (232 hộp, chưa ghi CVAT)

Ghi lên CVAT sau khi duyệt: `python scripts/bbox_draft.py --job 285 --apply-draft latest`
Ảnh duyệt: `tools/cvat-seg-copilot/out/bboxall_job285/overlay_<frame>.jpg` (trắng = hộp tay, màu = nháp).

| label | số hộp nháp | nguồn |
|---|---|---|
| building | 35 | SegFormer |
| car | 30 | YOLO26l |
| fence | 8 | SegFormer |
| pedestrian | 8 | YOLO26l |
| pole | 48 | SegFormer |
| road | 21 | SegFormer |
| sidewalk | 7 | SegFormer |
| sky | 9 | SegFormer |
| terrain | 1 | SegFormer |
| traffic light | 22 | YOLO26l |
| traffic sign | 18 | SegFormer |
| truck | 2 | YOLO26l |
| vegetation | 22 | SegFormer |
| wall | 1 | SegFormer |

Không vẽ: lane/* (label polyline), area/drivable, area/alternative (chưa có model), person/traffic_light/traffic_sign (trùng nghĩa).
Vegetation/terrain/wall/fence bỏ vùng tối (độ sáng TB < 40) vì ảnh đêm model nhận nhầm.
Bỏ hộp trùng hộp tay (IoU>=0.5). Hộp SegFormer là hộp bao vùng stuff, cần duyệt kỹ.

## Đánh giá sau khi xem overlay (11/11 22:20)
- Tin được: hộp vật thể YOLO (car, truck, pedestrian, traffic light) và traffic sign; pole cần xem.
- Kém: hộp stuff SegFormer (road, sky, vegetation, building, sidewalk, fence, terrain, wall) là hộp bao cả vùng, to và chồng nhau, ít giá trị cho bbox. Chỉ giữ nếu thầy cô yêu cầu vẽ.
