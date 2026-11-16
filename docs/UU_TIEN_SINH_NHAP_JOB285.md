# Thứ tự ưu tiên sinh nháp — job 285 (dễ → khó, ít sửa tay nhất)

Tiêu chí xếp hạng: **ít sửa tay nhất trên mỗi shape × nhiều shape**. Một nhãn lên cao khi (1) có nguồn tự động đáng tin, (2) hình đơn giản, (3) có nhiều shape, (4) sửa nhanh.

Căn cứ chỉ dùng số đã đo hoặc quan sát thật. Chỗ chưa đo ghi rõ **[chưa đo]**. Thời gian sửa tay mỗi shape **chưa đo** (cần D2 trong bộ câu hỏi PDCA), nên thứ hạng dựa trên độ chính xác và độ phức tạp hình, không dựa trên giây.

## Cổng trước khi bắt đầu
- **Q10:** job 285 chỉ làm **20 nhãn của sổ tay**, hay cả nhãn nền (road, sky, building, pole, vegetation...)? Bậc 5–7 chỉ áp dụng nếu bạn chọn làm cả nhãn nền.
- **Q9:** lane/crosswalk dùng polyline hay polygon hẹp? Bậc 4 phụ thuộc câu này.

## Bảng ưu tiên

| Bậc | Nhãn | Cách sinh nháp | Căn cứ đã đo | Bạn phải sửa gì |
|---|---|---|---|---|
| **0** | `road` | **Không sinh.** Bạn đã vẽ tay 20/20 frame | CVAT có 20 polygon road | — (là gốc cho bậc 3) |
| **1** | `car`, `truck`, `bus`, `motorcycle`, `pedestrian` (rectangle) | YOLO26l theo tile (script đã có) | Đúng nhãn 94.8% trên 97 hộp ghép được; 178 car đã có trên CVAT | Xóa báo nhầm (phản chiếu capo); thêm xe xa/đêm mà YOLO bỏ sót (41 hộp tay YOLO không thấy); hộp TINY |
| **2** | `traffic light`, `traffic sign` (rectangle) | YOLO (đèn) + SegFormer (biển) | Đã ghi 22 + 18 hộp từ nháp, người dùng chấp nhận để sửa | Hộp TINY < 12 px; biển xa; đèn bị nhầm với đèn đường |
| **3** | `area/direct`, `area/alternative` | **Dẫn xuất** từ road tay + 2 vạch biên (anchor + nội suy), không dò vạch | Frame 61 (anchors thử): direct rộng 586 px so với nêm cũ 262 px; 14 frame direct đã có tay | Kiểm biên phải ở đêm; `alternative` chỉ **làn cùng chiều** (sổ tay), không phải "road − direct" |
| **4** | `lane/single/double white/yellow`, `lane/crosswalk` | **Anchor + nội suy** (bạn chấm 4–5 frame neo, tool nội suy 20 frame). Dò tự động chỉ để gợi ý snap ở frame sáng | Dò tự động: lane trắng có ở 6/20 frame; crosswalk đúng 1/4, báo nhầm 6 lần/16 frame. Nội suy: chưa đo vì chưa có anchor | Chấm anchor; sửa đoạn lệch ở frame giữa; vạch đứt/che |
| **5** | `sky`, `building`, `vegetation` (**chỉ frame sáng**) | SegFormer-B2 (ONNX có sẵn) → làm sắc/mượt | Frame sáng: sky 6, vegetation 21, building 14 đã ghi và bạn chấp nhận để sửa; đêm ra mảng rác | Chỉnh biên; building cần biên thẳng |
| **6** | `sidewalk`, `terrain`, `wall`, `fence`, `pole` | Seg + luật hình (pole: hẹp, cao/rộng > 3) | Pole 12, sidewalk 9 đã ghi; wall/fence model hay nhầm (tấm bạt thành fence) | Nhiều: cột mảnh, ranh sidewalk/road |
| **7** | Tất cả nhãn nền + lane ở **13 frame đêm**; `lane/road curb`; `lane/*other` | Anchor tay + nội suy, hoặc vẽ tay | SegFormer-B2 ra mảng rác; lane đêm tối sâu gần như không ra; curb mới có 4 shape thử | Gần như vẽ tay. Cần chứng minh bằng số rồi mới bỏ nháp |

## Vì sao xếp như vậy
1. **Bậc 0–2** có nhiều shape nhất và hộp chữ nhật đơn giản nhất. YOLO đã chứng minh độ chính xác nhãn 94.8%, nên ít sửa nhất. Phần việc của bạn chỉ là xóa và bổ sung.
2. **Bậc 3** không cần phát hiện: nó là phép tính hình học từ road bạn đã vẽ cộng hai vạch biên. Lỗi chính cũ (xe che làn) không ảnh hưởng vì không dựa vào vạch dò được.
3. **Bậc 4** khó ở chỗ máy không dò được vạch ổn định. Cách khắc phục là để bạn chấm vài điểm rồi nội suy. Bạn chấm ít điểm hơn nhiều so với vẽ cả 20 frame.
4. **Bậc 5–7** phụ thuộc phân vùng ảnh và độ sáng. Đêm là chỗ yếu nhất nên đặt cuối.

## Thứ tự thực hiện (mỗi bước có cổng nghiệm thu)
1. **Bậc 1–2:** chạy lại bbox_draft cho 20 frame, ghi shape còn thiếu. Cổng: số hộp xóa/thêm trên mỗi frame giảm so với lần trước.
2. **Bậc 3:** chạy `lane_assist_area.py` sau khi có anchors 2 vạch biên ở frame 60, 69, 79. Cổng: direct nằm trong road, direct ∩ alternative rỗng.
3. **Bậc 4:** chấm anchor lane và crosswalk, chạy nội suy, đo leave-one-out (`lane_assist_eval.py`, cần ≥ 3 frame neo). Cổng: sai số px chấp nhận được do bạn đặt ra.
4. **Bậc 5–6:** chạy chuỗi seg → refine (W3, W4) chỉ trên frame sáng. Cổng: bạn sửa nhanh hơn vẽ mới (cần đo thời gian).
5. **Bậc 7:** quyết định theo số đo: giữ nháp, chuyển sang anchor, hay bỏ nháp để vẽ tay.

## Chưa biết, cần đo trước khi chốt thứ hạng
- Thời gian sửa trung bình mỗi shape theo từng nhãn.
- Nội suy từ anchor lệch bao nhiêu px so với bạn tự vẽ ở frame giữa.
- B5 và Mask2Former có hơn B2 trên frame đêm không (W3 đang đo).
