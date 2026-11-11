# Ý tưởng cải thiện quy trình gán nhãn trong CVAT (ban đêm / ADAS)

> Written for: nhóm thực tập và Key Coach, cần duyệt phạm vi trước khi code.
> Trạng thái: **Đề xuất (chưa triển khai)**. Bám theo `day02/projects/PROJECT_OVERVIEW.md` (Smart-CVAT Assistant), không thay thế nó.

---

## 0. Ba điều phải chốt trước (blocker)

### 0.1 Ba taxonomy đang lệch nhau

| Nguồn | Các lớp |
|---|---|
| Lab Day02 (`day02/labs/data.yaml`) | `car`, `truck`, `bus`, `van` |
| Đặc tả BlindSpot Guard+ (ảnh ADAS) | `car`, `motorcycle`, `bicycle`, `pedestrian` |
| Project CVAT đang mở (ảnh 1) | `car`, `motorcycle`, `pedestrian` (không có `bicycle`) |

Cần **một file schema duy nhất** (SSOT, ví dụ `schema/taxonomy.yaml`) và mọi tool đọc từ đó. Đề xuất: taxonomy chính thức theo đặc tả ADAS; nhóm `car` tách thêm thuộc tính `vehicle_type` (sedan/suv/pickup/truck/bus/van) để giữ được thông tin của lab Day02.

### 0.2 Cảnh báo nhãn lab Day02 (cần xử lý trước khi làm tool)

Đã kiểm tra thực tế trong `day02/labs/`:

- Nhãn hiện tại trong `dataset/labels/train/` **giống hệt `gold_train_labels/` ở cả 50/50 file** (so sánh byte-level).
- Commit `a8644a6` ("complete CP5 gold QC and rework") ghi đè nhãn đã khóa `37a29a9` bằng nội dung gold: 1171 box → 653 box, F1 0,4857 → 1,0.
- Trong `Downloads/` có export CVAT `job_2_annotations_2026_11_09_11_42_01_ultralytics yolo detection 1.0.zip` (1171 box). Export này khớp **50/50** với bản đã khóa `37a29a9`, không khớp gold. Vì vậy có thể khôi phục bản khóa từ export này, không cần lấy từ gold.
- `RULES.md` cấm "không dùng gold train để lấy đáp án trước khi khóa nhãn" và "không thay đổi gold labels". `RUBRIC.md` ghi rõ việc này làm bài không được chấm phần pipeline.
- `report/.../2A202604062_PhamPhuNguyenHung.md` mục 4 mô tả rework là "đối chiếu trực tiếp với quy chuẩn gold set", và tự chấm 100/100.

**Việc nên làm**: khôi phục nhãn từ commit `37a29a9` (bản đã khóa), tự rework bằng guideline và tool QA; sửa mục 4 và mục 7 của báo cáo; trao đổi với giảng viên trước khi nộp. Đây là quyết định của chủ bài, nên không tự sửa repo.

### 0.3 Lộ token CVAT trong code

`day02/projects/prelabel_to_cvat.py`, `sync_to_cvat.py`, `cvat_job_sync.py`, `upload_50_to_cvat.py` đều có `CVAT_PAT` hard-code trong source. Cần:
- Thu hồi (revoke) token đó trên CVAT, tạo token mới.
- Chuyển sang đọc từ `.env` (đã có cơ chế đọc `.env`, chỉ cần xóa giá trị mặc định).
- Kiểm tra `.env` không bị commit (RULES.md cấm).

---

## 1. Persona

| Persona | Vai trò |
|---|---|
| **Annotator** | Gán nhãn và sửa box trong CVAT, cần nhanh và ít lỗi. |
| **Reviewer / Key Coach** | Duyệt nhãn, quyết định ca mơ hồ, khóa schema. |
| **Người làm pipeline** | Viết tool, train model, chạy đánh giá. |
| **Người đọc báo cáo** | Đánh giá kết quả theo điều kiện (đêm, mưa, tuyết, che khuất). |

---

## 2. Jobs To Be Done (JTBD)

Mẫu: *Khi [tình huống], tôi muốn [động cơ], để [kết quả].*

### 2.1 Annotator

| ID | JTBD | Ưu tiên |
|---|---|---|
| A1 | Khi đổi lớp của nhiều box liên tiếp, tôi muốn đổi bằng phím tắt, để không phải click menu. | P0 |
| A2 | Khi gặp xe bị che/cắt khung, tôi muốn bật nhanh cờ `occluded`/`truncated` bằng phím, để ghi nhận đúng mà không mất nhịp. | P0 |
| A3 | Khi xe ở xa (box nhỏ), tôi muốn phóng to vùng đó, để vẽ box đúng pixel. | P1 |
| A4 | Khi ảnh đêm quá tối hoặc chói đèn, tôi muốn xem bản tăng sáng chỉ để nhìn (nhãn vẫn gán trên ảnh gốc), để thấy xe. | P1 |
| A5 | Khi chưa chắc một ca, tôi muốn đánh dấu "mơ hồ" và ghi lý do, để hỏi Key Coach sau mà không phải nhớ. | P0 |
| A6 | Khi làm xong frame/ảnh, tôi muốn thấy các cảnh báo QA ngay trên ảnh, để sửa trước khi nộp. | P0 |
| A7 | Khi model gợi ý box, tôi muốn chấp nhận hoặc bỏ từng gợi ý bằng một phím, để tăng tốc độ gán. | P1 |

### 2.2 Reviewer / Key Coach

| ID | JTBD | Ưu tiên |
|---|---|---|
| R1 | Khi nhận bộ nhãn của nhiều người, tôi muốn xem danh sách lỗi QA đã xếp hạng, để review đúng chỗ rủi ro nhất. | P0 |
| R2 | Khi có ca mơ hồ, tôi muốn chốt quyết định và tự thêm vào guideline, để các annotator khác áp dụng thống nhất. | P0 |
| R3 | Khi cần đo chất lượng nhóm, tôi muốn thấy IAA (IoU, độ khớp lớp) giữa hai người gán cùng frame, để biết guideline có đủ rõ không. | P1 |
| R4 | Khi lớp hoặc điều kiện thiếu dữ liệu, tôi muốn thấy bảng phân phối lớp × điều kiện, để điều chỉnh việc lấy thêm ảnh. | P0 |

### 2.3 Người làm pipeline và báo cáo

| ID | JTBD | Ưu tiên |
|---|---|---|
| E1 | Khi có nhãn khác tên lớp (ví dụ `bus`, `motorcycle`, `person` từ dataset ngoài), tôi muốn tự map về schema, để không sửa tay từng file. | P0 |
| E2 | Khi muốn pre-annotate, tôi muốn chạy model fine-tune và đẩy nhãn nháp vào CVAT, để giảm thời gian vẽ từ đầu. | P0 |
| E3 | Khi model có kết quả trên Colab, tôi muốn tự đọc `results.csv` và `model_eval_metrics.json` để vẽ biểu đồ per-class và per-condition, để không chép số tay. | P0 |
| E4 | Khi viết báo cáo, tôi muốn sinh sẵn bảng số liệu và link ảnh đúng cấu trúc `assets/`, để không sai đường dẫn. | P1 |
| E5 | Khi đổi schema hoặc guideline, tôi muốn kiểm tra ngay nhãn cũ có vi phạm không, để không phát hiện lỗi muộn. | P0 |
| E6 | Khi đánh giá model, tôi muốn biết số mẫu mỗi điều kiện đủ tin cậy không, để không kết luận từ 2–3 box. | P1 |

### 2.4 Người đọc báo cáo / sản phẩm

| ID | JTBD | Ưu tiên |
|---|---|---|
| S1 | Khi muốn biết model yếu ở đâu, tôi muốn xem Recall@FPPI=0,1 theo điều kiện (đêm, mưa, tuyết, che khuất), để so với KPI của đặc tả. | P1 |
| S2 | Khi muốn so sánh gán tay với gán có hỗ trợ, tôi muốn thấy thời gian, số lỗi, số lần sửa, để đánh giá Experiment A/B của overview. | P1 |

---

## 3. Nhóm tính năng

### 3.1 Phím tắt (A1, A2, A5, A7)

- Kiểm tra trước: CVAT đã có phím tắt mặc định cho tạo box, chuyển frame, và một số thuộc tính. Cần liệt kê phím hiện có rồi mới thêm, tránh trùng.
- Đề xuất bộ phím cho thuộc tính ca khó: `G` = glare, `H` = headlight_only, `F` = far, `O` = occluded, `T` = truncated, `M` = mơ hồ (ghi lý do sau).
- Nếu CVAT không cho cấu hình phím tùy ý, làm **userscript trình duyệt** hoặc extension nhỏ cho trang CVAT, không sửa core CVAT.
- Tiêu chí nghiệm thu: một annotator thao tác một ca "xe xa + bị che + đêm" chỉ bằng bàn phím, số lần chạm chuột = 0.

### 3.2 Auto-mapping nhãn (E1)

- File `mapping.yaml` ánh xạ tên lớp nguồn → schema chính thức, ví dụ `bus` (COCO) → `bus`, `person` → `pedestrian`, `bicycle` → `bicycle`.
- Mỗi ánh xạ là một dòng cấu hình, không hard-code trong code.
- Ca không có ánh xạ: đưa vào hàng đợi "lớp lạ" để người quyết định, không tự gán.
- Tiêu chí nghiệm thu: chạy trên file có tên lớp lạ, báo đúng số lớp chưa ánh xạ.

### 3.3 Tự động gợi ý sửa nhãn (A6, R1)

Nguyên tắc: **chỉ gợi ý, người chấp nhận**. Gợi ý chỉ được sinh từ luật hình học và từ model, **không bao giờ từ gold**.

| Gợi ý | Điều kiện kích hoạt | Hành động đề xuất |
|---|---|---|
| Đánh dấu `truncated` | Cạnh box chạm mép ảnh (0 hoặc 1) | Bật cờ truncated |
| Box trùng | IoU > 0,9 cùng lớp | Gộp hoặc xóa một box |
| Box quá nhỏ | Dưới ngưỡng px của guideline | Xóa hoặc đánh dấu `far` |
| Nghi thiếu box | Model tin cậy cao, người không gán | Thêm box nháp |
| Nghi thừa box | Người gán, model không thấy (lâu dài) | Xem lại |
| Lệch lớp | Model và người khác lớp, IoU cao | Xem lại lớp |
| Flicker (video) | Xe mất rồi xuất hiện lại ở frame kế cận | Xem lại frame |

- Hàng đợi gợi ý sắp theo độ rủi ro. Vì đặc tả coi bỏ sót (FN) là nguy hiểm hơn, nhóm "nghi thiếu box" có độ ưu tiên cao.

### 3.4 Auto-guideline (R2, E5)

Đề xuất **guideline như code**:
- Mỗi quy tắc trong guideline có một ID (ví dụ `R-SIZE-01: box cao < 15px thì không gán`), kèm một kiểm tra tự động tương ứng.
- Quyết định ca mơ hồ được lưu thành file log (`decisions.yaml`: ảnh, quyết định, lý do, người quyết định). Tool sinh bản nháp guideline từ log này.
- Tool kiểm tra "trôi guideline": nhãn có vi phạm quy tắc nào không.
- Ví dụ lỗ hổng cần chốt: guideline ghi "xe xa dưới 15 pixel", nhưng chưa nói rõ là chiều cao hay chiều rộng, và đo trên ảnh gốc hay ảnh đã resize (512×320 khi đưa vào model). Tool sẽ buộc người viết guideline chọn một giá trị.

### 3.5 Thống kê (R4, E6)

- Phân phối lớp × điều kiện (đêm, mưa, tuyết, chói đèn, che khuất, xa).
- Phân phối kích thước box và khoảng cách (theo chiều cao box).
- Số mẫu mỗi ô; cảnh báo ô có ít hơn ngưỡng mẫu (ví dụ < 30 box).
- Số liệu theo annotator, và IAA khi có frame gán chồng chéo.

### 3.6 Pre-annotation (E2)

- Model: fine-tune YOLO trên dữ liệu đêm; có thể dùng model giáo viên lớn hơn để sinh nhãn nháp, còn YOLO nano là model học sinh cần đánh giá.
- Đưa nhãn nháp vào CVAT bằng auto-annotation (serverless) hoặc import file đã chuyển đổi.
- Đo **tỷ lệ sửa** (IoU nhãn nháp với nhãn cuối) theo điều kiện. Số này cho biết model đã đủ tốt ở điều kiện nào.
- Active learning: ưu tiên gửi người gán các frame có độ tin cậy gần ngưỡng vận hành 0,20–0,25 của đặc tả.

### 3.7 Phân tích kết quả Colab (E3, E4, S1)

Đầu vào: `day2_colab_outputs/yolo26_runs/vehicle_annotation/results.csv`, `model_eval_metrics.json`, và các ảnh trong `eval_predictions/visuals/`.
- Đầu ra: bảng per-class; đường precision/recall theo epoch; cảnh báo lớp có ít mẫu (ví dụ `bus` 2 xe, `van` 12 xe trong tập eval).
- Cảnh báo kích thước mẫu: tập eval có 10 ảnh, 113 instance. Kết luận theo lớp chỉ mang tính gợi ý.
- **Phát hiện từ `day2_colab_outputs.zip` (Downloads):** số trong `model_eval_metrics.json` khớp với báo cáo (P 0,4071; R 0,2340; mAP50 0,2737; mAP50-95 0,2018). Nhưng `results.csv` cho thấy mAP50 cao nhất ở **epoch 1** (0,2739), còn epoch 50 chỉ 0,2267. `best.pt` là checkpoint epoch 1, được chọn trên 10 ảnh eval. Đây là lựa chọn lạc quan, và model gần như chưa học gì; báo cáo cần nêu rõ và phân tích nguyên nhân (ít ảnh, nhãn lệch, hay overfit).
- Tool cần kiểm tra tự động: best epoch có nằm ở đầu quá trình train không, và chênh lệch train/val theo epoch.
- Sinh sẵn bảng số liệu cho mục 5 của báo cáo, kèm đường dẫn ảnh đúng cấu trúc `assets/`.

### 3.8 Đánh giá với gold (chỉ sau khi khóa nhãn)

- Dùng `day02/labs/tools/evaluate_annotations.py` (đã có: matching một-một, IoU ≥ 0,5, theo lớp).
- Chỉ báo cáo kết quả, không tự động sửa nhãn dựa trên gold.

---

## 4. Ranh giới cần giữ

1. Gold không được dùng để sửa nhãn trước khi khóa. Tool không đọc `gold_train_labels/` trong luồng gán nhãn.
2. Tool gợi ý, người quyết định. Không có chế độ "tự sửa hàng loạt" trên bộ nhãn đã khóa.
3. Mỗi thay đổi nhãn được ghi lại: ai sửa, sửa gì, lý do (phục vụ báo cáo rework).
4. Không đưa dữ liệu có người đi bộ và biển số ra ngoài mà chưa ẩn danh (làm mờ). Ghi vào báo cáo.
5. Không đưa token vào code.

---

## 5. Lộ trình gợi ý (khớp với Experiment A/B/C của overview)

| Giai đoạn | Nội dung | Kết quả kiểm chứng được |
|---|---|---|
| 0 | Chốt schema SSOT, xử lý nhãn Day02 (mục 0.2), thu hồi token (0.3) | Schema một file; nhãn Day02 về trạng thái khóa |
| 1 | Auto-mapping + kiểm tra geometry/schema + thống kê | Chạy trên 50 ảnh Day02 cho ra báo cáo lỗi |
| 2 | Phím tắt thuộc tính ca khó + hàng đợi gợi ý sửa | Số lần chạm chuột giảm trong thử nghiệm có đo |
| 3 | Pre-annotation bằng model fine-tune + đo tỷ lệ sửa | Tỷ lệ sửa theo điều kiện |
| 4 | Phân tích Colab tự động + harness Recall@FPPI=0,1 | Bảng KPI theo điều kiện, có cảnh báo cỡ mẫu |
| 5 | Guideline như code + IAA | Tỷ lệ vi phạm guideline giảm qua các vòng |

Phạm vi MVP theo overview (mục 6) gồm: AI-assisted bbox, mapping, validation, export/import CVAT, human review, audit report, benchmark. Các mục trên bám theo phạm vi đó. Tracking (MOT) và retrain tự động vẫn để ngoài phạm vi Phase 1.

---

## 6. Câu hỏi cần Key Coach / nhóm trả lời

1. Taxonomy chính thức: dùng 4 lớp của đặc tả ADAS, hay giữ 4 lớp của lab Day02? Có tách `vehicle_type` không?
2. Ngưỡng "xe xa": đo chiều cao hay chiều rộng, trên ảnh gốc hay ảnh 512×320?
3. Có được dùng dữ liệu công khai (BDD100K, ACDC) để pretrain không? Ghi nguồn thế nào?
4. Mốc khóa nhãn Day02: có cho phép khôi phục bản `37a29a9` và rework lại không? Báo cáo sửa thế nào?
5. Ẩn danh người và biển số: làm mờ trước khi đưa vào CVAT, hay không cần?

---

## 7. Việc làm ngay (không cần chờ duyệt)

- [ ] Thu hồi token CVAT đã lộ, xóa giá trị mặc định trong 4 script ở `day02/projects/`.
- [ ] Báo với giảng viên về việc nhãn Day02 trùng gold; quyết định khôi phục theo hướng dẫn của lớp.
- [ ] Viết `schema/taxonomy.yaml` (một file, dùng chung cho mọi tool).
