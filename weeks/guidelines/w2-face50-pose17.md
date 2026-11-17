# Guideline nội bộ — Week 2: Face 50 điểm + Pose 17 điểm (nhóm G06)

> **Bản nội bộ G06, cập nhật 17/11/2026 theo guideline chính thức của BTC V1** (`HumanPose17_Annotation_Guideline_V1.docx`, `Face_Landmark50_Annotation_Guideline_V1.docx`). **Có mâu thuẫn thì bản BTC thắng.** Phần thêm của nhóm (ví dụ theo frame, ngưỡng tool, chính sách v0 ở mục 5) chỉ lấp chỗ BTC chưa nói, gắn nhãn "nhóm" để dễ phân biệt. Mục 8 liệt kê điều còn cần mentor chốt.

## 1. Phạm vi

| | Face | Pose |
|---|---|---|
| Task | 473 `W2-FACE-G6-T1` (150 frame, 5 job × 30) | 402 `week2-human-pose/G06` |
| Job của leader | 1975 (frame 90–119) | 1623 (frame 90–119) |
| Ảnh | 640×480, người lái xe trong cabin (màu) | 1280×1024, trong cabin, có ảnh hồng ngoại xám/ban đêm |
| Hình | 7 skeleton / ảnh, 50 điểm | 1 skeleton `person_vf17` / ảnh, 17 điểm |
| Chế độ vẽ | **Shape** (không Track) | **Shape** |

- Số frame CVAT = số trong tên file − 1 (frame 90 = `G06_091.jpg`).
- Mỗi ảnh chỉ gán **người lái**. Người ngồi sau, ảnh phản chiếu, hình in: không gán. **Không có người lái / không có mặt thì bỏ qua frame, không vẽ** (BTC).
- Mỗi ảnh có đủ **7 skeleton mặt** (mỗi label đúng 1 cái) hoặc **1 skeleton người đủ 17 điểm**, mọi điểm có trạng thái. Không thiếu, không thừa. Không tạo label/attribute mới, không đổi tên sublabel.
- Mỗi nhóm 150 ảnh (50 có pre-label, 100 ảnh gốc): **cả 150 đều phải kiểm tra**. Pre-label đúng thì giữ vị trí nhưng vẫn phải đặt trạng thái cho mọi điểm.
- BTC ghi ảnh pose 960×540, face 1280×720; ảnh thật của job mình khác (bảng trên). Không ảnh hưởng cách gán, chỉ ghi để biết (mục 8).

## 2. Face: 7 skeleton, 50 điểm

Mẫu: ![mẫu face](images/face50_template.png)

Tên điểm trên CVAT chỉ là số `0…49`. Số điểm là thứ tự cố định, **không được đổi**.

| Label | Điểm | Số điểm | Cách đặt (theo khung mẫu nhìn thẳng) |
|---|---|---:|---|
| `longmaytrai` | 0–4 | 5 | Lông mày bên **trái ảnh**: từ đuôi ngoài (0) dọc **bờ trên** lông mày tới đầu trong sát sống mũi (4) |
| `longmayphai` | 5–9 | 5 | Lông mày bên **phải ảnh**: từ đầu trong (5) qua đỉnh (7) tới đầu ngoài (9) |
| `songmui` | 10–13 | 4 | 4 điểm chia ba đoạn gần bằng nhau. 10: đỉnh sống mũi, điểm lõm giữa hai mắt, ngang khóe mắt trong. 13: **chân sống mũi**, phía trên lỗ mũi, **chưa chạm chóp mũi** (BTC) |
| `mattrai` | 14–21 | 8 | Mắt bên trái ảnh. 14 khóe ngoài, 15–17 mép mí trên (trái → phải), 18 khóe trong, 19–21 mép mí dưới (phải → trái) |
| `matphai` | 22–29 | 8 | Mắt bên phải ảnh. 22 khóe trong, 23–25 mí trên, 26 khóe ngoài, 27–29 mí dưới (phải → trái) |
| `moingoai` | 30–41 | 12 | Mép **ngoài** môi: 30 khóe miệng trái ảnh, 31–35 viền môi trên (33 giữa), 36 khóe phải, 37–41 viền môi dưới (39 giữa) |
| `moitrong` | 42–49 | 8 | Mép **trong** môi (khe miệng): 42 khóe trái, 43–45 trên (44 giữa), 46 khóe phải, 47–49 dưới (48 giữa) |

Quy tắc đặt điểm:
1. Phóng to ≥ 300 % khi đặt mắt và môi. Điểm đặt **lên mép/đường viền thật**, không đặt vào vùng da bên cạnh.
2. Điểm mí mắt nằm trên **bờ mi** (ranh giới da mi và nhãn cầu), không đặt lên lông mi hoặc vào lòng trắng. 3 điểm mí trên và 3 điểm mí dưới tại 1/4, 1/2, 3/4 chiều rộng mắt giữa hai khóe.
3. Hai khóe mắt dùng chung cho mí trên và mí dưới: 14/18 và 22/26 nằm đúng chỗ mí trên gặp mí dưới.
4. Môi: vòng ngoài và vòng trong là **hai vòng khác nhau**. Miệng ngậm vẫn đặt vòng trong ở đường khép môi. Vòng trong không chạm hoặc vượt vòng ngoài.
5. Lông mày: 5 điểm trên **mép lông ở bờ trên** (ranh giới lông mày và da trán), chia 4 đoạn bằng nhau theo chiều dài lông mày; không đặt giữa đám lông hoặc lên da trán (BTC). Trái: 0 đuôi ngoài → 4 đầu trong; phải: 5 đầu trong → 9 đuôi ngoài. Mày thưa hoặc bị tóc che: ước lượng theo xương mày, đánh `occluded`.
6. Sống mũi: 4 điểm gần thẳng hàng theo trục mũi, không lệch theo bóng đổ.
7. Môi ngoài: 31–35 nằm ở tỉ lệ 0,18 · 0,36 · 0,50 · 0,66 · 0,84 chiều rộng môi (từ khóe trái sang khóe phải); 37–41 chia đều ngược lại. Môi trong: 43–45 và 47–49 tại 1/4, 1/2, 3/4 chiều rộng miệng; làm 44 và 48 trước. Vòng kín chạy **cùng chiều kim đồng hồ, bắt đầu từ điểm trái nhất**; Point ID chạy liên tục 0–49 qua 7 skeleton.
8. Sai số cho phép: **±5 px** điểm visible, **±20 px** điểm occluded.

### 2.1. Ngưỡng khi cả một bộ phận bị che (BTC, bảng 3.1)

| Skeleton | Còn thấy từ | Xử lý |
|---|---|---|
| `mattrai`, `matphai`, `moitrong` | ≥ 4/8 điểm | Đặt đủ contour; điểm không thấy: Occluded |
| `longmaytrai`, `longmayphai` | ≥ 3/5 điểm | Đặt đủ; điểm không thấy: Occluded |
| `moingoai` | ≥ 6/12 điểm | Đặt đủ; điểm không thấy: Occluded |
| `songmui` | ≥ 2/4 điểm | Đặt đủ; điểm không thấy: Occluded |

Dưới ngưỡng: vẫn **đặt đủ + Occluded nếu có đủ bằng chứng thị giác** (hình dáng mặt, bên còn lại đối xứng, gọng kính...). Chỉ khi không còn căn cứ nào mới gán **Outside cả skeleton**, kèm issue `ATTRIBUTE_CHECK` (mục 5B). Chính sách nhóm: mặt luôn ưu tiên Visible/Occluded, Outside là phương án cuối.

## 3. Pose: 1 skeleton, 17 điểm (thứ tự COCO)

Mẫu: ![mẫu pose](images/pose17_template.png)

| # | Điểm | # | Điểm | # | Điểm |
|---:|---|---:|---|---:|---|
| 1 | mũi | 7 | vai L | 13 | hông L |
| 2 | mắt R | 8 | khuỷu R | 14 | gối R |
| 3 | mắt L | 9 | khuỷu L | 15 | gối L |
| 4 | tai R | 10 | cổ tay R | 16 | cổ chân R |
| 5 | tai L | 11 | cổ tay L | 17 | cổ chân L |
| 6 | vai R | 12 | hông R | | |

**R/L theo ẢNH, không theo người (BTC):** số **chẵn (2–16) = R luôn nằm PHẢI ảnh**, số **lẻ (3–17) = L luôn nằm TRÁI ảnh**, bất kể người quay mặt, quay lưng, vặn mình hay ảnh xoay 90°. Không suy luận theo tay/chân giải phẫu. Người quay mặt về camera thì R trùng với tay trái giải phẫu của họ, nên khung mẫu vẫn khớp.

Định nghĩa điểm (BTC) và sai số **±5 px** khi visible, **±20 px** khi occluded:
- **Mũi (1)**: chóp mũi; mặt nghiêng vẫn là chóp mũi, không dời về giữa mặt. **Mắt (2, 3)**: tâm đồng tử (mắt nhắm: tâm khe mí). **Tai (4, 5)**: ống tai, không phải chóp/dái tai.
- **Vai (6, 7)**: tâm khớp vai, điểm xoay của cánh tay. **Khuỷu (8, 9)**: tâm khớp khuỷu. **Cổ tay (10, 11)**: nếp gấp cổ tay; tay trên vô-lăng vẫn không dời lên vành vô-lăng.
- **Hông (12, 13)**: tâm khớp háng, không phải mép ngoài hông hay cạp quần. **Gối (14, 15)**: giữa xương bánh chè. **Cổ chân (16, 17)**: ngang mắt cá.
- Hai khớp **Visible không được trùng tọa độ**: tách đúng vị trí, hoặc đánh lại trạng thái cho điểm không thật sự thấy.
- Kiểm tra chéo: chuỗi vai–khuỷu–cổ tay và hông–gối–cổ chân mỗi phía phải liên tục, không bắt chéo sang bên kia.
- Ngồi trong xe: nửa dưới thường bị vô-lăng, ghế, cửa che. Hông, gối, cổ chân không thấy: xem mục 5.
- Ảnh hồng ngoại xám, thiếu sáng, nhòe: nội suy hợp lý, bàn với thành viên khác (BTC).

## 4. Trái/phải: theo ảnh (BTC), cả pose và face

| | Quy ước (BTC) |
|---|---|
| Pose | R (số chẵn 2–16) = **phải ảnh**, L (số lẻ 3–17) = **trái ảnh**, kể cả khi quay lưng hoặc ảnh xoay 90° |
| Face | `longmaytrai`, `mattrai` ở **phía trái của khuôn mặt trên ảnh**; `longmayphai`, `matphai` ở phía phải. Tham chiếu là khuôn mặt nhìn thấy, không cần quan tâm mirror effect |

Hai quy ước giờ **cùng gốc là ảnh**; đừng đổi theo giải phẫu người. Khi mặt/thân quay đi, phần xa vẫn giữ nhãn của bên đó theo vị trí trên ảnh, **không đổi chỗ**.

Ca người nằm ngang hoặc ảnh xoay 90° mà hai bên cùng tọa độ x (không phân định được "phải ảnh/trái ảnh"): không đoán; tạo issue `UNCERTAIN_CLASS` (mục 5B) và theo kết luận bỏ phiếu của nhóm/mentor. Riêng face, câu chữ BTC chưa nói rõ khi mặt xoay 90° (mục 8, câu 1).

## 5. Cờ trạng thái điểm (phím tắt CVAT)

| Tình huống | Cờ | Phím |
|---|---|---|
| Thấy rõ | bình thường | không bấm |
| **Bị che nhưng còn suy ra được vị trí** (kính râm, tóc, tay, vô-lăng, ghế, tự che do nghiêng người): khớp nằm trong khung, suy ra từ khớp kề, tư thế, tỉ lệ cơ thể | `occluded` (v1) | **Q** |
| **Ngoài khung hình, hoặc che đến mức không còn căn cứ suy ra vị trí** | `outside` (v0) | **O** |

Điểm `outside` **không dùng đến tọa độ** (BTC). Điểm visible/occluded phải đúng vị trí thật/ước lượng hợp lý.

Cách dùng: chọn đúng điểm trong skeleton (không phải cả skeleton) rồi bấm Q hoặc O.

**Q hay v0 (O)? Chính sách nhóm, dựa trên BTC "không suy ra được vị trí thì Outside"**. Tự hỏi: "Nhìn đường nét xung quanh, mình chỉ được vị trí khớp trong ±20 px không?"
- **Đầu/mặt (mũi, mắt, tai, và toàn bộ 50 điểm face): ưu tiên Visible hoặc Occluded, gần như không bao giờ v0.** Đầu luôn suy ra được từ hướng mặt, bên còn lại, tỉ lệ khuôn mặt. Mặt bị che (kính râm, tay, tóc, gục mặt, ngửa/cúi): đặt ước lượng + **Q**. Face chỉ O khi ra ngoài khung hoặc dưới ngưỡng mục 2.1 mà không còn căn cứ nào.
- **Tai (4, 5)**: tóc/đầu quay che kín mà ước lượng được thì Q; chỉ O khi thật sự không còn dấu hiệu (BTC). Trường hợp này nên có issue `ATTRIBUTE_CHECK`.
- **Vai, hông (6, 7, 12, 13)**: suy ra được từ thân, đối xứng qua đường giữa nên mặc định Q khi bị che, không v0.
- **Tay và chân (khuỷu 8-9, cổ tay 10-11, gối 14-15, cổ chân 16-17) bị che hẳn không suy ra được** (báo/laptop/ghế/vô-lăng che kín, không còn đoạn kề nào thấy): **O (v0)**, không đặt bừa. Còn thấy đoạn kề hoặc bóng dáng: Q. Đây là chỗ nháp AI hay đoán sai nhất.
- Tool nháp tự áp: tay/chân conf model < 0.3 -> v0; 0.3–0.5 -> Q; mặt/vai/hông không bao giờ v0 vì conf thấp (chỉ O khi ra ngoài/sát biên ảnh). Vẫn phải duyệt tay: điểm tool đánh visible mà thực tế che hẳn (vd khuỷu dưới tờ báo) sửa thành O.

- Điểm bị che vẫn **đặt tại vị trí ước lượng** theo khớp/đường nét lân cận, rồi bấm **Q**.
- Điểm ngoài biên: bấm **O**, **không** kéo về mép ảnh.
- **Không dùng `hidden` (phím H)** thay Q: không lưu lên server.
- Kính râm tối: mắt đặt theo gọng/tròng, bấm Q; kính trong thấy mắt thì bình thường.
- Mặt nghiêng mạnh: mày, mắt, má phía xa bị che thì Q.
- Miệng bị che (tay, khẩu trang): môi bấm Q, đặt theo dáng môi ước lượng.
- Pose ngồi trong xe: hông bị ghế/vô-lăng che thì Q; gối, cổ chân che nhưng ước lượng được thì Q; ra ngoài khung hoặc che hẳn không ước lượng được thì O (v0).
- Không điền bừa với tay/chân: điểm không thể ước lượng ngay cả gần đúng thì **O (v0)**, không đặt điểm đoán mò. Ghi issue (mục 5B). Với mặt không áp dụng: luôn đặt ước lượng + Q.
- **Mắt nhắm** mà vẫn xác định khe mí: **Visible**, không phải Q. Chỉ Q khi mắt bị vật khác che (BTC).
- **Đeo kính** mà vẫn xác định được vị trí điểm: Visible (BTC).

## 5A. Edge case và cách xử lý (khảo sát toàn bộ 150 ảnh mặt task 473 và 30 ảnh pose job 1623)

Ảnh là camera giám sát tài xế (DMS) trong cabin. Có **hai kiểu ảnh**: ảnh màu góc rộng ban ngày, và ảnh **hồng ngoại xám (IR) ban đêm, méo fisheye**. Danh sách frame theo từng nhóm: `week02/task473-face/EDGE_CASES.md`. Bảng từng frame của job mình: `job1975-face50/EDGE_CASES.md`, `job1623-pose17/EDGE_CASES.md`.

### A. Ai là người được gán
- Chỉ gán **tài xế** (người ngồi ghế lái, tay ở vô-lăng hoặc ngồi đúng vị trí ghế lái). Hành khách phía sau hoặc bên cạnh (nhiều frame có, ví dụ f0, f21, f60, f99, f107, f113, f117) **không gán**, kể cả khi họ lớn hoặc rõ hơn.
- Ảnh IR chỉ có một người: người đó là tài xế.
- Không có người lái trong khung: **bỏ qua frame, không vẽ** (BTC), ghi frame vào nhật ký `review/`. Chỉ thấy lưng/đầu bị cắt gần hết nhưng vẫn rõ là người lái: vẫn vẽ, phần không thấy Q hoặc O theo mục 5, và tạo issue `LOW_VISIBILITY`.

### B. Mặt xoay, nghiêng, ngửa (nhóm gây sai nhiều nhất)
- **Xoay ~90° (người nằm ngang trong ảnh fisheye IR)**, ví dụ f10, f20, f34, f44, f58, f67, f68, f92, f106, f116, f124, f142: gán `trai/phai` **theo vị trí trên ảnh** như quy tắc BTC (mục 4): phần nằm phía trái ảnh là `trai`. Văn bản BTC nói "trái/phải theo cách nhìn trên ảnh", chưa nêu riêng mặt xoay 90°: gặp ca này tạo issue `UNCERTAIN_CLASS` và theo kết luận mentor (mục 8, câu 1). Bản cũ của nhóm ("đưa mặt thẳng đứng trong đầu rồi mới gán") **bị hủy** vì ngược chữ BTC.
- Mặt **quay nghiêng (profile)**: giữ nhãn theo bên đó (bên nằm phía trái khi nhìn mặt thẳng). Mày, mắt, má phía xa bị sống mũi/má che: Q. Vòng môi vẫn đủ 20 điểm, phần khuất Q.
- **Ngửa mặt lên** (f96, f97, f100, f105, f112, f118): mắt nhìn ngược chiều bình thường, mí trên vẫn là mí phía đỉnh đầu. Mũi che môi trên: môi ngoài phía trên Q.
- **Cúi mặt xuống** (f103, f111, f114, f115, f35, f46): mí trên che phần lớn mắt, mí dưới sát nhau. Đặt điểm theo mép mí thật; nếu mi mắt khép gần như một đường, các điểm mí trên và mí dưới nằm sát nhau (cách nhau vài pixel), không kéo ra để trông giống mẫu.

### C. Che khuất (đánh Q, đặt ở vị trí ước lượng)
| Vật che | Frame ví dụ | Xử lý |
|---|---|---|
| Kính trong có phản sáng/lóa | f18, f19, f20 | Mắt vẫn thấy mờ: đặt theo mí, không Q. Nếu lóa che hết mắt: Q |
| Kính râm / tròng tối | f6, f45, f106, f116, f144, f147 | 16 điểm hai mắt Q, đặt theo hình dáng tròng kính/gọng, tròng ngay trên mí ước lượng. BTC: kính râm đen không xác định nổi đủ điểm thì Outside; nhóm: vẫn đặt ước lượng + Q khi còn ≥ ngưỡng mục 2.1, dưới ngưỡng thì Outside cả skeleton mắt + issue |
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
- Pose: ảnh IR nhìn thẳng thường cắt ở đùi/gối, ảnh màu nhìn nghiêng thường cắt bên phải. Cổ chân (16, 17) và nhiều khi gối (14, 15) nằm ngoài ảnh: **O**. Che bởi vô-lăng, ghế, bàn đạp nhưng còn trong ảnh và ước lượng được: **Q**; che hẳn không ước lượng được: **O (v0)**.

### E. Điểm chuẩn mắt, miệng
- **Mắt nhắm/nheo** (f17, f39, f40, f99): vẫn đặt đủ 8 điểm, vòng kín; hai mí nằm sát hoặc trùng nhau theo khe mí (các cặp 15–21, 16–20, 17–19 có thể trùng). Khóe ngoài và khóe trong đặt đúng khóe. Không vẽ mắt mở. Xác định được khe mí: **Visible**; chỉ Occluded khi mắt bị vật khác che (BTC).
- **Miệng mở, ngáp, nói** (f99, f133, f119, f120): vòng môi ngoài bám mép đỏ ngoài; vòng môi trong bám mép trong của khe miệng (nơi lộ răng/lưỡi), thành một hình mở. Vòng trong vẫn nằm trong vòng ngoài.
- **Miệng ngậm**: vòng trong thành một đường hẹp trên đường khép môi.
- **Cười lớn, mắt híp** (f119, f120, f147): mí híp, điểm 16/24 và 20/28 gần nhau; khóe mắt đặt đúng khóe.

### F. Điều kiện ảnh
- **Ảnh IR tối, mặt nhỏ** (f5, f13, f14, f24, f37, f38, f61, f84–f86, f94, f95, f110, f111): phóng to, tăng độ sáng bằng công cụ của CVAT (Image settings). Mặt nhỏ vẫn gán đủ điểm.
- **Mặt rất nhỏ hoặc mờ đến mức không thấy mắt-miệng**: đặt vị trí ước lượng theo tương quan mặt, Q cho điểm không thấy; ghi lại trong nhật ký để QC.
- **Nhòe chuyển động (motion blur)** (pose f100): đặt tại tâm khớp ước lượng, Q nếu không phân biệt được khớp.

### G. Pose: trái/phải khi thân người xoay (theo ảnh, BTC)
Với ảnh nằm ngang (fisheye), quay lưng hoặc nhìn nghiêng, **không dùng giải phẫu người, không đoán theo dây an toàn hay hướng nhìn**:
1. Điểm **chẵn (R)** là điểm nằm **bên phải ảnh** của cặp; điểm **lẻ (L)** nằm bên trái ảnh. Làm cho mọi cặp: mắt, tai, vai, khuỷu, cổ tay, hông, gối, cổ chân.
2. Kiểm tra chéo: chuỗi vai–khuỷu–cổ tay và hông–gối–cổ chân mỗi phía liên tục; hai đường chân/tay không bắt chéo sang bên kia. Bắt chéo là dấu hiệu gán nhầm cặp.
3. Người nằm ngang/xoay 90° mà hai bên cùng tọa độ x, không phân biệt được "phải ảnh/trái ảnh": tạo issue `UNCERTAIN_CLASS`, theo phiếu bầu của nhóm rồi mentor, không chọn bừa.
4. Nháp tool đã tự đổi cả chuỗi theo luật này và gắn cờ `UNCERTAIN_CLASS_LR` ở frame không chắc (hiện: f96, 103, 105, 106, 110, 112 của job 1623).

Các frame pose có nguy cơ nhầm trái/phải cao: f103, f104, f106, f110, f112 (nằm ngang/ngả), f92, f97, f116, f118 (cúi, nghiêng sát camera).

Lưu ý riêng cho pose:
- Hông bị dây an toàn, tay, báo, laptop, túi che: Q nếu còn ước lượng được theo xương chậu (đối xứng qua đường giữa, thân còn thấy); không ước lượng được: O (v0).
- Cổ tay khi tay cầm vật (bút, điện thoại, túi): đặt ở khớp cổ tay, không ở vật.
- Mặt bị che hẳn (f118, gục mặt vào tay): mũi, hai mắt, hai tai vẫn đặt ở vị trí đầu ước lượng, Q.
- Nhiều khớp cùng lúc bị che nặng (f94 báo trải trên đùi): hông còn suy ra được từ thân thì Q/bình thường; **gối và cổ chân (14-17) không đoán nổi thì O (v0)**, không đặt bừa trên tờ báo.

## 5B. Case không rõ: quy trình issue (BTC)

Ưu tiên review thay vì "đoán cho xong". Nhóm **bỏ phiếu đa số** (inter-annotator agreement) trước, rồi gửi issue theo mẫu tới mentor. Không tự đặt luật mới.

| Issue type | Ví dụ |
|---|---|
| `UNCERTAIN_CLASS` | không chắc điểm/nhóm thuộc R hay L (pose), `mattrai` hay `matphai` (face) khi người vặn mình, quay lưng, mặt nghiêng mạnh |
| `UNCERTAIN_BOUNDARY` | không rõ vị trí khớp/điểm do vô-lăng, ghế, quần áo, gọng kính, tay che |
| `UNCERTAIN_SCOPE` | không xác định được ai là người lái, có skeleton/mặt thứ hai |
| `ATTRIBUTE_CHECK` | không chắc Visible / Occluded / Outside (kể cả mọi điểm gán O vì không suy ra được) |
| `LOW_VISIBILITY` | khó quan sát do thiếu sáng, ngược sáng, nhòe, lóa kính, mặt quá nhỏ |

## 6. Nháp có sẵn trong job

Các frame **91, 92, 97, 98, 103, 104, 109, 110, 115, 116** của job 1975 và 1623 đã có skeleton nhập từ file (`source=file`). Với mặt, 50 điểm của mỗi ảnh dồn thành cụm nhỏ quanh vùng mặt, không bám mày/mắt/môi. Với pose, nhiều điểm lệch khỏi khớp. Coi đây là **nháp thô**, không phải nhãn đúng: sửa từng điểm hoặc xóa vẽ lại (cần BTC xác nhận, mục 8 câu 3).

## 7. Quy trình + checklist QC cho leader

Mỗi người (kể cả leader):
1. Vào đúng **Job** (không làm trong trang Task), mở frame đầu job.
2. Mỗi ảnh: phóng to, đặt đủ 7 skeleton mặt (hoặc 1 skeleton người), kiểm số điểm và `trai/phai`.
3. Xong 30 frame mới đổi state/stage theo hướng dẫn BTC.

Leader kiểm trước khi chốt (mẫu 5 ảnh mỗi người, thêm ảnh khó):
- [ ] Mỗi ảnh đúng 7 skeleton mặt (hoặc 1 skeleton người), không trùng label.
- [ ] Mỗi điểm đều có trạng thái rõ (không bỏ trống); điểm `outside` không dùng tọa độ.
- [ ] Tọa độ trong sai số: ±5 px visible, ±20 px occluded. Kiểm hai lần toàn bộ trước khi save.
- [ ] Case không chắc đã tạo issue/comment và raise lên mentor.
- [ ] Pose: số chẵn ở phải ảnh, số lẻ ở trái ảnh ở mọi cặp; không có hai khớp visible trùng tọa độ.
- [ ] Pose: gối/cổ chân/khuỷu/cổ tay che hẳn không suy ra được thì O; mặt luôn đã đặt ước lượng (V hoặc Q).
- [ ] `longmaytrai` luôn ở bên trái ảnh so với `longmayphai`; không có cặp bị đổi bên.
- [ ] Hai khóe của cùng một mắt nằm đúng chỗ mí trên gặp mí dưới.
- [ ] Vòng môi trong nằm trọn trong vòng môi ngoài.
- [ ] Không còn cụm điểm giống nháp `source=file`.
- [ ] Điểm Q/O có lý do rõ: Q = bị che nhưng suy ra được, O = ngoài khung hoặc không còn căn cứ suy ra.
- [ ] Pose: tay/chân không bắt chéo bất thường (dấu hiệu đổi trái/phải).
- [ ] Mỗi người chỉ sửa **job được gán** cho mình.

Xem nhanh nhãn (chỉ đọc CVAT):
```powershell
cd D:\06-Learning\AIA-VINGROUP\learning\cvat
python scripts/render_skeleton_overlay.py --job 1975 --profile edufun --frames 91 103 --scale 2
python scripts/render_skeleton_overlay.py --job 1975 --profile edufun --template
```

## 8. Cần BTC xác nhận (chưa biết)

**Đã được BTC V1 trả lời (17/11/2026):** có guideline chính thức (bản này bám theo nó); face và pose đều theo **trái/phải trên ảnh**; điểm không suy ra được vị trí thì **Outside**; không có người lái/mặt thì **bỏ qua frame**; sai số ±5 px (visible), ±20 px (occluded); nháp AI/pre-label được dùng làm điểm xuất phát nhưng phải kiểm và đặt trạng thái cho mọi điểm; có quy trình issue + bỏ phiếu đa số.

**Còn cần mentor chốt:**
1. Face: mặt/thân xoay ~90° trong ảnh fisheye, "trái ảnh" áp thế nào? (BTC chỉ nói theo cách nhìn trên ảnh; ở pose BTC nói rõ kể cả ảnh xoay 90°, ở face thì không.)
2. Pose: người nằm ngang/xoay mà hai bên cùng x, chọn R/L theo tiêu chí nào? (f96, 103, 105, 106, 110, 112.)
3. 10 frame đã có skeleton `source=file` (f91, 92, 97, 98, 103, 104, 109, 110, 115, 116) là nháp để sửa hay mẫu mốc? Có được xóa vẽ lại không? (BTC nói "pre-label": sửa hay vẽ mới đều được, nhưng chưa nói riêng cho `source=file`.)
4. Chấm điểm: Outside có bị tính lỗi khi gold có tọa độ không? Tính trên điểm visible/occluded hay mọi điểm?
5. Hạn nộp, và nộp bằng cách đổi state job hay export?
6. Ảnh thật của job lệch số liệu trong guideline BTC (pose 1280×1024 so với 960×540; face 640×480 so với 1280×720): có phải ảnh khác bộ nên ngưỡng pixel có khác không?
7. Ngưỡng bằng chứng "đủ bằng chứng thị giác" (mục 2.1) dưới ngưỡng: BTC chưa định lượng, cần ví dụ.
8. Mặt nhỏ trong ảnh IR tối có ngưỡng tối thiểu (px) để được gán không?
9. Face điểm 13 "chân sống mũi, chưa chạm chóp mũi": cách đo chính xác? Tool tạm đặt tại 85% đoạn từ điểm lõm giữa hai mắt tới chóp mũi; cần ảnh mẫu của BTC để chỉnh.
10. Face lông mày "mép lông ở bờ trên": nháp FAN đặt giữa sợi lông, lệch khoảng nửa bề dày lông mày. Cách dịch có đúng ý BTC không, hay cứ duyệt tay?
