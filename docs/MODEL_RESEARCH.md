# MODEL_RESEARCH — đề xuất model cho nhãn còn thiếu (R6, 14/11/2026)

Phạm vi: nghiên cứu tài liệu, KHÔNG chạy model, KHÔNG tải checkpoint. Ký hiệu độ tin cậy:
- **[N]** = đã đọc trực tiếp từ trang nguồn (URL kèm theo).
- **[S]** = suy đoán / chưa xác minh; phải đo trước khi tin.
- "không tìm thấy" = đã tìm, không có nguồn.

Hạn chế của lần nghiên cứu này: WebFetch dùng model nhỏ tóm tắt trang nên nhiều thông số (tham số, crop, license chi tiết) trả về "không nêu". Không có trang nào xác nhận tốc độ CPU; mọi ước lượng CPU là [S].

## 0. Điểm mấu chốt (kết luận)

1. **Cityscapes 19 lớp đã có sẵn pole, wall, fence, terrain, sidewalk** (ACDC/Dark Zurich đều dùng đúng 19 lớp này [N: arxiv 1901.05946 / 2305.17349 qua tìm kiếm]). Vì vậy các nhãn này "yếu" chủ yếu do chất lượng/domain, không do thiếu lớp. SegFormer-B5/M2F Cityscapes đã có; cần ĐO sidewalk/terrain/pole trên job 285 trước khi thay model.
2. **Cityscapes KHÔNG có lane paint, crosswalk, curb.** Muốn có phải dùng model train trên **Mapillary Vistas** (có `Curb`, `Fence`, `Wall`, `Pole`, `Lane Marking - Crosswalk`, và các lớp lane marking khác; v1.2 66 lớp, v2.0 124 lớp [N: blog Mapillary, mmseg mapillary.py qua tìm kiếm]). Ứng viên thật và có checkpoint: **Mask2Former Swin-L Mapillary (HF)** và **OneFormer Mapillary (Swin-L/ConvNeXt-L/DiNAT-L)**. Cả hai ~220M tham số, nặng trên CPU.
3. **Không tìm thấy** model công khai chuyên "road paint trắng/vàng, single/double" hay "crosswalk" có model card đầy đủ. Lane màu/đơn-đôi nhiều khả năng cần luật hình học + màu (HSV) trên vùng road/lane-marking do model Vistas cho ra, hoặc fine-tune nhẹ.
4. **Ảnh tối sâu:** nguồn hợp lý là ACDC night (có nhãn 19 lớp Cityscapes) và Dark Zurich; có checkpoint công khai Refign (MIT) trên SegFormer-B5/MiT-B5. Nhưng chỉ cho 19 lớp Cityscapes, và B5 ở độ phân giải cao khó đạt 10s/frame trên CPU [S].

## 1. Nhóm A — pole, wall, fence, terrain, sidewalk (lớp Cityscapes)

| # | Ứng viên | Chi tiết | Ghi chú |
|---|---|---|---|
| A1 | **SegFormer-B2 Cityscapes** `nvidia/segformer-b2-finetuned-cityscapes-1024-1024` | Train Cityscapes, input 1024x1024 [N], license "other" (link sang NVlabs SegFormer) [N]. Tham số: trang không nêu; B2 thường ~27M [S] (card Vrjb là fine-tune của chính nó và ghi 27.4M [N]). ONNX: Optimum liệt kê SegFormer trong kiến trúc hỗ trợ export [N, không rõ task semseg]. | Đã có. CPU: khả thi [S] vì 27M tham số. Đêm: không có dữ liệu đêm trong Cityscapes [S]. |
| A2 | **Mask2Former Swin-L Mapillary** `facebook/mask2former-swin-large-mapillary-vistas-semantic` | Train Mapillary Vistas [N], 0.2B tham số [N], license "other" [N], độ phân giải huấn luyện: không nêu trên trang [N]. Vistas có Pole/Fence/Wall/Curb [N, qua mmseg]. Không thấy Mask2Former trong danh sách ONNX Optimum [N-âm: không tìm thấy]. | Vistas đa dạng thời tiết/thời điểm hơn Cityscapes (Vistas có ảnh nhiều điều kiện chiếu sáng; mức độ ban đêm cụ thể: không xác minh [S]). CPU 16GB: nặng; 220M + Swin-L, ước vài chục giây/frame ở ~1024 [S] -> khó vào 10s. |
| A3 | **OneFormer Swin-L Mapillary** (checkpoint `.pth` repo SHI-Labs, MIT) | mIoU Vistas single-scale 62.9, 219M [N]; biến thể ConvNeXt-L 63.2/220M, DiNAT-L 64.0/223M [N]. Link: shi-labs.com/projects/oneformer/mapillary/250_16_swin_l_oneformer_mapillary_300k.pth. Crop: không nêu [N]. Không tìm thấy bản HF Mapillary trong org shi-labs ở lần tìm này. | Dạng .pth cần code detectron2-style; cài đặt trên Windows CPU rủi ro [S]. |

Cũng có `Vrjb/SegFormer_b2_mappillary_` (27.4M, 23 lớp nhóm cấp cao, mIoU 0.678, tập dữ liệu **không nêu**, license other) [N]. Chỉ để tham khảo: 23 lớp gộp (có nhóm "marking"), dữ liệu không rõ -> rủi ro nguồn gốc; không khuyến nghị dùng cho sản xuất trước khi kiểm.

## 2. Nhóm B — lane paint (trắng/vàng, single/double), crosswalk, road curb, lane khác màu

| # | Ứng viên | Chi tiết | Ghi chú |
|---|---|---|---|
| B1 | **Mask2Former Swin-L Mapillary** (như A2) | Có lớp `Lane Marking - Crosswalk` (v1.2) và các biến thể crosswalk/lane marking ở v2.0 [N qua mmseg & blog; nhưng checkpoint HF dùng v1.2 hay v2.0: **không xác minh**, trang không liệt kê lớp]. Có `Curb` [N]. | Ứng viên mạnh nhất cho crosswalk + curb. Lane trắng/vàng/đơn/đôi: Vistas phân loại theo loại vạch (Lane Marking - General...), KHÔNG phân màu trắng/vàng [S, theo tên lớp]; màu phải suy bằng HSV. |
| B2 | **OneFormer Mapillary** (A3) | như A3. | Cùng họ Vistas, mIoU Vistas cao hơn chút (62.9-64.0 vs M2F ms 64.7 theo Papers With Code [N: số này là multiscale]). Không có số riêng cho lớp marking. |
| B3 | **8bits-ai/SegFormer-Lane-Marking** (đã có, recall rất thấp) | 27.3M, MIT, card trống: không có lớp/dataset [N]. | Đã đo yếu. Không khuyến nghị. Hướng thay: tự fine-tune SegFormer-B2/B3 trên lane (hướng dẫn BDD100K ở LearnOpenCV, DebuggerCafe - [N] có bài, chưa đánh giá chất lượng). |

BDD100K: repo SysCV/bdd100k-models (Apache-2.0) nêu có `sem_seg` và `Drivable Area`, **lane marking chưa hỗ trợ (roadmap)** [N]. Kiến trúc/định dạng: không nêu. Dataset BDD100K segmentation 10k ảnh nhãn Cityscapes 19 lớp [N qua paper]; lane marking là nhãn riêng dạng đường (polyline) chứ không phải polygon hẹp -> không khớp quy ước người dùng [S].

Kết luận B: **không tìm thấy** model công khai có model card rõ cho vạch kẻ trắng/vàng/đôi/đơn. Khả thi nhất: (i) Vistas M2F/OneFormer để lấy road/crosswalk/curb/lane-marking mask thô, (ii) luật HSV + hình học (đã có `src/cvat_tools/lanes/`) để tách trắng/vàng và đơn/đôi, (iii) fine-tune nhẹ nếu vẫn kém.

## 3. Nhóm C — mọi nhãn nền ở ảnh tối sâu

| # | Ứng viên | Chi tiết | Ghi chú |
|---|---|---|---|
| C1 | **Refign-HRDA\* (ACDC/Dark Zurich)** github.com/brdav/refign | MIT [N]. Checkpoint công khai trên ETH Research Collection [N]. Test mIoU: ACDC 72.1, Dark Zurich 63.9 (HRDA\*, backbone Cityscapes-pretrained SegFormer-B5); Refign-DAFormer (MiT-B5): ACDC 65.5, DZ 56.2 [N]. Độ phân giải huấn luyện: không nêu [N]. | Có night thực (ACDC night, Dark Zurich). Chỉ 19 lớp. B5 + HRDA multi-scale: nặng trên CPU, khó 10s [S]. Cần code mmseg-style; định dạng ONNX: không tìm thấy. |
| C2 | **Mask2Former/OneFormer Mapillary** | như A2/A3. | Chưa có bằng chứng đo ban đêm. Phải đo trên job 285 tối. |
| C3 | **SegFormer-B5 Cityscapes + tăng sáng/CLAHE/gamma tiền xử lý** (đã có) | Không phải model mới. | Đường rẻ nhất; cần thêm vào input contract (chuẩn hóa độ sáng) và đo. Hiệu quả: [S]. |

Dữ liệu night:
- **ACDC**: 4006 ảnh, chia đều night/fog/rain/snow; train/val/test 1600/406/2000; 19 lớp Cityscapes [N]. License dataset: **không tìm thấy** trên kết quả (kiểm acdc.vision.ee.ethz.ch trước khi dùng).
- **Dark Zurich**: 2617 ảnh (2416 train/50 val/151 test), ngày/hoàng hôn/đêm có tương ứng ảnh [N]; license: **không tìm thấy**.
- **BDD100K**: 10k ảnh segmentation 19 lớp có nhiều thời điểm trong ngày [N]; license các nguồn mâu thuẫn (trang bên thứ 3: BSD-3) -> phải kiểm trang chính thức.
- Mapillary Vistas: nguồn mâu thuẫn (CC-BY-SA trong paper; CC BY-NC-SA ở Dataset Ninja; nghiên cứu miễn phí, thương mại trả phí) [N]. Dự án học tập nội bộ: khả năng chấp nhận được, nhưng KHÔNG dùng thương mại khi chưa xác nhận.

**Cần fine-tune không?** Kết luận có cơ sở: các model domain adaptation (Refign) đạt mIoU Dark Zurich 56-64 so với ACDC 65-72, tức đêm vẫn kém ngày dù đã adapt [N]; nghĩa là model Cityscapes thuần sẽ kém hơn nữa ở đêm [S, suy luận]. Với ngân sách 10s/frame CPU và lớp chủ yếu cần là road/sky/building/vegetation, nên: (1) thử tiền xử lý + model Vistas trước (chưa cần train); (2) chỉ fine-tune nếu đo trên ảnh đêm job 285 cho thấy IoU lớp nền < ngưỡng người dùng. Fine-tune trên CPU i7-8850H thực tế không khả thi cho B5/Swin-L [S]; nếu cần, dùng SegFormer-B0/B2 hoặc huấn luyện ngoài máy (Colab/GPU thuê).

## 4. Về CPU 16GB / định dạng (tóm tắt)

- SegFormer: có trong danh sách export ONNX của Optimum [N, task chưa rõ]; B2 ~27M tham số nên ước lượng chạy được [S].
- Mask2Former: không thấy trong danh sách Optimum [N-âm]; Swin-L 0.2B: RAM ổn (FP32 ~0.9GB trọng số) nhưng chậm [S].
- OpenVINO: không tìm thấy nguồn riêng cho các model trên.
- Số giây/frame: toàn bộ là [S]; phải đo bằng `scripts/seg_model_bench.py`.

## 5. Bảng tổng hợp: nhãn -> ứng viên -> rủi ro -> bước đo tiếp

| Nhãn | Ứng viên (ưu tiên) | Rủi ro | Bước đo tiếp theo |
|---|---|---|---|
| sidewalk, terrain, wall, fence, pole | SegFormer-B5/B2 Cityscapes (đã có) -> M2F Mapillary | Pole mỏng bị mất ở độ phân giải thấp; wall/fence nhầm với building; sidewalk chưa đo | Đo IoU/overlay trên các frame job 285 có GT tay; thử tile/độ phân giải cao cho pole |
| crosswalk | M2F Mapillary (B1), OneFormer Mapillary (B2) | Xác minh lớp có trong checkpoint HF (chưa liệt kê); 220M chậm CPU | Đọc `config.json` `id2label` (file nhỏ, không cần tải trọng số); chạy 3-5 frame có crosswalk |
| road curb | M2F Mapillary (`Curb`) | Lớp mảnh, IoU Vistas thường thấp [S] | Như trên; so với luật hình học hiện có |
| lane paint trắng/vàng, đơn/đôi | Vistas lane-marking mask + luật HSV/hình học (`src/cvat_tools/lanes/`) | Không có model phân màu/đơn-đôi (không tìm thấy); Vistas không phân màu [S]; polygon hẹp theo quy ước người dùng | Đo recall của lớp lane marking Vistas trên 5-10 frame; nếu < luật hiện tại thì giữ luật |
| lane khác màu (đỏ/xanh...) | Luật màu HSV | Không có model | Liệt kê ảnh có vạch màu lạ, hiệu chỉnh ngưỡng |
| nền ở ảnh tối sâu | Tiền xử lý sáng + SegFormer-B5/M2F; nếu cần Refign-HRDA\* | Refign nặng, cài đặt mmseg trên Windows CPU; dataset license chưa rõ | Đo mIoU nền trên frame tối job 285 với vs. không CLAHE/gamma; sau đó mới quyết định thử Refign |
| mọi nhãn: ONNX/OpenVINO | SegFormer qua Optimum | M2F/OneFormer khó export | Thử export SegFormer-B2 ONNX và đo giây/frame |

## Nguồn
- https://huggingface.co/nvidia/segformer-b2-finetuned-cityscapes-1024-1024
- https://huggingface.co/facebook/mask2former-swin-large-mapillary-vistas-semantic
- https://github.com/SHI-Labs/OneFormer
- https://huggingface.co/Vrjb/SegFormer_b2_mappillary_
- https://huggingface.co/8bits-ai/SegFormer-Lane-Marking
- https://github.com/SysCV/bdd100k-models
- https://github.com/brdav/refign
- https://arxiv.org/abs/1901.05946 , https://arxiv.org/pdf/2305.17349 (Dark Zurich, ACDC)
- https://blog.mapillary.com/update/2021/01/18/vistas-2-dataset.html ; https://onedl-mmsegmentation.readthedocs.io/en/latest/_modules/mmseg/datasets/mapillary.html
- https://research.mapillary.com/publication/iccv17a ; https://datasetninja.com/mapillary-vistas-dataset
- https://huggingface.co/docs/optimum/exporters/onnx/overview
- https://learnopencv.com/segformer-fine-tuning-for-lane-detection/
