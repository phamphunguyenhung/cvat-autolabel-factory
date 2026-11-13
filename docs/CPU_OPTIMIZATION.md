# Tối ưu CPU-first (bbox + tracking)

## Kiểm kê phần cứng/phần mềm (đo trực tiếp)
- CPU i7-8850H 6C/12T, AVX2 (torch báo `AVX2`; không AVX512), RAM 15,8 GB, không GPU. Ultralytics 8.4.202; OpenVINO 2026.4.1 (cài mới cho CET);
  ONNX Runtime 1.27.0.
- Tracker có trong cài đặt (đọc `ultralytics/cfg/trackers`): bytetrack, botsort, ocsort, deepocsort, tracktrack, fasttrack. Không có boxmot/motcpp.
- Checkpoint: trước đó chỉ có `yolo26{s,m,l}-seg.pt` (seg) và yolo11; **không có yolo26 detect, không có yolo26n**. Đã tải `yolo26{n,s,l}.pt`
  (detect) vào `models/checkpoints/` (gitignored; sha256 trong `config/models.yaml`).
- MOT17-09: 150 ảnh có tại `day05/labs/K5-L2-MOTTracking/.lab-local/mot17-09`, **không có gt.txt**.

## Baseline trước khi tối ưu
YOLO26l PyTorch @1920 (mặc định của `mtm`): **median 2,62 s/frame, 0,38 FPS, peak RAM 1,2 GB** (lượt sạch). Tracker hiện tại botsort.

## Ablation A-G (60 frame tuần tự, `data/benchmarks/ablation.csv`)
| ID | Model | Tracker | Res | Backend | FPS e2e | Peak RAM MB | Recall | IDF1 | Keyframes (tối ưu) | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| A | 26l | botsort | 1920 | PyTorch | 0,30* | 1223 | n/a (tham chiếu) | n/a (no GT) | 50 | measured (noisy) |
| B | 26n | bytetrack | 640 | OpenVINO | 11,4* | 728 | giống A 0,843 (pseudo) | n/a | 54 | measured (noisy) |
| C | 26s | tracktrack | 640 | OpenVINO | 6,5* | 843 | giống A 0,887 (pseudo) | n/a | 56 | measured (noisy) |
| D | 26s | ocsort | 640 | OpenVINO | 7,4* | tracker-only** | 0,887 (pseudo) | n/a | 52 | measured (noisy) |
| E | 26s | fasttrack | 640 | OpenVINO | 7,4* | tracker-only** | 0,887 (pseudo) | n/a | 45 | measured (noisy) |
| F | 26s | tracktrack+ReID chọn lọc | 640 | OpenVINO | — | — | — | — | — | **BLOCKED**: thiếu trọng số OSNet x0.25 |
| G | 26s + 26l@1280 cho frame khó | tracktrack | 640/1280 | OpenVINO | 1,05* | 1782 | giống A 0,965 (pseudo) | n/a | 72 | measured (noisy) |

\* Detector đo lúc tải CPU 43-87% do tiến trình nền khác: dùng để xếp thứ tự thô, không phải con số cuối. Lượt detector sạch ở MODEL_COMPARISON.md.
\** D/E dùng lại detection cache của C nên peak RAM chỉ gồm tracker (không gồm detector): không so sánh được.
"Recall (pseudo)" = tỉ lệ detection conf≥0,5 của A mà cấu hình này cũng thấy (IoU≥0,5); A là tham chiếu giả, không phải nhãn thật.
Người nhỏ (<100 px cao): B-E khớp A **0%**, G 50% (mẫu nhỏ) -> nghi 640 px bỏ sót người nhỏ; chưa chứng minh vì không GT.
**Số keyframe khác nhau giữa các dòng chủ yếu phản ánh độ rung của track, không phải chất lượng.** Hàm heuristic frame khó của G chọn lại **78%**
frame (47/60) nên chi phí cao, lợi ích chưa kiểm chứng: cần siết ngưỡng trước khi dùng QUALITY.

## Keyframe optimizer (`tracking/keyframes.py`)
Quy hoạch động tìm tập keyframe NHỎ NHẤT với sai số nội suy tuyến tính (chuẩn CVAT) ≤ tol ở mọi frame; luôn giữ frame vượt dung sai,
vào/ra khung, biên khoảng trống. Sự kiện (đổi hướng, đổi tỉ lệ, gia tốc, giao nhau) được liệt kê và có thể ép giữ (`keyframes_with_events`).
Kết quả thật (bytetrack, P1-P5 theo neo, 60 frame, tol 4px): 270 box → Douglas-Peucker 56 → tối ưu **50** (-11% so với DP, -81% so với mỗi frame),
sai số tối đa 3,97 px. Trên nháp job15 cũ: P2 56→43, P3 55→44. Quyết định ID không chắc chắn không tự chọn: chuyển sang review queue.

## Profile đã chọn (`config/profiles.yaml`) và lý do
- **balanced = 26s + OpenVINO + TrackTrack, 640** (mặc định; 960 chỉ khi có GT chứng minh lợi ích: chậm 2,7x). Lý do: TrackTrack cho độ liên tục neo 1,0 và ít track thô
  nhất (8) trên cùng detection; chi phí association ~19 ms không đáng kể.
- **fast = 26n + ONNX + ByteTrack, 640**: đổi OpenVINO→ONNX vì lượt sạch cho thấy OpenVINO chậm hơn cho 26n. Chất lượng liên tục thấp hơn (0,887, 6 đứt).
- **quality**: chưa chốt; cần siết heuristic frame khó (đang 78%) và có OSNet.
- Chưa claim cải thiện chất lượng: không có GT/held-out. Không retrain (recall detector chưa chứng minh là nút thắt).

## ReID / adapter nghiên cứu
`tracking/reid.py`: ReID chọn lọc, embedding cache theo (frame, det id, hash model), `auto_relabel: False` luôn; OSNet x0.25 BLOCKED (thiếu trọng số).
Adapter nghiên cứu (motcpp, LITE, SFSORT): **không làm** — không có sẵn trong cài đặt, chưa xác nhận tương thích/lợi ích; không cài thêm.
