# So sánh model/tracker (đo thật trên máy này)

Máy: i7-8850H (6C/12T, AVX2, **không AVX512**), 15,8 GB RAM, CPU-only, Windows 11, Ultralytics 8.4.202, OpenVINO 2026.4.1, ONNX Runtime 1.27.0, torch 2.13 CPU.
Dữ liệu: MOT17-09 (150 ảnh 1920x1080, **không có gt.txt**), đoạn tuần tự frame 0..29 (detector) và 0..59 (ablation). Tiến trình nền khác
(`scene_model_eval.py`, `bbox_all_draft.py`) chen vào CPU nên có hàng bị nhiễu (cột `noisy`). Số của nhà sản xuất Ultralytics KHÔNG dùng ở đây.

## Detector, 30 frame, imgsz 640 trừ khi ghi khác (lượt sạch: `cpu_load_before` 3-11%) — `data/benchmarks/detector_bench.csv` (10 dòng cuối)
| Model | Backend | median ms | P95 ms | FPS (trung bình) | Peak RAM MB |
|---|---|---|---|---|---|
| yolo26l | PyTorch @1920 (baseline hiện tại của mtm) | 2622 | 2956 | 0,38 | 1223 |
| yolo26l | PyTorch | 319 | 354 | 3,1 | 660 |
| yolo26s | PyTorch | 104 | 126 | 9,4 | 480 |
| yolo26s | ONNX Runtime | 131 | 150 | 7,5 | 570 |
| yolo26s | OpenVINO FP32 | 57 | 465 | 6,6 | 840 |
| yolo26s | OpenVINO FP16 | 65 | 412 | 6,1 | 804 |
| yolo26s | OpenVINO FP32 @960 | 158 | 690 | 4,3 | 914 |
| yolo26n | PyTorch | 56 | 84 | 16,8 | 394 |
| yolo26n | ONNX Runtime | 56 | 87 | 16,5 | 465 |
| yolo26n | OpenVINO FP32 | 95 | 262 | 8,4 | 728 |

Nhận xét trung thực: OpenVINO có **median** tốt hơn cho 26s nhưng đuôi độ trễ rất dài (P95 gấp 4-8 lần median; nghi do nhiễu từ tiến trình khác
hoặc khởi động luồng, chưa tách được nguyên nhân) nên thông lượng thực thấp hơn PyTorch; với 26n OpenVINO chậm hơn PyTorch/ONNX. Chưa kết luận
"OpenVINO nhanh hơn" cho máy này. Lượt đo đầu (cùng file, 10 dòng đầu) bị nhiễu nặng (tải 57-85%): baseline @1920 khi đó 5,4 s/frame.
**INT8: BLOCKED** (không có dữ liệu hiệu chuẩn đại diện và không có GT để biết có làm mất người không). **FP16**: chạy được, chất lượng chưa đánh giá.
**Recall/mAP: không đo được** (không GT). Chỉ có `pseudo_recall_vs_A` (độ khớp với YOLO26l@1920, không phải recall).

## Tracker trên CÙNG detection cache (yolo26s/openvino/640, 60 frame) — `data/benchmarks/tracker_bench.csv`
| Tracker | association median/P95 ms | track thô | track ≥30f | đứt | liên tục neo P1-P5 (heuristic) |
|---|---|---|---|---|---|
| bytetrack | 1,2 / 1,9 | 15 | 6 | 0 | 0,897 |
| ocsort | 1,8 / 2,7 | 15 | 7 | 0 | 0,927 |
| fasttrack | 1,4 / 1,9 | 16 | 6 | 0 | 0,875 |
| deepocsort (không ReID) | 2,0 / 3,3 | 13 | 7 | 0 | 0,943 |
| botsort (không ReID, GMC) | 19,1 / 26,0 | 15 | 6 | 0 | 0,897 |
| tracktrack (không ReID, GMC) | 18,6 / 23,1 | 8 | 5 | 0 | **1,000** |

Association chỉ ~1-26 ms/frame so với detector 57-300 ms: **chọn tracker theo độ liên tục, không theo tốc độ**. Đây là chỉ số heuristic, không phải
IDF1/HOTA/MOTA (không GT); "liên tục neo" chỉ đo track chứa điểm neo P1-P5 có phủ liền mạch không, không đo có đúng người không.
