# Kiến trúc CET

```
config/ (cvat.*, models, profiles, tracking)   projects/<p>/project.yaml
        |                                              |
core: client(read-only default) · transactions · cache(content-addressed) · config · draftstore
        |
detection: Detector(pytorch|onnx|openvino, lazy) -> detect_cached (key = nguồn + frame + hash ckpt + cấu hình) -> adaptive (frame khó)
        |
tracking: engine (ultralytics trackers trên detection đã cache, tuần tự, reset) -> geometry/keyframes/reid/writer
        |
quality: assist (người tự gán, chỉ đọc) · review (queue + HTML)       benchmark: detector · tracker · ablation · figures
```
- Biểu diễn track độc lập tracker: `{track_id: {frame: [x1,y1,x2,y2]}}` + `scores` + provenance `ai_draft`; P1-P5 là ánh xạ của người duyệt.
- Khóa cache: `make_key(source identity, frame range, ckpt sha256, backend, imgsz, conf, iou)`; đổi bất kỳ thứ nào là cache miss (có test).
- Mỗi tracker thấy CÙNG detection; thời gian detector và association tách riêng.
- `mtm` là wrapper (`src/mtm/*`) trỏ vào `cvat_tools.tracking`; test cũ chạy nguyên văn.
- Giới hạn tài nguyên: `profiles.yaml.limits.threads` truyền vào detector; `ram_mb` là ngưỡng tham chiếu (chưa cưỡng chế).
