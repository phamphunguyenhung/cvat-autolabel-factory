# Guideline Pose 17 điểm — Nhóm G06 (Task 402 / Job 1623, Tier A)

> **Phiên bản:** `G06 v2.0` (18/11/2026) — Đồng bộ `BTC_OFFICIAL` V1 (`HumanPose17_Annotation_Guideline_V1.docx` qua `weeks/guidelines/w2-face50-pose17.md`) và bổ sung bằng chứng thực nghiệm từ Job 1623 (`A01`–`A06`).  
> **Tham chiếu quy tắc tái sử dụng:** [POSE17_GENERAL_GUIDELINE.md](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/docs/guidelines/pose17/POSE17_GENERAL_GUIDELINE.md) (`P17-G01`–`P17-G30`).  
> **Nguyên tắc phân biệt nguồn:** Mọi quy định đều gắn nhãn `[BTC_OFFICIAL]`, `[USER_OBSERVED]`, `[GEOMETRIC_INFERENCE]`, hoặc `[AI_RECOMMENDATION]`. Khi có xung đột, **`BTC_OFFICIAL` luôn thắng**.

---

## 1. Bối cảnh bài tập (`Task 402` / `Job 1623`)

| Thuộc tính | Giá trị thực tế (`A01_cvat_reader.md`) |
|---|---|
| **CVAT Server / Org** | `https://cvat.edufun.ai` · `X-Organization: cohort-5a` |
| **Project / Task / Job** | `project_id = 159` · `task_id = 402` (`week2-human-pose/G06`) · `job_id = 1623` |
| **Assignee** | `id = 245`, `username = "2A202604062"` (`ACR`) |
| **Phạm vi frame** | `30` frames: `frame_index = 90..119` (`G06_091.jpg` .. `G06_120.jpg`, công thức `frame = số_file - 1`) |
| **Label chính** | `person_vf17` (`id = 12322`, `type = "skeleton"`) · **Chế độ vẽ: `Shape`** (không `Track`) |
| **Trạng thái hiện tại** | `status = "annotation"`, `stage = "annotation"`, `state = "in progress"`, `issues = 0` |
| **Số skeleton hiện có** | `28/30` frames có 1 skeleton (`476` keypoints, `source = "manual"`); **thiếu 2 frame**: `100` (`G06_101.jpg`) và `118` (`G06_119.jpg`); `gold = 0` |

- `[BTC_OFFICIAL]` (`P17-G01`): Mỗi ảnh **chỉ gán 1 tài xế** (người ngồi ghế lái). Hành khách phía sau/bên cạnh, ảnh phản chiếu, hình in: **không gán**. Không có tài xế trong khung: **bỏ qua frame, không vẽ**.

---

## 2. Cấu hình CVAT & Topology (`person_vf17`)

- `[BTC_OFFICIAL]` (`P17-G02`): Vẽ bằng chế độ **Shape**, mỗi ảnh đúng **1 skeleton `person_vf17`** (`id = 12322`) với đủ **17 sublabel `"1".."17"`** (`id = 12323..12339`). Không tạo label/attribute mới, không đổi tên sublabel (kể cả khi tài liệu BTC ghi tên label là `person` — xem `issues.md` A3, trạng thái `NEEDS MENTOR`).
- `[AI_RECOMMENDATION]` (`P17-G29`): **Khác biệt topology CVAT SVG vs COCO chuẩn**:
  - CVAT `person_vf17` (`data/jobs/edufun/1623/labels.json` & `pose17_template.png`) định nghĩa **18 cạnh SVG**: `(1,2), (1,3), (2,4), (3,5), (4,6), (5,7), (6,7), (6,8), (8,10), (7,9), (9,11), (6,12), (7,13), (12,13), (12,14), (14,16), (13,15), (15,17)`.
  - COCO chuẩn (`tools/skeleton-pose-manager/config/schema.json`) có **19 cạnh** — bao gồm thêm cạnh **`[2, 3]` (mắt R – mắt L)** mà CVAT `person_vf17` **không vẽ**.

---

## 3. Đặc điểm Dataset Job 1623 (`30` frames)

| Đặc trưng | Thống kê thực nghiệm (`A05_difficult_case_miner.md`) |
|---|---|
| **Cảm biến (Modality)** | **18 ảnh IR xám** (`max_rgb_diff = 0.0`, `sat = 0.0`) · **12 ảnh RGB màu** (`sat = 78.8–110.7`) |
| **Độ phân giải (`RESOLUTION_MISMATCH`)** | **`1280×1024`**: 15 frames (IR chính diện + 2 fisheye ngang `f106, f110`)<br>**`960×540`** (mức danh nghĩa BTC V1): 12 frames (toàn bộ 12 RGB góc nghiêng)<br>**`512×424`**: 3 frames (`f103, f104, f112` — IR góc nghiêng ngả lưng)<br>*(18/30 frames = 60% lệch chuẩn `960×540` của BTC)* |
| **Thiếu sáng (`LOW_LIGHT`)** | 18/18 ảnh IR có `mean_luma` từ **`12.8`** (`f116`) đến **`36.4`** (`f119`), `dark_fraction (luma < 40)` từ **`0.68` đến `0.93`** (`f099` tối nhất 0.93). Cần tăng độ sáng bằng *Image settings* trên CVAT khi gán. |
| **Góc máy & Méo fisheye (`FISHEYE_ROTATION`)** | **15 frames góc nghiêng (side-mount)**: đầu bên trái ảnh, chân bên phải (`12 RGB + 3 IR`: `f103, f104, f112`).<br>**2 frames fisheye ngang (head right)**: `f106, f110` (đầu bên phải ảnh, chân bên trái).<br>**13 frames thẳng đứng (upright)**: `f90–92, f94–95, f99, f102, f107, f109, f111, f114, f116, f119`. |
| **Nhòe chuyển động (`MOTION_BLUR`)** | RGB: `f100` (`Lap=192.8`, tay/cánh tay nhòe mạnh), `f118` (`Lap=183.7`), `f113` (`218.9`), `f108` (`283.5`). IR độ nét thấp (`Lap = 3.5–62.8`, dưới `10.0` ở `f116, f110, f099, f091, f094`). |

---

## 4. Bảng 17 Keypoint với Tên và ID Thực tế (`person_vf17`)

> `[BTC_OFFICIAL]` (`P17-G06`, `P17-G18`–`P17-G21`): Số **chẵn (`2–16`) = `R` (phải ảnh)**, số **lẻ (`3–17`) = `L` (trái ảnh)**.  
> *Lưu ý kỹ thuật (`A03 §6`):* Trong COCO chuẩn nhìn thẳng, `left_*` giải phẫu nằm bên phải ảnh (`R`), `right_*` giải phẫu nằm bên trái ảnh (`L`). Code cũ `eval_pose17.py` đang in nhãn `T/P` ngược so với quy ước BTC.

| Sublabel | CVAT ID | COCO Idx | COCO Name | Tên BTC/G06 | Vị trí giải phẫu chuẩn (`[BTC_OFFICIAL]`) | Nhóm |
|:---:|---:|---:|---|---|---|---|
| `"1"` | `12323` | `0` | `nose` | **mũi** | Chóp mũi (mặt nghiêng vẫn đặt tại chóp mũi, không dời về giữa mặt) | `head` |
| `"2"` | `12324` | `1` | `left_eye` | **mắt R** | Tâm đồng tử (mắt nhắm: tâm khe mí) | `head` |
| `"3"` | `12325` | `2` | `right_eye` | **mắt L** | Tâm đồng tử (mắt nhắm: tâm khe mí) | `head` |
| `"4"` | `12326` | `3` | `left_ear` | **tai R** | Ống tai (không đặt ở chóp tai hay dái tai) | `head` |
| `"5"` | `12327` | `4` | `right_ear` | **tai L** | Ống tai (không đặt ở chóp tai hay dái tai) | `head` |
| `"6"` | `12328` | `5` | `left_shoulder` | **vai R** | Tâm khớp vai (điểm xoay của cánh tay, không đặt ở cổ/cổ áo) | `torso` |
| `"7"` | `12329` | `6` | `right_shoulder` | **vai L** | Tâm khớp vai (điểm xoay của cánh tay) | `torso` |
| `"8"` | `12330` | `7` | `left_elbow` | **khuỷu R** | Tâm khớp khuỷu | `upper_limb` |
| `"9"` | `12331` | `8` | `right_elbow` | **khuỷu L** | Tâm khớp khuỷu | `upper_limb` |
| `"10"` | `12332` | `9` | `left_wrist` | **cổ tay R** | Nếp gấp cổ tay (cầm vô-lăng/chai/điện thoại vẫn đặt tại khớp, không dời lên vật) | `upper_limb` |
| `"11"` | `12333` | `10` | `right_wrist` | **cổ tay L** | Nếp gấp cổ tay (không đặt giữa cẳng tay) | `upper_limb` |
| `"12"` | `12334` | `11` | `left_hip` | **hông R** | Tâm khớp háng (không phải mép ngoài hông hay cạp quần) | `torso` |
| `"13"` | `12335` | `12` | `right_hip` | **hông L** | Tâm khớp háng | `torso` |
| `"14"` | `12336` | `13` | `left_knee` | **gối R** | Giữa xương bánh chè | `lower_limb` |
| `"15"` | `12337` | `14` | `right_knee` | **gối L** | Giữa xương bánh chè | `lower_limb` |
| `"16"` | `12338` | `15` | `left_ankle` | **cổ chân R** | Ngang mắt cá | `lower_limb` |
| `"17"` | `12339` | `16` | `right_ankle` | **cổ chân L** | Ngang mắt cá | `lower_limb` |

---

## 5. Quy tắc Left / Right (`R` vs `L`)

1. **`[BTC_OFFICIAL]` (`P17-G06`) — R/L theo ẢNH, cấm suy luận giải phẫu:**
   - Số **chẵn (`2–16`) = R (phải ảnh, `x` lớn hơn)**; số **lẻ (`3–17`) = L (trái ảnh, `x` nhỏ hơn)**, bất kể tài xế quay mặt, quay lưng, vặn mình hay ảnh xoay 90°.
   - Không đoán theo tay/chân giải phẫu, hướng nhìn, hay dây an toàn.
2. **`[BTC_OFFICIAL]` (`P17-G07`) — Kiểm tra liên tục chuỗi chi:**
   - Hai chuỗi `vai–khuỷu–cổ tay` (`6–8–10`, `7–9–11`) và `hông–gối–cổ chân` (`12–14–16`, `13–15–17`) mỗi bên phải liên tục, không bắt chéo sang bên đối diện.
3. **`[GEOMETRIC_INFERENCE]` (`P17-G08`) — Cảnh báo ảnh nằm ngang / xoay 90° (`15` frames trong Job 1623):**
   - Trong `15` frames góc nghiêng/fisheye ngang (`93, 96, 97, 98, 101, 103, 104, 105, 106, 108, 110, 112, 113, 115, 117`), độ nghiêng thân từ `66.3°–87.3°` nên các cặp R/L tách nhau theo trục **`y`** (`|dy| > |dx|`), khiến phép kiểm tra thô `x_R > x_L` báo giả `44` cặp đảo ngược.
   - Khi chiếu `R - L` lên trục vuông góc với trục thân (`mid_hip -> mid_shoulder`), **`40/44`** là nhiễu xoay góc máy, chỉ còn **`4`** ca đảo/chéo thật trong hệ tọa độ thân: `f093 (14-15)`, `f110 (10-11)`, `f112 (10-11)`, `f113 (10-11)`.
   - **Quy trình bắt buộc khi hai điểm gần trùng tọa độ `x` (`UNCERTAIN_CLASS`):** Không chọn bừa; tạo issue **`UNCERTAIN_CLASS`**, bỏ phiếu nhóm và gửi mentor chốt (nháp tool gắn cờ `UNCERTAIN_CLASS_LR` ở `f96, f103, f105, f106, f110, f112`).

---

## 6. Quy tắc Visibility (`visible`, `occluded`/`Q`, `outside`/`O`/`v0`)

- `[BTC_OFFICIAL]` (`P17-G10`, `P17-G14`):
  - **`visible`** (`occluded=False, outside=False`, không bấm phím): Thấy rõ. **Mắt nhắm** thấy khe mí và **đeo kính trong** thấy mắt vẫn là **`visible`** (chỉ `Q` khi vật khác che). Hai khớp `visible` **không được trùng tọa độ** (`P17-G22`).
  - **`occluded` (`v1`, phím `Q`)** (`occluded=True, outside=False`): Nằm trong khung, bị che (kính râm, tóc, tay, vô-lăng, ghế, tự che) **nhưng còn suy ra vị trí trong `±20 px`**. Đặt tại vị trí ước lượng + bấm `Q`.
  - **`outside` (`v0`, phím `O`)** (`occluded=False, outside=True`): Nằm ngoài khung hình, **HOẶC** khớp tay/chân (`8–11, 14–17`) bị che kín hoàn toàn không còn căn cứ suy ra vị trí. Điểm `outside` **không dùng đến tọa độ**.
- **Ba điều CẤM TUYỆT ĐỐI (`[BTC_OFFICIAL]`, `P17-G10`–`P17-G12`):**
  1. **Cấm dùng `hidden` (phím `H`)** thay cho `Q` (không lưu lên server CVAT).
  2. **Cấm bật đồng thời `occluded=True AND outside=True`** trên cùng 1 điểm (Job 1623 đang có **22 lỗi** này trên 13 frames).
  3. **Cấm bật `occluded=True` ở cấp skeleton** (bulk-occlude như `f093`: toàn bộ 14 điểm trong khung bị đánh `Q`, `visible=0`). Phải chọn từng sublabel điểm để bấm `Q`/`O`.

---

## 7. Quy tắc Occlusion & Inference + Ngưỡng sai số

- **`[BTC_OFFICIAL]` (`P17-G04`) — Ngưỡng sai số:** **`±5 px`** cho điểm `visible`; **`±20 px`** cho điểm `occluded`. *(Lưu ý `[GEOMETRIC_INFERENCE]` `P17-G26`: `18/30` frames có độ phân giải `1280×1024` hoặc `512×424` khác chuẩn `960×540` của BTC; việc scale ngưỡng theo đường chéo ảnh đang `needs_mentor`.)*
- **`[BTC_OFFICIAL]` (`P17-G15`) — Đầu/Mặt (`1–5`), Vai (`6,7`), Hông (`12,13`):**
  - Suy ra được từ hướng mặt, đối xứng đường giữa và thân người -> **mặc định `visible` hoặc `occluded` (`Q`)** khi ở trong khung, **không gán `outside` (`v0`)**.
  - Ngoại lệ duy nhất theo BTC: **tai (`4, 5`)** bị tóc/đầu che kín không còn bất kỳ dấu hiệu nào mới được gán `O` kèm issue `ATTRIBUTE_CHECK`.
- **`[BTC_OFFICIAL]` (`P17-G16`) — Tay & Chân (`8–11, 14–17`):**
  - Còn thấy đoạn kề hoặc bóng dáng để ước lượng trong `±20 px`: **`Q`**.
  - Bị báo/laptop/ghế/táp-lô che kín hoàn toàn, không suy ra được: **`O` (`v0`)**, không đặt bừa lên vật che.
- **`[AI_RECOMMENDATION]` (`P17-G27`) — Heuristic của tool `person17.py`:**
  - `Q_CONF = 0.5` (`< 0.5` -> `Q`); `V0_CONF = 0.3` chỉ áp dụng cho `LIMB_IDX = {8..11, 14..17}` (`< 0.3` -> `O`); đầu/vai/hông không bao giờ tự chuyển `O` chỉ vì `conf` thấp (trừ dải biên `BORDER_PX = 8`).

---

## 8. Cách xử lý cơ thể bị cắt (`OUT_OF_FRAME` / `TRUNCATION`)

- **Hiện trạng (`A05 §2`):** `OUT_OF_FRAME` xuất hiện ở **14/30 frames** (chủ yếu cổ chân `16, 17` và gối `14, 15` cắt ở đáy khung hoặc mép phải dưới táp-lô), `TRUNCATION` ở **9/30 frames** (`f092, f093, f095–f098, f100, f102, f118`).
- **`[BTC_OFFICIAL]` (`P17-G13`):**
  1. Điểm nằm ngoài `[0, W] × [0, H]` -> đánh **`O` (`outside`)**, **KHÔNG kéo điểm về mép ảnh**.
  2. Nếu khớp còn nằm trong khung (ví dụ dưới táp-lô/vô-lăng) nhưng vẫn suy ra được theo hướng đùi/cẳng chân -> đánh **`Q`**, không đánh `O` theo thói quen.
  3. **`[USER_OBSERVED]` vs `[AI_RECOMMENDATION]`**: Tool `person17.py` clamp tọa độ vào `[0, W] × [0, H]` và dùng `BORDER_PX = 8`, khiến `58/58` điểm `outside` hiện tại đều có tọa độ nằm trong khung (trong đó chỉ có `2` điểm nằm sát mép đáy `y=1024.0`: `f90 kp16`, `f102 kp17`). Khi duyệt tay, cần kiểm tra lại toàn bộ `56` điểm `outside` nằm sâu trong khung (`dist >= 8 px`).

---

## 9. Các lỗi thường gặp trong Job 1623 (Bằng chứng `A04` / `A05` / `A06`)

| Loại lỗi | Số lượng / Frame tiêu biểu | Mô tả thực tế & Cách sửa |
|---|---|---|
| **1. Cờ xung đột `occluded + outside` đồng thời** | **22 điểm / 13 frames** (`f116` có 5 điểm: `4,8,10,16,17`; `f93` có 3 điểm) | `[BTC_OFFICIAL]` cấm bật cả 2 cờ (`P17-G11`). Phải chọn dứt khoát `Q` hoặc `O`. |
| **2. Bulk-occlude cấp skeleton** | **`f093`** (`V=0, Q=14, O=3`, skeleton `occluded=True`) | Toàn bộ khớp rõ như mặt/vai/tay đều bị đánh `Q`; `7Q` tụt ~80 px. Tắt `occluded` cấp skeleton và đặt lại từng điểm. |
| **3. Thiếu skeleton hoàn toàn** | **`f100`**, **`f118`** (`0` shapes) | `[BTC_OFFICIAL]` bắt buộc gán đủ 1 skeleton (`P17-G01`). `f100` có nhòe tay trái; `f118` hai tay/vải xanh che mặt (`1..5` cần `Q`). |
| **4. Mắt/Tai trong khung gán `outside`** | **9 điểm / 8 frames** (`f93 kp2`, `f106 kp3,5`, `f98,103,104,105,116,117 kp4`) | `[USER_OBSERVED]` mâu thuẫn `P17-G15`. Nằm sâu trong khung (`58–227 px` cách biên) -> chuyển về `Q` (hoặc `O` + `ATTRIBUTE_CHECK` nếu tai không còn dấu hiệu). |
| **5. Trùng / dính khớp (`< 3 px`)** | **`f101`** (`kpt 2 visible` và `kpt 4 occluded` cách **`0.27 px`** tại `(265, 141)`) | Tách đúng vị trí đồng tử (`2`) và ống tai (`4`) theo `P17-G22`. |
| **6. Đặt sai vị trí khớp nghiêm trọng** | **`f117`** (`kpt 6` vai R đặt trên mũi/cằm); **`f116`** (`kpt 10` cổ tay R trên mũi, `kpt 8` lơ lửng ngoài thân); **`f094`** (`kpt 17` trên bàn tay cầm báo); **`f114`** (`kpt 11` giữa cẳng tay, `forearm_R = 0.139x` torso) | Đặt lại đúng khớp giải phẫu (`P17-G19`–`P17-G21`). |
| **7. Đảo chuỗi chân / vượt tỉ lệ xương** | **`f119`** (`kpt 17O` đặt cao hơn gối `15`); **`f115`** (`16Q/17Q` trên tapi cửa, cẳng chân dài hơn đùi); **`f113`** (4 điểm tự cắt cẳng tay + nghi đảo `10/11`) | Kiểm tra liên tục `hông–gối–cổ chân` và `vai–khuỷu–cổ tay` (`P17-G07`, `P17-G25`). |

---

## 10. Case khó đã xử lý & Case chưa thể kết luận

### 10.1 Case khó đã có hướng xử lý rõ ràng
- **Che khuất bởi vật dụng cabin (`f094` báo, `f096` laptop, `f105/f111` sách, `f109` túi):** Hông (`12,13`) giữ `Q` theo thân; gối/cổ chân (`14–17`) chỉ `Q` khi thấy đoạn nối suy ra được trong `±20 px`, còn bị che kín hoàn toàn thì đánh `O` (`v0`) và không đặt điểm bừa lên vật che (`f094 kp17`).
- **Tài xế gục/tay che mặt (`f118`):** Vẫn tạo skeleton, ước lượng vị trí đầu (`1–5`) theo dáng đầu/vai và đánh `Q` (`P17-G15`).
- **Nhòe chuyển động (`f100`, `f108`, `f113`):** Đặt tại tâm khớp ước lượng, đánh `Q` nếu không phân biệt rõ ranh giới khớp.
- **IR tối (`f099`, `f110`, `f112`, `f116`):** Tăng sáng trên CVAT, vẫn gán đủ 17 điểm, không bỏ qua frame nếu vẫn thấy tài xế.

### 10.2 Case chưa thể kết luận (`needs_mentor` / `NEEDS HUMAN DECISION`)
1. **R/L trên ảnh nằm ngang / fisheye xoay ~90°** (`f096, f103, f105, f106, f110, f112` và các frame nghiêng có cặp R/L gần trùng `x`): Chờ mentor chốt tiêu chí chọn R/L khi `|dx| ≈ 0` (`issues.md` A4, F3; `w2-face50-pose17.md §8 Q2`).
2. **Chuẩn hóa sai số `±5 / ±20 px` theo độ phân giải** (`1280×1024` và `512×424` vs `960×540` của BTC — `18/30` frames): Chờ mentor xác nhận (`issues.md` A1; `P17-G26`).
3. **Tên label `person_vf17` vs `person` trong BTC V1** (`issues.md` A3): Giữ nguyên `person_vf17`, chờ xác nhận.
4. **Cơ chế chấm điểm `outside` và kích thước mặt/người tối thiểu trong IR tối** (`w2-face50-pose17.md §8 Q4, Q8`).
5. **10 frame `source=file` ban đầu (`f91, 92, 97, 98, 103, 104, 109, 110, 115, 116`):** Đã chuyển sang `source=manual`, chờ mentor chốt việc có được xóa vẽ lại hoàn toàn hay chỉ tinh chỉnh (`§8 Q3`).

---

## 11. Ví dụ trực quan (Overlays đã xác minh trong `artifacts/pose17_research/evidence/overlays/`)

- **Baseline sạch nhất (IR):** [`f090_G06_091.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/evidence/overlays/f090_G06_091.jpg) (`14V/2Q/1O`, `16O` sát mép đáy `y=1024`).
- **Bulk-occlude cấp skeleton + chéo chân:** [`f093_G06_094.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/evidence/overlays/f093_G06_094.jpg) (`V=0/Q=14/O=3`, `7Q` tụt thấp, `2O` trên trán).
- **Che bởi báo & đặt cổ chân lên tay:** [`f094_G06_095.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/evidence/overlays/f094_G06_095.jpg) (`17O` đặt ngay trên bàn tay trái).
- **Thiếu skeleton + nhòe chuyển động:** [`f100_G06_101.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/evidence/overlays/f100_G06_101.jpg) · **Thiếu skeleton + tay che mặt:** [`f118_G06_119.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/evidence/overlays/f118_G06_119.jpg).
- **Trùng tọa độ `2=4` (`0.27 px`):** [`f101_G06_102.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/evidence/overlays/f101_G06_102.jpg).
- **Fisheye ngang (đầu bên phải) & đảo toàn bộ 7 cặp R/L:** [`f106_G06_107.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/evidence/overlays/f106_G06_107.jpg) · **Fisheye ngang tối + khoanh tay:** [`f110_G06_111.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/evidence/overlays/f110_G06_111.jpg).
- **Độ phân giải thấp `512×424` tối + dính cổ tay:** [`f112_G06_113.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/evidence/overlays/f112_G06_113.jpg).
- **IR tối nhất (`L=12.8`) + 5 xung đột `occ+out` + `10O` trên mũi:** [`f116_G06_117.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/evidence/overlays/f116_G06_117.jpg).
- **Vai `6` đặt lên cằm/mũi:** [`f117_G06_118.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/evidence/overlays/f117_G06_118.jpg) · **Cổ chân `17O` cao hơn gối `15`:** [`f119_G06_120.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/evidence/overlays/f119_G06_120.jpg).

---

## 12. Thay đổi giữa các Guideline Version & 3 Trục phiên bản

| Trục phiên bản | Tiến hóa ghi nhận được (`A02_version_historian.md`) |
|---|---|
| **1. Guideline version** | **Pre-BTC (16/11, `3f5391cb`):** Tự viết, dùng **trái/phải giải phẫu** theo người, chưa có chính sách `v0` cho tay/chân.<br>**BTC V1 + G06 (17/11, `cd129065`):** Chuyển hoàn toàn sang **trái/phải theo ảnh**, bổ sung `outside` (`v0`) cho tay/chân không suy ra được, ngưỡng `±5/±20 px`, quy trình issue `UNCERTAIN_CLASS`.<br>**G06 v2.0 (18/11):** Tách rõ Tier A (`G06_POSE17_GUIDELINE.md`) và Tier B (`POSE17_GENERAL_GUIDELINE.md`, `P17-G01`–`P17-G30`), gắn nhãn `BTC_OFFICIAL` / `USER_OBSERVED` / `GEOMETRIC_INFERENCE` / `AI_RECOMMENDATION`, bổ sung bằng chứng định lượng 30 frames. |
| **2. Annotation version** | `source=file` (10 pre-label `1163231..1163240`) -> `source=auto` (Push #1–#4, 18 shapes) -> `source=manual` (chuyển đổi 17/11 19:29–19:30, 28 shapes) -> bản live 18/11 09:17 (đã sửa tay 25/28 frames, xóa bản trùng `1163232` ở `f92`, vẫn `0` gold). |
| **3. Tool / Pipeline version** | `week2.py` (`spm` + `LOW_CONF_Q=0.5`) -> `person17.py` (`yolo`/`vitpose` + xoay 4 hướng) -> `person17.py auto` (`merge_consensus` + `V0_CONF=0.3` giới hạn trong `LIMB_IDX` + `enforce_image_lr`). |

---

## 13. Bài học từ việc sửa Annotation (`A02` & `A06` Human-Edit Deltas)

1. **`source=manual` KHÔNG đồng nghĩa `human_approved`:** Việc chuyển đổi `source=file`/`auto` sang `source=manual` tối 17/11 làm thay đổi toàn bộ `shape_id`, khiến lệnh `cvat-tools pose rollback --run` bị vô hiệu (`issues.md` A8/F10). Mọi chỉnh sửa hàng loạt phải giữ backup JSON đầy đủ.
2. **Nhật ký sửa tay thực tế (`before_manual` -> `18/11 09:17`):** Người gán đã sửa **25/28 frames** (`148` lần di chuyển khớp, `51` lần đổi trạng thái; chỉ `f90, f91, f95` giữ nguyên) và đã xóa skeleton trùng `1163232` ở `f92`. Tuy nhiên, kéo cả skeleton tạo ra micro-drag `0.12–0.50 px` ở 5 frames (`104, 106, 108, 114, 116`).
3. **Lỗi mới phát sinh từ thao tác tay:** Quá trình sửa tay đã vô tình tạo ra **22 cặp cờ xung đột `occluded=True AND outside=True`**, **9 điểm mắt/tai `outside` trong khung**, **bulk-occlude `f093`**, **dính khớp `2=4` ở `f101`**, và **cẳng tay `f114` ngắn bất thường (`0.139x` torso)** sau khi dịch `kpt 8` đi `65.31 px`.
4. **Hành động bắt buộc tiếp theo:** Không tự động xem các chỉnh sửa tay hiện tại là `gold`. Cần chạy QC deterministic dọn sạch 22 xung đột `occ+out`, `f093`, `f101`, `f114`–`f119`, gán mới `f100` và `f118`, rồi mới duyệt `human_approved`.
