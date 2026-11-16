# Quy ước vẽ — job 285 (dashcam 1280x720, frame 60-79)

Mục đích: chốt **vẽ đúng là thế nào** trước, rồi mới tự động hóa. Mỗi quy tắc sau này thành một hàm kiểm (validator) và một luật sinh nháp.

Ký hiệu nguồn của từng quy tắc:
- **[BẠN]** bạn đã nói rõ.
- **[DỮ LIỆU]** rút từ shape đang có trên CVAT (chỉ tham khảo, vì shape của tool và của bạn đều `source: manual`).
- **[ĐỀ XUẤT]** tôi đề xuất, **cần bạn duyệt** trước khi coi là chuẩn.

## 0. Nguyên tắc chung
1. **[BẠN] Polygon nguyên vùng.** Không khoét lỗ. Vật phía trên đè lên vật phía dưới bằng `z_order`. (Bản khoét lỗ nếu cần chỉ dẫn xuất khi xuất, không vẽ.)
2. **[BẠN] Vẽ đúng hình dạng thực của vật**, không vẽ thừa điểm. Ít đỉnh nhất mà vẫn ôm đúng vật.
3. **[ĐỀ XUẤT]** Chỉ vẽ phần **nhìn thấy**. Phần bị che do vật khác đè lên thì không vẽ bù, mà bật cờ che khuất (mục 4).
4. **[ĐỀ XUẤT]** Không có vật trong ảnh thì không có shape. Vật nằm hoàn toàn ngoài khung ảnh thì không vẽ.
5. **[DỮ LIỆU]** SPEC job 285 ghi: vật thể (car, truck, bus, motorcycle, pedestrian, rider...) dùng **rectangle**, không đổi sang polygon. Label nền và lane dùng **polygon**.
6. Đã làm tay theo SPEC: không xóa/sửa shape của người; tool chỉ **thêm**.

## 1. Kiểu hình theo nhóm label 

| Nhóm | Label | Kiểu hình | Nguồn |
|---|---|---|---|
| Vật thể có thuộc tính | pedestrian, rider, car, truck, bus, train, motorcycle, bicycle, traffic light, traffic sign | **rectangle** | [DỮ LIỆU] SPEC, 178 car / 38 traffic light / 23 traffic sign đều rectangle |
| Nền | road, sidewalk, building, wall, fence, vegetation, terrain, sky | **polygon** | [DỮ LIỆU] |
| Cột | pole | **polygon hẹp theo hình chữ nhật cột** | [BẠN] |
| Vạch | lane/single white, single yellow, double white, double yellow, single other, double other | **polygon rất hẹp, gần như đường thẳng** | [BẠN] |
| Vạch ngựa vằn | lane/crosswalk | **polygon 4–6 điểm** bao cả dải sọc | [DỮ LIỆU] bạn vẽ 4–6 điểm |
| Lề đường | lane/road curb | polygon hẹp theo mép lề | [ĐỀ XUẤT] |
| Vùng | area/direct, area/alternative | polygon trong road | [DỮ LIỆU] |

**Label trùng nghĩa** (job có cả hai tên): `person` và `pedestrian`, `traffic_light` và `traffic light`, `traffic_sign` và `traffic sign`.
- [ĐỀ XUẤT] Dùng bản **có khoảng trắng / pedestrian** (rectangle, có thuộc tính `occluded`/`truncated`). Không dùng bản gạch dưới / `person`.
- [DỮ LIỆU] Hiện có 1 `traffic_sign` polygon lẻ trên CVAT, nên xem lại.

## 2. Quy ước từng label

### Nền (polygon nguyên vùng)
| Label | Cách vẽ | Nguồn |
|---|---|---|
| **road** | Cả mặt đường lái được, **kể cả phần xe đang đỗ/chạy đè lên**. Cắt bỏ **capo/taplo** của xe mình. Mặt đường dưới xe vẫn thuộc road. Gồm cả vạch kẻ và vạch ngựa vằn trên đường. Biên ngoài chạy theo mép đường/lề. | [BẠN] nguyên vùng, [DỮ LIỆU] cắt capo |
| **sidewalk** | Vỉa hè (phần đi bộ). Cạnh giáp road là đường lề. Không gồm cột đèn, người, xe đỗ trên vỉa hè (đè bằng z_order). | [ĐỀ XUẤT] |
| **building** | Mặt tiền tòa nhà nhìn thấy, **biên thẳng theo mép nhà**. Mỗi tòa một polygon nếu biên tách rõ; liền khối thì gộp. | [ĐỀ XUẤT], [DỮ LIỆU] 25 polygon |
| **sky** | Vùng trời, biên chạy theo đường chân trời nhà/cây. Bầu trời bị dây điện cắt thì bỏ qua dây, vẫn một vùng. | [ĐỀ XUẤT] |
| **vegetation** | Tán cây, bụi cây. Biên **mượt, ít điểm**, không đuổi từng chiếc lá. Mỗi tán một polygon. | [ĐỀ XUẤT] |
| **terrain** | Cỏ, đất trống, dải phân cách mềm. | [ĐỀ XUẤT] |
| **wall** | Tường, hàng rào đặc (không phải mặt nhà). | [ĐỀ XUẤT] |
| **fence** | Hàng rào hở, lưới. Không nhầm tấm bạt hay biển công trình với fence. | [ĐỀ XUẤT], TASK ghi model hay nhầm |

### Cột và biển
| Label | Cách vẽ | Nguồn |
|---|---|---|
| **pole** | Polygon **hình chữ nhật hẹp** ôm thân cột: 4 điểm nếu thẳng, tối đa 6–8 điểm nếu gấp khúc/có tay đỡ. Từ chân cột (chạm đất/vỉa hè) đến đỉnh. Cột che một phần thì chỉ vẽ phần nhìn thấy. | [BẠN], [DỮ LIỆU] cột rộng khoảng 11–25 px, cao 100–200 px |
| **traffic light** | rectangle ôm **cụm đèn**, không ôm cột. | [ĐỀ XUẤT] |
| **traffic sign** | rectangle ôm **mặt biển**, không ôm cột. | [ĐỀ XUẤT] |

### Vạch (lane/*)
Quy tắc chung **[BẠN]**: polygon vẽ **hẹp gần như đường thẳng**, chỉ vẽ trong **vùng nhận ra được màu đó** (trắng hoặc vàng), **không làm nhiều**. Không có vạch rõ thì không vẽ.

| Label | Cách vẽ | Nguồn |
|---|---|---|
| **lane/single white** | Một vạch trắng liền hoặc đứt. Polygon 4 điểm (hình thang rất hẹp) cho mỗi **đoạn nhìn thấy**; vạch đứt: mỗi nét một polygon, hoặc nối cả hàng nét thành một polygon nếu bạn quy định (xem câu hỏi Q3). Rộng khoảng vài px ở xa, vài chục px ở gần (theo phối cảnh). | [BẠN] hẹp, [ĐỀ XUẤT] đoạn đứt |
| **lane/single yellow** | Như trên, màu vàng. | [BẠN] |
| **lane/double white** | Hai vạch trắng sát nhau, vẽ **một polygon ôm cả hai** (phần khe giữa nằm trong polygon). | [ĐỀ XUẤT] |
| **lane/double yellow** | Như double white, màu vàng. | [ĐỀ XUẤT] |
| **lane/single other / double other** | Vạch không phải trắng/vàng (đỏ, xanh...). Chỉ vẽ khi có thật. | [ĐỀ XUẤT] |
| **lane/crosswalk** | Polygon 4–6 điểm bao cả dải sọc ngựa vằn; sọc bị xe che vẫn ôm trọn dải (vì polygon nguyên vùng). Biên theo hướng ngang của dải. | [DỮ LIỆU] bạn vẽ 4–6 điểm ở frame 72, 73, 78, 79 |
| **lane/road curb** | Polygon hẹp theo mép lề, giữa road và sidewalk. | [ĐỀ XUẤT] |

### Vùng làn
| Label | Cách vẽ | Nguồn |
|---|---|---|
| **area/direct** | Phần road là **làn xe mình đang chạy**, từ đáy ảnh lên điểm tụ. Ở frame 71 bạn vẽ hình thang 5 điểm rộng từ mép trái đáy ảnh đến x≈915. **Vẽ cả phần dưới xe phía trước** (nguyên vùng). | [DỮ LIỆU] frame 71, [BẠN] nguyên vùng |
| **area/alternative** | Phần road **còn lại** ngoài direct (làn khác/làn có thể chuyển sang). Không chồng lên direct. | [DỮ LIỆU] |

### Vật thể (rectangle)
| Điểm | Quy ước | Nguồn |
|---|---|---|
| Khung | Hộp **ôm sát phần nhìn thấy** của vật. | [ĐỀ XUẤT] |
| Vật quá nhỏ (cạnh < ~12 px) | Cờ TINY: không vẽ nếu không nhận ra được loại; vẽ nếu bạn muốn đếm đủ xe xa. | [DỮ LIỆU] metric ghi hộp TINY cần mắt người |
| Xe đã có hộp tay | Không vẽ thêm hộp trùng (IoU cao). | [DỮ LIỆU] có bước dedupe |
| Phản chiếu capo/taplo | Không vẽ hộp cho phản chiếu. | [DỮ LIỆU] ghi chú SPEC |

## 3. z_order (thứ tự chồng)
[ĐỀ XUẤT] bảng chuẩn, từ **sau ra trước**; số lớn hơn nằm trên.

| z | Nhóm |
|---|---|
| -6 | road |
| -5 | area/alternative |
| -4 | area/direct |
| -3 | lane/*, crosswalk, curb |
| -2 | pole |
| 0 | vật thể (rectangle) |

Nền khác (sky, building, vegetation, sidewalk, terrain, wall, fence) nằm dưới road hoặc cạnh road, **không chồng nhau đáng kể**; sky xa nhất.

**[DỮ LIỆU] Cần chú ý:** z_order trên CVAT hiện lộn xộn (road có -13, -10, -3, -1, 0; area/direct có -4, -2, 0; building có -12 đến 0). Cần quy ước cứng một bảng, rồi tool kiểm.

## 4. Che khuất (occluded) và cắt mép (truncated)
- **[DỮ LIỆU]** 10 label vật thể (pedestrian, rider, car, truck, bus, train, motorcycle, bicycle, traffic light, traffic sign) **có** hai thuộc tính checkbox `occluded` và `truncated`. Label nền và lane **không có** thuộc tính, chỉ có cờ `occluded` của shape CVAT (thấy 1 crosswalk bật).
- **[ĐỀ XUẤT]** Vật bị vật khác che ≥ 30% diện tích (ngưỡng chỉnh được) thì bật `occluded`.
- **[ĐỀ XUẤT]** Vật bị cắt bởi mép khung ảnh thì bật `truncated`. Vật nằm hoàn toàn ngoài khung thì không có shape.
- **[ĐỀ XUẤT]** Label nền và lane: bật cờ `occluded` của shape khi bị vật thể che đáng kể, **không** thêm thuộc tính mới vì label không định nghĩa.

## 5. Cấm / lỗi thường gặp
- Không vẽ vạch bằng polygon bè rộng (nhiều chục px) như một mảng. Vạch phải hẹp (mục lane).
- Không khoét lỗ polygon.
- Không để polygon tự cắt, không lỗ ngoài ý muốn, không có đỉnh trùng.
- Không vẽ hộp/vạch cho phản chiếu trên capo, mặt đường ướt, đèn pha.
- Không vẽ đoán khi không nhìn thấy (đêm tối sâu): bỏ trống, ghi chú để vẽ tay sau.
- Không dùng label trùng nghĩa bản gạch dưới (mục 1).

## 6. Câu hỏi cần bạn chốt (các [ĐỀ XUẤT] quan trọng nhất)
- **Q1.** Capo/taplo của xe mình: cắt khỏi road (như tôi nghe được) và **không gán label nào**, đúng không?
- **Q2.** Vật thể: hộp ôm **phần nhìn thấy** hay **cả vật kể cả phần bị che** (amodal)? Tôi đề xuất phần nhìn thấy + bật `occluded`.
- **Q3.** Vạch đứt: **mỗi nét một polygon** hay **nối cả hàng nét thành một polygon dài**?
- **Q4.** Double white/yellow: **một polygon ôm cả hai vạch** hay **hai polygon riêng**?
- **Q5.** Vạch ở xa rất mờ hoặc bị xe che: **vẽ phần nhìn thấy** hay **nối suy qua chỗ bị che**?
- **Q6.** `traffic light`/`traffic sign` có bắt buộc vẽ khi xa dưới 12 px không?
- **Q7.** z_order: dùng bảng ở mục 3 làm chuẩn để tool kiểm và sửa, được không?
- **Q8.** `occluded` ngưỡng 30%: bạn muốn mức nào, hay chỉ bật khi che rõ ràng?

## 7. Từ quy ước sang tự động (làm sau khi chốt)
Mỗi dòng ở mục 2 thành một **validator** (kiểm shape đã vẽ) và một **luật sinh nháp**:
- `pole` → bề rộng < ~30 px, cao/rộng > 3, ≤ 8 đỉnh.
- `lane/*` → bề rộng gần đường thẳng, nằm trong road, mask màu đúng (trắng/vàng) ≥ ngưỡng.
- `crosswalk` → 4–6 đỉnh, nằm trong road, có ≥ 4–5 sọc song song.
- `area/*` → ⊆ road, direct ∩ alternative = ∅.
- Mọi polygon: hợp lệ, không khoét lỗ, z_order đúng bảng.
