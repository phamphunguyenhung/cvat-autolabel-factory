# Guideline nội bộ — Week 2: Face 50 điểm + Pose 17 điểm (nhóm G06)

> **Tự viết, chưa phải bản chính thức của BTC.** Nguồn: cấu trúc label đọc từ CVAT edufun (job 1975, 1623), khung mẫu skeleton, và quy ước keypoint của Day 4 (`day04/.../docs/GUIDELINE.md`). Task và job trên CVAT không gắn guideline (`guide_id = null`). Mục 8 liệt kê những điều **cần BTC xác nhận**; trong lúc chờ, cả nhóm dùng đúng các quy ước mặc định dưới đây để nhãn đồng nhất.

## 1. Phạm vi

| | Face | Pose |
|---|---|---|
| Task | 473 `W2-FACE-G6-T1` (150 frame, 5 job × 30) | 402 `week2-human-pose/G06` |
| Job của leader | 1975 (frame 90–119) | 1623 (frame 90–119) |
| Ảnh | 640×480, người lái xe trong cabin (màu) | 1280×1024, trong cabin, có ảnh hồng ngoại xám/ban đêm |
| Hình | 7 skeleton / ảnh, 50 điểm | 1 skeleton `person_vf17` / ảnh, 17 điểm |
| Chế độ vẽ | **Shape** (không Track) | **Shape** |

- Số frame CVAT = số trong tên file − 1 (frame 90 = `G06_091.jpg`).
- Mỗi ảnh chỉ gán **người lái/người chính trong khung**. Người ngồi sau, ảnh phản chiếu, hình in: không gán.
- Mỗi ảnh có đủ **7 skeleton mặt** (mỗi label đúng 1 cái) hoặc **1 skeleton người**. Không thiếu, không thừa.

## 2. Face: 7 skeleton, 50 điểm

Mẫu: ![mẫu face](images/face50_template.png)

Tên điểm trên CVAT chỉ là số `0…49`. Số điểm là thứ tự cố định, **không được đổi**.

| Label | Điểm | Số điểm | Cách đặt (theo khung mẫu nhìn thẳng) |
|---|---|---:|---|
| `longmaytrai` | 0–4 | 5 | Lông mày bên **trái ảnh**: từ đầu ngoài (0) vòng cung lên đỉnh (2) tới đầu trong sát sống mũi (4) |
| `longmayphai` | 5–9 | 5 | Lông mày bên **phải ảnh**: từ đầu trong (5) qua đỉnh (7) tới đầu ngoài (9) |
| `songmui` | 10–13 | 4 | Sống mũi từ giữa hai mắt (10) xuống chóp mũi (13), cách đều |
| `mattrai` | 14–21 | 8 | Mắt bên trái ảnh. 14 khóe ngoài, 15–17 mép mí trên (trái → phải), 18 khóe trong, 19–21 mép mí dưới (phải → trái) |
| `matphai` | 22–29 | 8 | Mắt bên phải ảnh. 22 khóe trong, 23–25 mí trên, 26 khóe ngoài, 27–29 mí dưới (phải → trái) |
| `moingoai` | 30–41 | 12 | Mép **ngoài** môi: 30 khóe miệng trái ảnh, 31–35 viền môi trên (33 giữa), 36 khóe phải, 37–41 viền môi dưới (39 giữa) |
| `moitrong` | 42–49 | 8 | Mép **trong** môi (khe miệng): 42 khóe trái, 43–45 trên (44 giữa), 46 khóe phải, 47–49 dưới (48 giữa) |

Quy tắc đặt điểm:
1. Phóng to ≥ 300 % khi đặt mắt và môi. Điểm đặt **lên mép/đường viền thật**, không đặt vào vùng da bên cạnh.
2. Điểm mí mắt nằm trên mép mi, 3 điểm cách đều giữa hai khóe; điểm giữa (16, 24) ngay trên tâm con ngươi, (20, 28) ngay dưới.
3. Hai khóe mắt dùng chung cho mí trên và mí dưới: 14/18 và 22/26 nằm đúng chỗ mí trên gặp mí dưới.
4. Môi: vòng ngoài và vòng trong là **hai vòng khác nhau**. Miệng ngậm vẫn đặt vòng trong ở đường khép môi. Vòng trong không chạm hoặc vượt vòng ngoài.
5. Lông mày đặt dọc **đường giữa sợi lông mày**, không đặt theo viền trên hay dưới. Mày thưa hoặc bị tóc che: ước lượng theo xương mày, đánh `occluded`.
6. Sống mũi: 4 điểm gần thẳng hàng theo trục mũi, không lệch theo bóng đổ.

## 3. Pose: 1 skeleton, 17 điểm (thứ tự COCO)

Mẫu: ![mẫu pose](images/pose17_template.png)

| # | Điểm | # | Điểm | # | Điểm |
|---:|---|---:|---|---:|---|
| 1 | mũi | 7 | vai phải | 13 | hông phải |
| 2 | mắt trái | 8 | khuỷu trái | 14 | gối trái |
| 3 | mắt phải | 9 | khuỷu phải | 15 | gối phải |
| 4 | tai trái | 10 | cổ tay trái | 16 | cổ chân trái |
| 5 | tai phải | 11 | cổ tay phải | 17 | cổ chân phải |
| 6 | vai trái | 12 | hông trái | | |

"Trái/phải" ở **pose** là trái/phải **của người**. Trong khung mẫu (người quay mặt về camera) các điểm chẵn nằm bên phải ảnh.

- Đặt vào **tâm khớp**, không đặt lên viền áo (hông ở khớp hông, không ở cạp quần).
- Ngồi trong xe: nửa dưới thường bị vô-lăng, ghế, cửa che. Hông, gối, cổ chân không thấy: xem mục 5.
- Ảnh hồng ngoại xám, thiếu sáng: vẫn gán theo hình dáng; không đoán nếu cả hai đoạn chi lân cận đều không thấy.

## 4. Trái/phải: quy tắc mặc định

| | Quy ước dùng trong nhóm | Lý do |
|---|---|---|
| Pose | trái/phải của **người** | Khớp thứ tự COCO và khung mẫu (điểm chẵn = trái của người) |
| Face | `trai` = bên **trái ảnh** khi nhìn mặt thẳng, tức **phải của người** | Khung mẫu đặt `longmaytrai`, `mattrai` ở bên trái ảnh |

Hai quy ước này **ngược nhau**, đây là chỗ dễ nhầm nhất. Trước khi gán mặt nghiêng, nói to "mặt này nhìn sang trái/phải ảnh". Phần nằm về phía trái ảnh là `trai`; khi mặt quay đi, mắt/mày phía xa vẫn giữ nhãn của bên đó, **không đổi chỗ**.

Cần BTC xác nhận (mục 8, câu 1): nếu họ định nghĩa `trai` theo người thì toàn bộ nhãn mặt phải đổi.

## 5. Cờ trạng thái điểm (phím tắt CVAT)

| Tình huống | Cờ | Phím |
|---|---|---|
| Thấy rõ | bình thường | không bấm |
| **Bị che khuất** (kính râm, tóc, tay, vô-lăng, ghế, tự che do nghiêng người) | `occluded` | **Q** |
| **Nằm ngoài biên ảnh** (bị cắt khỏi khung) | `outside` | **O** |

Cách dùng: chọn đúng điểm trong skeleton (không phải cả skeleton) rồi bấm Q hoặc O.

- Điểm bị che vẫn **đặt tại vị trí ước lượng** theo khớp/đường nét lân cận, rồi bấm **Q**.
- Điểm ngoài biên: bấm **O**, **không** kéo về mép ảnh.
- **Không dùng `hidden` (phím H)** thay Q: không lưu lên server.
- Kính râm tối: mắt đặt theo gọng/tròng, bấm Q; kính trong thấy mắt thì bình thường.
- Mặt nghiêng mạnh: mày, mắt, má phía xa bị che thì Q.
- Miệng bị che (tay, khẩu trang): môi bấm Q, đặt theo dáng môi ước lượng.
- Pose ngồi trong xe: hông, gối, cổ chân bị ghế/vô-lăng che thì Q nếu ước lượng được; ra ngoài khung thì O.
- Không điền bừa: điểm không thể ước lượng ngay cả gần đúng, ghi lại để hỏi BTC (mục 8 câu 7).

## 5A. Edge case và cách xử lý (khảo sát toàn bộ 150 ảnh mặt task 473 và 30 ảnh pose job 1623)

Ảnh là camera giám sát tài xế (DMS) trong cabin. Có **hai kiểu ảnh**: ảnh màu góc rộng ban ngày, và ảnh **hồng ngoại xám (IR) ban đêm, méo fisheye**. Danh sách frame theo từng nhóm: `week02/task473-face/EDGE_CASES.md`. Bảng từng frame của job mình: `job1975-face50/EDGE_CASES.md`, `job1623-pose17/EDGE_CASES.md`.

### A. Ai là người được gán
- Chỉ gán **tài xế** (người ngồi ghế lái, tay ở vô-lăng hoặc ngồi đúng vị trí ghế lái). Hành khách phía sau hoặc bên cạnh (nhiều frame có, ví dụ f0, f21, f60, f99, f107, f113, f117) **không gán**, kể cả khi họ lớn hoặc rõ hơn.
- Ảnh IR chỉ có một người: người đó là tài xế.
- Không thấy tài xế hoặc chỉ thấy lưng/đầu bị cắt gần hết: không vẽ, ghi frame vào nhật ký `review/` (cần BTC xác nhận có được bỏ trống không, mục 8 câu 8).

### B. Mặt xoay, nghiêng, ngửa (nhóm gây sai nhiều nhất)
- **Xoay ~90° (người nằm ngang trong ảnh fisheye IR)**, ví dụ f10, f20, f34, f44, f58, f67, f68, f92, f106, f116, f124, f142: **đưa mặt về thẳng đứng trong đầu** (cằm hướng xuống), rồi mới xác định `trai/phai`. Bên nào nằm bên trái khi mặt thẳng đứng là `trai`. Không gán `trai/phai` theo vị trí trái/phải trên ảnh đã xoay.
- Mặt **quay nghiêng (profile)**: giữ nhãn theo bên đó (bên nằm phía trái khi nhìn mặt thẳng). Mày, mắt, má phía xa bị sống mũi/má che: Q. Vòng môi vẫn đủ 20 điểm, phần khuất Q.
- **Ngửa mặt lên** (f96, f97, f100, f105, f112, f118): mắt nhìn ngược chiều bình thường, mí trên vẫn là mí phía đỉnh đầu. Mũi che môi trên: môi ngoài phía trên Q.
- **Cúi mặt xuống** (f103, f111, f114, f115, f35, f46): mí trên che phần lớn mắt, mí dưới sát nhau. Đặt điểm theo mép mí thật; nếu mi mắt khép gần như một đường, các điểm mí trên và mí dưới nằm sát nhau (cách nhau vài pixel), không kéo ra để trông giống mẫu.

### C. Che khuất (đánh Q, đặt ở vị trí ước lượng)
| Vật che | Frame ví dụ | Xử lý |
|---|---|---|
| Kính trong có phản sáng/lóa | f18, f19, f20 | Mắt vẫn thấy mờ: đặt theo mí, không Q. Nếu lóa che hết mắt: Q |
| Kính râm / tròng tối | f6, f45, f106, f116, f144, f147 | 16 điểm hai mắt Q, đặt theo hình dáng tròng kính/gọng, tròng ngay trên mí ước lượng |
| Tay đưa lên mặt (chỉnh kính, gãi, che) | f102, f75, f116 | Điểm bị tay che Q; điểm không bị che đặt bình thường |
| Điện thoại áp tai | f8, f9, f22, f73, f117 | Thường che má/tai, không che mắt-miệng: chỉ Q điểm bị che |
| Chai/đồ ăn/đồ uống sát miệng | f19, f59, f55, f96 | Môi ngoài và môi trong phần bị che: Q |
| Sách, báo, laptop che mặt | f11, f44, f58, f67, f92, f34, f37 | Điểm bị che Q. Nếu che hết mặt: xem mục A (không vẽ, ghi nhật ký) |
| Ba lô, túi che đầu | f64 | Thường che hầu hết mặt: không vẽ nếu không đặt được ≥ 3 nhóm đặc điểm thấy rõ |
| Tóc dài che mày/mắt/má | f9, f46, f115 | Mày hoặc mắt bị tóc che: Q, đặt theo xương mày/khóe mắt ước lượng |
| Nón lưỡi trai, mũ len che mày | f25, f81, f123, f127 | Lông mày bị che: Q |
| Ngón tay/bàn tay giơ gần trán | f107, f126, f129, f143, f149 | Che mày/trán: Q |
| Râu, ria che viền môi | f0, f27, f103 | Đặt viền môi ở chỗ thấy được; nếu râu che hẳn viền môi trên: Q |
| Khăn trùm đầu (hijab) | f139 | Không che mặt: gán bình thường |

### D. Cắt khỏi khung (đánh O)
- Đầu sát hoặc vượt mép ảnh (f2, f68, f110, f20 sát phải, ảnh IR khi người cúi sát camera): điểm **nằm ngoài ảnh = O**. Điểm còn trong ảnh gán bình thường. Không kéo điểm về mép.
- Pose: ảnh IR nhìn thẳng thường cắt ở đùi/gối, ảnh màu nhìn nghiêng thường cắt bên phải. Cổ chân (16, 17) và nhiều khi gối (14, 15) nằm ngoài ảnh: **O**. Vẫn che bởi vô-lăng, ghế, bàn đạp nhưng còn trong ảnh: **Q**.

### E. Điểm chuẩn mắt, miệng
- **Mắt nhắm** (f17, f39, f40, f99): hai mí nằm sát nhau trên đường khép mi. Khóe ngoài và khóe trong đặt đúng khóe. Không vẽ mắt mở.
- **Miệng mở, ngáp, nói** (f99, f133, f119, f120): vòng môi ngoài bám mép đỏ ngoài; vòng môi trong bám mép trong của khe miệng (nơi lộ răng/lưỡi), thành một hình mở. Vòng trong vẫn nằm trong vòng ngoài.
- **Miệng ngậm**: vòng trong thành một đường hẹp trên đường khép môi.
- **Cười lớn, mắt híp** (f119, f120, f147): mí híp, điểm 16/24 và 20/28 gần nhau; khóe mắt đặt đúng khóe.

### F. Điều kiện ảnh
- **Ảnh IR tối, mặt nhỏ** (f5, f13, f14, f24, f37, f38, f61, f84–f86, f94, f95, f110, f111): phóng to, tăng độ sáng bằng công cụ của CVAT (Image settings). Mặt nhỏ vẫn gán đủ điểm.
- **Mặt rất nhỏ hoặc mờ đến mức không thấy mắt-miệng**: đặt vị trí ước lượng theo tương quan mặt, Q cho điểm không thấy; ghi lại trong nhật ký để QC.
- **Nhòe chuyển động (motion blur)** (pose f100): đặt tại tâm khớp ước lượng, Q nếu không phân biệt được khớp.

### G. Pose: trái/phải khi thân người xoay
Với ảnh nằm ngang (fisheye) hoặc nhìn nghiêng, xác định trái/phải theo **người**, không theo ảnh:
1. Xác định hướng **mặt** (nhìn về camera / quay lưng / nghiêng).
2. Không dùng dây an toàn để đoán bên: xe có vô-lăng bên trái lẫn bên phải trong bộ ảnh nên hướng dây không cố định. Dùng vị trí tai/mắt, vai và hướng nhìn.
3. Chưa chắc: đối chiếu hai khuỷu/cổ tay với hướng cánh tay đi vào vô-lăng. Hai đường chân chéo nhau hoặc tai/mắt trái ở bên phải mà vai lại ngược: đổi lại.
4. Vẫn không chắc: ghi vào nhật ký để hỏi, không chọn bừa.

Các frame pose có nguy cơ nhầm trái/phải cao: f103, f104, f106, f110, f112 (nằm ngang/ngả), f92, f97, f116, f118 (cúi, nghiêng sát camera).

Lưu ý riêng cho pose:
- Hông bị dây an toàn, tay, báo, laptop, túi che: Q, đặt theo xương chậu ước lượng (đối xứng qua đường giữa).
- Cổ tay khi tay cầm vật (bút, điện thoại, túi): đặt ở khớp cổ tay, không ở vật.
- Mặt bị che hẳn (f118, gục mặt vào tay): mũi, hai mắt, hai tai vẫn đặt ở vị trí đầu ước lượng, Q.
- Nhiều khớp cùng lúc bị che nặng (f94 báo trải trên đùi): Q cho cả nhóm hông-gối, không bỏ trống.

## 6. Nháp có sẵn trong job

Các frame **91, 92, 97, 98, 103, 104, 109, 110, 115, 116** của job 1975 và 1623 đã có skeleton nhập từ file (`source=file`). Với mặt, 50 điểm của mỗi ảnh dồn thành cụm nhỏ quanh vùng mặt, không bám mày/mắt/môi. Với pose, nhiều điểm lệch khỏi khớp. Coi đây là **nháp thô**, không phải nhãn đúng: sửa từng điểm hoặc xóa vẽ lại (cần BTC xác nhận, mục 8 câu 3).

## 7. Quy trình + checklist QC cho leader

Mỗi người (kể cả leader):
1. Vào đúng **Job** (không làm trong trang Task), mở frame đầu job.
2. Mỗi ảnh: phóng to, đặt đủ 7 skeleton mặt (hoặc 1 skeleton người), kiểm số điểm và `trai/phai`.
3. Xong 30 frame mới đổi state/stage theo hướng dẫn BTC.

Leader kiểm trước khi chốt (mẫu 5 ảnh mỗi người, thêm ảnh khó):
- [ ] Mỗi ảnh đúng 7 skeleton mặt (hoặc 1 skeleton người), không trùng label.
- [ ] `longmaytrai` luôn ở bên trái ảnh so với `longmayphai`; không có cặp bị đổi bên.
- [ ] Hai khóe của cùng một mắt nằm đúng chỗ mí trên gặp mí dưới.
- [ ] Vòng môi trong nằm trọn trong vòng môi ngoài.
- [ ] Không còn cụm điểm giống nháp `source=file`.
- [ ] Điểm Q/O có lý do rõ: Q = bị che (kính, tóc, vô-lăng), O = ngoài biên ảnh.
- [ ] Pose: tay/chân không bắt chéo bất thường (dấu hiệu đổi trái/phải).
- [ ] Mỗi người chỉ sửa **job được gán** cho mình.

Xem nhanh nhãn (chỉ đọc CVAT):
```powershell
cd D:\06-Learning\AIA-VINGROUP\learning\cvat
python scripts/render_skeleton_overlay.py --job 1975 --profile edufun --frames 91 103 --scale 2
python scripts/render_skeleton_overlay.py --job 1975 --profile edufun --template
```

## 8. Cần BTC xác nhận (chưa biết)

1. `trai/phai` của mặt tính theo **trái ảnh** (như khung mẫu) hay theo **người**?
2. Có guideline chính thức không? Cách dùng cờ Q (`occluded`) và O (`outside`) có khác mục 5 không?
3. 10 frame đã có skeleton `source=file` là nháp để sửa hay mẫu mốc/gold? Có được xóa không?
4. Có được dùng **nháp AI** (pre-label) làm điểm xuất phát rồi tự sửa tay không?
5. Chấm điểm theo chỉ số nào (số điểm đúng, độ lệch so với gold, IAA)? Ngưỡng sai số bao nhiêu pixel?
6. Hạn nộp, và nộp bằng cách đổi state job hay export?
7. Điểm bị che mà không thể ước lượng được thì gán Q hay O? (mục 5 hiện mặc định: vẫn đặt ước lượng + Q).
8. Frame không có tài xế rõ (người bị cắt, mặt bị che hẳn như f64) có được bỏ trống không, hay bắt buộc đủ 7 skeleton (đặt ước lượng + Q/O)?
9. Mặt nhỏ trong ảnh IR tối có ngưỡng tối thiểu (px) để được gán không?
10. Pose trong ảnh nằm ngang: trái/phải theo người (như mục 5A.G) có đúng ý BTC không?
