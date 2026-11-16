# Quy ước vẽ chung — job BBox · Polygon · Polyline (ảnh đường phố dashcam)

Áp dụng cho mọi job dùng bộ label chung, không riêng một job. Mọi tool sinh nháp và validator phải theo file này.

Thứ tự ưu tiên khi các nguồn mâu thuẫn: **quy ước của bạn** > Sổ tay nhãn W1 (BTC) > mặc định của tôi.
Mặc định của tôi ghi **(mặc định)** ở cuối dòng. Danh sách các mặc định chưa được bạn xác nhận nằm ở mục 9.

## 1. Nguyên tắc chung
1. **Polygon nguyên vùng.** Không khoét lỗ. Vật phía trên đè lên vật phía dưới bằng `z_order`; xuất file ra vẫn giữ đúng thứ tự chồng.
2. **Vẽ đúng hình dạng thực của vật**, ít đỉnh nhất mà vẫn ôm đúng. Đường bao không tự cắt, không đỉnh trùng.
3. **Chỉ vẽ phần nhìn thấy.** Phần bị che do vật khác thì không vẽ bù, bật cờ che khuất (mục 5). *(mặc định)*
4. **Không có vật trong ảnh thì không có shape.** Vật nằm hoàn toàn ngoài khung thì không vẽ.
5. **Chỉ dùng đúng label có sẵn**, không tạo, không đổi tên, không gộp class. Tool chỉ **thêm** shape, không xóa hay sửa shape của người.
6. **Không vẽ đoán.** Không nhìn thấy rõ (ảnh tối sâu, quá xa) thì bỏ trống để vẽ tay sau.

## 2. Kiểu hình theo nhóm label

| Nhóm | Label | Kiểu hình |
|---|---|---|
| Vật thể | `pedestrian`, `rider`, `car`, `truck`, `bus`, `train`, `motorcycle`, `bicycle`, `traffic light`, `traffic sign` | **Rectangle** |
| Nền | `road`, `sidewalk`, `building`, `wall`, `fence`, `vegetation`, `terrain`, `sky` | **Polygon** |
| Cột | `pole` | **Polygon hình chữ nhật hẹp** theo thân cột |
| Vạch kẻ | `lane/single white`, `lane/single yellow`, `lane/double white`, `lane/double yellow`, `lane/single other`, `lane/double other` | **Polygon rất hẹp, gần như đường thẳng** |
| Vạch ngựa vằn | `lane/crosswalk` | **Polygon 4–6 điểm** bao cả dải sọc |
| Lề đường | `lane/road curb` | Polygon hẹp theo mép bó vỉa *(mặc định)* |
| Vùng làn | `area/direct`, `area/alternative` | Polygon |

**Label trùng nghĩa:** `traffic light`, `traffic sign`, `pedestrian` (có dấu cách) là bản dùng cho job BBox/polygon. Bản `traffic_light`, `traffic_sign`, `person` (gạch dưới) thuộc job Segmentation, **không dùng** ở đây.

## 3. Quy ước từng label

### 3.1 Vạch kẻ (lane/\*)
Quy tắc chung của vạch:
- Polygon **hẹp gần như đường thẳng**, chạy theo **tim vạch**.
- Chỉ vẽ **trong vùng nhận ra được màu đó** (trắng hoặc vàng). **Không vẽ nhiều**: không có vạch rõ thì không vẽ.
- Rộng theo phối cảnh: vài px ở xa, vài chục px ở gần. Không bao giờ phình thành mảng rộng.
- Nét **liền hay đứt dùng chung một class**.

| Label | Cách vẽ |
|---|---|
| `lane/single white` | Một vạch trắng. Nét đứt: **một polygon liền** chạy qua các khoảng hở nhỏ, chỉ dừng khi vạch biến mất hẳn. |
| `lane/single yellow` | Như trên, màu vàng. Ban đêm vàng nhạt dễ tưởng trắng: phóng to kiểm màu. |
| `lane/double white` | Hai vạch trắng song song: **một polygon** theo đường giữa cặp vạch, không vẽ hai đường. |
| `lane/double yellow` | Như double white, màu vàng. |
| `lane/single other` / `lane/double other` | Vạch màu khác trắng và vàng (đỏ, xanh...), hiếm. Vạch trắng bị ánh đèn nhuộm màu vẫn là white. Không chắc màu thì không vẽ. |

### 3.2 Vạch ngựa vằn (`lane/crosswalk`)
- Polygon 4–6 điểm bao **cả dải sọc**, theo hướng ngang của dải (vuông góc hướng xe chạy).
- Sọc bị xe che một phần: vẫn ôm trọn dải nếu nhìn thấy hai đầu dải (polygon nguyên vùng).
- Vạch qua đường ở xa, phía bên kia ngã tư: vẽ nếu nhìn rõ.

### 3.3 Lề đường (`lane/road curb`)
- Polygon hẹp theo mép bó vỉa, ngăn mặt đường với vỉa hè, cỏ hoặc chân tường, từ gần ra xa. *(mặc định)*

### 3.4 Vùng làn
| Label | Cách vẽ |
|---|---|
| `area/direct` | Làn **xe mình đang chạy thẳng tiếp được**, từ sát mép trên capo lên điểm xa nhất còn thấy rõ, giới hạn bởi hai vạch làn hoặc hai mép đường. **Có xe phía trước vẫn vẽ vùng liền** (xe có box riêng). Không tô lên capo. Đường không kẻ vạch: lấy phần mặt đường xe đang chạy. |
| `area/alternative` | **Phần còn lại của `road` sau khi trừ `area/direct`**, tức lát cắt `road − direct`. Lấy đúng phần đó, polygon nguyên vùng. Biên chung với `direct` trùng khít biên của `direct`. *(theo bạn, thay cho định nghĩa "làn cùng chiều" của Sổ tay)* |

Cả hai polygon nằm trong `road`; `direct` và `alternative` không chồng lên nhau, và `direct ∪ alternative` phủ gần hết `road`. Khi `direct` đã phủ gần hết `road` thì có thể không có `alternative` hoặc chỉ là một lát mỏng.

### 3.5 Vật thể (rectangle)
- Hộp **ôm sát 4 điểm ngoài cùng** (trái, phải, trên, dưới) của phần nhìn thấy. Mỗi vật một hộp, hộp được chồng nhau.
- **Bắt buộc vẽ** khi vật bị che hoặc bị cắt đến 80% (còn nhìn thấy ít nhất 20%).
- Không ôm bóng đổ dưới gầm; ôm cả gương, cản, bánh xe. Xe xa chỉ thấy đèn: vẽ nếu đoán được khung xe.
- Không vẽ cho: capo/taplo của xe mình, hình phản chiếu (kính, mặt đường ướt, capo), vật trên poster hoặc màn hình.
- `traffic light`: chỉ ôm **hộp đèn tín hiệu**, không ôm cột. Không gồm đèn đường, đèn xe, đèn quảng cáo.
- `traffic sign`: chỉ ôm **mặt biển**, không ôm cột; giàn nhiều biển thì mỗi tấm một hộp. Không gồm biển quảng cáo, biển hiệu cửa hàng.
- `rider`: ôm người từ mũ tới chân trên xe; xe hai bánh vẽ hộp riêng (`motorcycle`, `bicycle`). `pedestrian`: từ đỉnh đầu tới gót chân, không kéo hộp ôm ô hay túi.

### 3.6 Nền (polygon nguyên vùng)
| Label | Cách vẽ |
|---|---|
| `road` | Cả mặt đường lái được, **kể cả phần xe đang đè lên** (xe có z_order cao hơn). Gồm vạch kẻ trên đường. **Cắt bỏ capo/taplo xe mình**, không gán label. Biên theo mép đường/bó vỉa. |
| `sidewalk` | Vỉa hè, bám sát mép bó vỉa giáp road. Người, xe, cột trên vỉa hè đè bằng z_order. *(mặc định)* |
| `building` | Mặt tiền tòa nhà nhìn thấy; **biên thẳng theo mép nhà**; biên trên theo đường viền mái với trời. *(mặc định)* |
| `sky` | Vùng trời, biên dưới bám mái nhà, ngọn cây, cột. Ban đêm giảm opacity và phóng to để tìm biên. *(mặc định)* |
| `vegetation` | Tán cây, bụi cây, thân cây. Biên **mượt, ít điểm**, không đuổi từng lá. Kẽ lá nhỏ thấy trời: tính cả là vegetation. *(mặc định)* |
| `terrain` | Đất, cỏ thấp, dải cỏ. Cỏ cao hoặc bụi rậm là vegetation. *(mặc định)* |
| `wall` | Tường độc lập kín đặc, dải phân cách bê tông liền khối. *(mặc định)* |
| `fence` | Hàng rào có khe hở: rào sắt, lưới, lan can thanh. Không nhầm tấm bạt hay biển công trình với fence. *(mặc định)* |
| `pole` | Cột đèn, cột điện, cột biển, kể cả cần vươn ngang. Polygon **hình chữ nhật hẹp** ôm thân cột từ chân tới đỉnh: 4 điểm nếu thẳng, tối đa 6–8 điểm nếu gấp khúc. Giữ đúng độ mảnh, không tô phình. |

## 4. z_order (thứ tự chồng, từ sau ra trước)
Số lớn hơn nằm trên.

| z | Nhóm |
|---|---|
| -6 | `road` |
| -5 | `area/alternative` |
| -4 | `area/direct` |
| -3 | `lane/*` (gồm crosswalk, curb) |
| -2 | `pole` |
| 0 | Vật thể (rectangle) |

Nền khác (`sky`, `building`, `vegetation`, `sidewalk`, `terrain`, `wall`, `fence`) nằm dưới `road` hoặc cạnh `road`, không chồng nhau đáng kể; `sky` xa nhất. *(mặc định)* Hai vật thể chồng nhau: vật có cạnh dưới thấp hơn trong ảnh (gần camera hơn) nằm trên.

## 5. Che khuất và cắt mép
- Chỉ **10 label vật thể** (`pedestrian`, `rider`, `car`, `truck`, `bus`, `train`, `motorcycle`, `bicycle`, `traffic light`, `traffic sign`) có hai thuộc tính checkbox **`occluded`** và **`truncated`**. Bật chúng cho các vật thể này.
- **`occluded`:** vật bị vật khác che. Xe phía sau bị xe phía trước che thì bật `occluded`.
- **`truncated`:** vật bị mép khung ảnh cắt.
- Label nền, lane và area **không có thuộc tính**: nếu cần chỉ dùng cờ `occluded` có sẵn của shape CVAT, bật khi bị vật thể che đáng kể. *(mặc định)*
- Ngưỡng che khuất tính tự động cho tool: **30% diện tích** bị che thì bật `occluded`. *(mặc định, chỉnh được)*

## 6. Những điều cấm
- Vạch bè rộng như một mảng, hoặc polygon vạch dài hơn vùng có màu nhận ra được.
- Khoét lỗ polygon; polygon tự cắt hoặc có đỉnh trùng.
- Vẽ cho phản chiếu (capo, kính, mặt đường ướt, đèn pha), bóng đổ, vật trên biển quảng cáo.
- Vẽ đoán khi không nhìn thấy.
- Dùng bản label gạch dưới (`traffic_light`, `traffic_sign`, `person`) trong job này.
- Vẽ `area/alternative` ra ngoài `road`, hoặc chồng lên `area/direct`.

## 7. Từ quy ước sang tự động
Mỗi quy tắc thành một **validator** (kiểm shape đã vẽ) và một **luật sinh nháp**:
- `pole`: bề rộng nhỏ, cao/rộng lớn (tỉ lệ cột), ≤ 8 đỉnh.
- `lane/*`: bề rộng gần đường thẳng, nằm trong road, mask màu đúng (trắng hoặc vàng) đủ nhiều trong polygon.
- `crosswalk`: 4–6 đỉnh, nằm trong road, có nhiều sọc song song.
- `area/*`: nằm trong road; `direct` ∩ `alternative` rỗng.
- Mọi polygon: hợp lệ hình học, không khoét lỗ, `z_order` đúng bảng mục 4.
- Vật thể: hộp ôm sát phần nhìn thấy; `occluded`/`truncated` tính từ chồng lấn và mép khung.

## 8. Thứ tự sinh nháp
Từ ít sửa nhất đến nhiều sửa nhất: vật thể rectangle → đèn và biển → `area/*` (dẫn xuất từ `road` và hai vạch biên) → `lane/*` và crosswalk (người chấm vài điểm, tool nội suy) → nền sáng (sky, building, vegetation) → sidewalk, terrain, wall, fence, pole → nền và lane ở ảnh tối.

## 9. Mặc định chưa được bạn xác nhận
Những dòng đánh dấu *(mặc định)* ở trên là do tôi đề xuất. Cần bạn xác nhận hoặc sửa trước khi coi là chuẩn, nhất là:
1. Ngưỡng `occluded` 30% cho tool.
2. Biên và cách vẽ của `building`, `sky`, `vegetation`, `sidewalk`, `terrain`, `wall`, `fence`.
3. `lane/road curb` là polygon hẹp theo mép bó vỉa.
4. Nền khác nằm dưới road hay cạnh road, không chồng nhau đáng kể.
5. Vật thể: hộp ôm phần nhìn thấy (không ôm phần bị che).

## 10. Chỗ khác với Sổ tay nhãn W1 (theo bạn, ưu tiên quy ước của bạn)
- Vạch lane: Sổ tay dùng **polyline theo tim vạch**; file này dùng **polygon hẹp** theo bạn nói.
- Crosswalk: Sổ tay đề xuất **2 polyline** (mép gần và mép xa); file này dùng **polygon 4–6 điểm**.
- `area/alternative`: Sổ tay định nghĩa là "làn cùng chiều bên cạnh"; file này dùng `road − direct` theo bạn nói.
- Phạm vi: Sổ tay giới hạn job BBox ở **20 nhãn**, các nhãn nền thuộc job Segmentation; file này vẫn quy ước cho cả nhãn nền theo yêu cầu "label nào cũng làm được".
