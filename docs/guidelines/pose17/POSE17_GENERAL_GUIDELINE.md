# Pose17 General Annotation Guideline (Tier B — Reusable SSOT)

> **Tài liệu chuẩn tái sử dụng cho mọi job Pose 17 điểm (`person_vf17` / COCO-17).**  
> Mọi quy tắc đều gắn **Rule ID ổn định (`P17-G01`..`P17-G30`)** để `pose17_rules.csv`, script QC (`w2_qc_rules.py`), và bộ đánh giá (`eval_pose17.py`) tham chiếu trực tiếp.

---

## 1. Phân loại nguồn & Trục phiên bản

### 1.1 Bốn loại nguồn quy tắc (`source_type`)
1. **`BTC_OFFICIAL`**: Quy định trực tiếp trong tài liệu chính thức BTC V1 (`HumanPose17_Annotation_Guideline_V1.docx`, được đồng bộ vào `weeks/guidelines/w2-face50-pose17.md`). Luôn có quyền ưu tiên cao nhất khi xảy ra xung đột.
2. **`USER_OBSERVED`**: Hành vi/mẫu quan sát được từ thao tác gán nhãn thực tế của người dùng (ví dụ Job 1623). **KHÔNG** tự động nâng cấp thành quy tắc chính thức; phải ghi rõ `confidence` và cảnh báo nếu mâu thuẫn với `BTC_OFFICIAL`.
3. **`GEOMETRIC_INFERENCE`**: Quy tắc suy luận từ hình học/giải phẫu học (ví dụ: trục thân `mid_hip -> mid_shoulder` cho ảnh xoay 90°, tỉ lệ chiều dài xương chuẩn hóa theo `torso_height`).
4. **`AI_RECOMMENDATION`**: Ngưỡng và heuristic của pipeline/tool (`person17.py`, `w2_qc_rules.py`, VLM audit). Dùng để tạo nháp và lọc QC tự động, không thay thế quyết định của người duyệt/mentor.

### 1.2 Ba trục phiên bản độc lập
1. **Annotation version**: Trạng thái nhãn thực tế (`source=file` pre-label -> `source=auto` tool draft -> `source=manual` pre-review -> `human_approved` / `gold`).
2. **Guideline version**: Phiên bản tài liệu quy ước (`Pre-BTC 16/11` -> `BTC V1 + G06 17/11` -> `Tier A/B v2.0 18/11`).
3. **Tool/pipeline version**: Phiên bản code sinh nháp & QC (`week2.py spm` -> `person17.py yolo/vitpose` -> `person17.py auto + V0_CONF + enforce_image_lr`).

---

## 2. Bảng tổng hợp quy tắc (`P17-G01` – `P17-G30`)

| `rule_id` | Nhóm | Tóm tắt quy tắc | `source_type` | `source_ref` | `confidence` | `status` |
|---|---|---|---|---|---|---|
| `P17-G01` | Scope | Chỉ gán 1 tài xế; bỏ qua hành khách/ảnh in/phản chiếu; không có tài xế thì bỏ qua frame | `BTC_OFFICIAL` | `w2-face50-pose17.md §1, §5A.A` | `high` | `approved` |
| `P17-G02` | Schema | Chế độ **Shape** (không Track), 1 skeleton đủ 17 điểm `1..17`, cấm tạo/đổi tên label | `BTC_OFFICIAL` | `w2-face50-pose17.md §1, §3` | `high` | `approved` |
| `P17-G03` | Review | Pre-label/`source=auto` chỉ là nháp; phải duyệt tọa độ & trạng thái; `source=manual` ≠ `human_approved` | `BTC_OFFICIAL` | `w2-face50-pose17.md §1, §6`; `issues.md A6, A8` | `high` | `approved` |
| `P17-G04` | Tolerance | Sai số cho phép: **`±5 px` (visible)**, **`±20 px` (occluded)** | `BTC_OFFICIAL` | `w2-face50-pose17.md §3, §7` | `high` | `approved` |
| `P17-G05` | Issue | Case không chắc tạo CVAT issue (`UNCERTAIN_CLASS`, `UNCERTAIN_BOUNDARY`, `UNCERTAIN_SCOPE`, `ATTRIBUTE_CHECK`, `LOW_VISIBILITY`) + bỏ phiếu nhóm | `BTC_OFFICIAL` | `w2-face50-pose17.md §5B` | `high` | `approved` |
| `P17-G06` | Left/Right | R (chẵn `2–16`) = **phải ảnh**, L (lẻ `3–17`) = **trái ảnh**, bất kể quay lưng hay xoay 90°; cấm suy luận giải phẫu | `BTC_OFFICIAL` | `w2-face50-pose17.md §3, §4` | `high` | `approved` |
| `P17-G07` | Left/Right | Chuỗi `vai–khuỷu–cổ tay` và `hông–gối–cổ chân` mỗi bên phải liên tục, không bắt chéo sang bên kia | `BTC_OFFICIAL` | `w2-face50-pose17.md §3, §5A.G` | `high` | `approved` |
| `P17-G08` | Left/Right | Ảnh xoay 90° / người nằm ngang (`\|dy\| > \|dx\|`): chiếu `R - L` lên trục vuông góc `mid_hip -> mid_shoulder` để kiểm tra, tạo `UNCERTAIN_CLASS` | `GEOMETRIC_INFERENCE` | `A06 §2.4`; `w2-face50-pose17.md §4, §8 Q2` | `medium` | `needs_mentor` |
| `P17-G09` | Left/Right | `enforce_image_lr`: đảo đồng loạt cả 8 cặp R/L khi `x_R - x_L < 0` theo trọng số `LR_PAIRS`; gắn `UNCERTAIN_CLASS_LR` khi `sep < 0.12 * torso` | `AI_RECOMMENDATION` | `person17.py` (`enforce_image_lr`, `LR_MIN_SEP=0.12`) | `medium` | `approved` |
| `P17-G10` | Visibility | Dùng 3 trạng thái: `visible`, `occluded` (`Q`), `outside` (`O`). **Cấm dùng `hidden` (`H`)** | `BTC_OFFICIAL` | `w2-face50-pose17.md §5` | `high` | `approved` |
| `P17-G11` | Visibility | **Cấm đặt đồng thời `occluded=True AND outside=True`** trên cùng 1 keypoint | `BTC_OFFICIAL` | `w2-face50-pose17.md §5`; `A04 §1, §5` | `high` | `approved` |
| `P17-G12` | Visibility | **Cấm bật `occluded=True` ở cấp skeleton** (bulk-occlude); chỉ đặt cờ trên từng sublabel điểm | `BTC_OFFICIAL` | `w2-face50-pose17.md §5`; `A04 §1` | `high` | `approved` |
| `P17-G13` | Visibility | Điểm `outside` (`v0`) không dùng tọa độ; không kéo điểm ngoài khung vào mép ảnh | `BTC_OFFICIAL` | `w2-face50-pose17.md §5` | `high` | `approved` |
| `P17-G14` | Visibility | Mắt nhắm thấy khe mí hoặc đeo kính trong thấy mắt = **`visible`**; kính râm che mắt = **`occluded` (`Q`)** | `BTC_OFFICIAL` | `w2-face50-pose17.md §5, §5A.C` | `high` | `approved` |
| `P17-G15` | Visibility | Đầu/mặt (`1–5`), vai (`6,7`), hông (`12,13`) trong khung: luôn **`visible` hoặc `Q`**, không gán `O` (tai che hết không dấu hiệu mới `O` + `ATTRIBUTE_CHECK`) | `BTC_OFFICIAL` | `w2-face50-pose17.md §5` | `high` | `approved` |
| `P17-G16` | Visibility | Tay/chân (`8–11, 14–17`) trong khung: còn suy ra trong `±20 px` từ đoạn kề = **`Q`**; che kín hoàn toàn không căn cứ = **`O` (`v0`)** | `BTC_OFFICIAL` | `w2-face50-pose17.md §5, §5A.D` | `high` | `approved` |
| `P17-G17` | Visibility | Quan sát thực tế có `eye/ear` gán `outside` trong khung (9 ca) & `occ+out` (22 ca) — là lỗi cần sửa, **không phải quy tắc** | `USER_OBSERVED` | `A04 §3, §5`; `A06 §3.3` | `low` | `proposed` |
| `P17-G18` | Landmark | Đầu (`1–5`): `1` chóp mũi; `2,3` tâm đồng tử / khe mí; `4,5` ống tai (không dái/chóp tai) | `BTC_OFFICIAL` | `w2-face50-pose17.md §3`; `A03 §2` | `high` | `approved` |
| `P17-G19` | Landmark | Thân (`6,7,12,13`): `6,7` tâm khớp vai (điểm xoay tay); `12,13` tâm khớp háng (không đặt ở cạp quần/mép ngoài) | `BTC_OFFICIAL` | `w2-face50-pose17.md §3`; `A03 §2` | `high` | `approved` |
| `P17-G20` | Landmark | Tay (`8–11`): `8,9` tâm khuỷu; `10,11` nếp gấp cổ tay (cầm vô-lăng/chai/điện thoại vẫn đặt tại cổ tay) | `BTC_OFFICIAL` | `w2-face50-pose17.md §3, §5A.G` | `high` | `approved` |
| `P17-G21` | Landmark | Chân (`14–17`): `14,15` giữa xương bánh chè; `16,17` ngang mắt cá (không đặt lên túi/cửa/đùi) | `BTC_OFFICIAL` | `w2-face50-pose17.md §3`; `A05 §2` | `high` | `approved` |
| `P17-G22` | Landmark | Hai khớp `visible` **không được trùng tọa độ**; tránh dính `< 3 px` giữa khớp khác loại (`2=4` ở `f101`) | `BTC_OFFICIAL` | `w2-face50-pose17.md §3`; `A06 §2.2` | `high` | `approved` |
| `P17-G23` | Geometry | Mọi điểm `visible` và `occluded` phải nằm trong `[0, W] × [0, H]` | `GEOMETRIC_INFERENCE` | `A06 §2.1`; `w2_qc_rules.py` | `high` | `approved` |
| `P17-G24` | Geometry | Chiều dài xương chuẩn hóa theo `torso_height` nằm trong `[0.15x, 2.5x median]` (cảnh báo như `f114` `0.139x`) | `GEOMETRIC_INFERENCE` | `A06 §2.3` | `medium` | `proposed` |
| `P17-G25` | Geometry | Kiểm tra đảo chuỗi chi (`ankle` cao hơn `knee` ở `f119`, `shank > 1.5x thigh` ở `f115`) và tự cắt chéo bất thường (`f113`) | `GEOMETRIC_INFERENCE` | `A05 §3`; `A06 §2.5` | `medium` | `proposed` |
| `P17-G26` | Tolerance | Chuẩn hóa ngưỡng `±5 px` / `±20 px` theo đường chéo ảnh khi độ phân giải lệch `960×540` (`1280×1024`, `512×424`) | `GEOMETRIC_INFERENCE` | `A05 §1, §4`; `issues.md A1` | `medium` | `needs_mentor` |
| `P17-G27` | Pipeline | Ngưỡng nháp `person17.py`: `Q_CONF=0.5`, `V0_CONF=0.3` chỉ áp dụng cho `LIMB_IDX={8..11,14..17}`, `BORDER_PX=8` | `AI_RECOMMENDATION` | `person17.py`; `w2-face50-pose17.md §5` | `medium` | `approved` |
| `P17-G28` | Pipeline | `detect()` xoay 4 hướng (`rot_bias=0.08`, `torso_quality<0.6`), `merge_consensus` (`AGREE_FRAC=0.35`, `DISAGREE_CONF=0.4`), `MIN_PERSON_PX=60` | `AI_RECOMMENDATION` | `person17.py`; `A03 §6` | `medium` | `approved` |
| `P17-G29` | Pipeline | Đồng bộ topology 18 cạnh SVG (`person_vf17`, bỏ `[2,3]`) vs 19 cạnh COCO (`schema.json`) khi render/export | `AI_RECOMMENDATION` | `A03 §3` | `high` | `approved` |
| `P17-G30` | Pipeline | QC deterministic (`w2_qc_rules.py`) phải bắt `occ+out`, skeleton `occ=True`, `face/torso out`; luôn giữ backup trước khi đổi `source` (vì đổi ID làm gãy `rollback --run`) | `AI_RECOMMENDATION` | `A02 §2.3`; `A04 §7`; `issues.md A8` | `high` | `approved` |

---

## 3. Chi tiết nhóm quy tắc cốt lõi

### 3.1 Quy ước 17 điểm (`person_vf17` / COCO-17)
- **Thứ tự cố định `1..17` (COCO `0..16`)**: `1` mũi, `2` mắt R, `3` mắt L, `4` tai R, `5` tai L, `6` vai R, `7` vai L, `8` khuỷu R, `9` khuỷu L, `10` cổ tay R, `11` cổ tay L, `12` hông R, `13` hông L, `14` gối R, `15` gối L, `16` cổ chân R, `17` cổ chân L.
- **Số chẵn (`2, 4, 6, 8, 10, 12, 14, 16`) = R (phải ảnh)**; **Số lẻ (`3, 5, 7, 9, 11, 13, 15, 17`) = L (trái ảnh)** (`P17-G06`).

### 3.2 Ma trận quyết định trạng thái (`visible` vs `Q` vs `O`)
1. **Visible** (`occluded=False, outside=False`): Thấy rõ trong khung, kể cả mắt nhắm thấy khe mí hoặc đeo kính trong thấy mắt (`P17-G14`).
2. **Occluded (`Q`, `v1`)** (`occluded=True, outside=False`): Nằm trong khung, bị che nhưng ước lượng được trong `±20 px` từ khớp kề/tỉ lệ thân. Mặc định cho **đầu/mặt (`1–5`), vai (`6,7`), hông (`12,13`)** khi bị che (`P17-G15`).
3. **Outside (`O`, `v0`)** (`occluded=False, outside=True`): Nằm ngoài `[0, W] × [0, H]`, **HOẶC** là tay/chân (`8–11, 14–17`) bị che kín hoàn toàn không còn căn cứ suy luận (`P17-G16`). Cấm đặt đồng thời `occluded=True` (`P17-G11`).
4. **Cấm tuyệt đối**: Dùng `hidden` (`H`) (`P17-G10`), bật `occluded` trên cả skeleton (`P17-G12`), hoặc kéo điểm ngoài biên vào mép ảnh (`P17-G13`).

### 3.3 Chuẩn hóa kiểm tra hình học & Pipeline (`P17-G23` – `P17-G30`)
- Mọi công cụ đánh giá (`eval_pose17.py`, `gold.py`) phải lưu và tách riêng trạng thái `visible` (`±5 px`), `occluded` (`±20 px`), và loại bỏ `outside` khỏi phép đo tọa độ (`P17-G04`, `P17-G13`).
- Trước khi chạy bất kỳ thao tác ghi/đổi `source` hàng loạt nào trên CVAT, bắt buộc lưu snapshot JSON backup vì thay đổi `shape_id` sẽ vô hiệu hóa `rollback --run` (`P17-G30`).
