# Workflow Day 5 (MOT17-09, P1-P5)

Frame CVAT 0-based (0..149); MOT 1-based = +1. Job hiện tại: 15 (task 17). Luật: `RULES.md` cấm nộp box/track AI như nhãn của mình.

## A. Chế độ manual-assist (luôn dùng được, không AI, chỉ đọc)
1. Tự gán P1-P5 trong CVAT (track mode, rectangle, keyframe thưa, `outside` khi rời khung).
2. `python -m cvat_tools track assist --project day05-mot17`
   - Báo cáo: box nhảy bất thường, track đứt (outside rồi nối lại), track trùng, thiếu keyframe, nội suy nhanh bất thường, frame cần mở lại.
   - File: `data\exports\day05-mot17\assist_report.md/.json`. Không sửa nhãn.
3. Mở lại các frame trong danh sách, tự sửa, chạy lại đến khi sạch. `python -m mtm check --job 15` cho thêm kiểm tra ngưỡng của lab.
4. `python -m cvat_tools export --project day05-mot17 --format mot` chỉ để tự đối chiếu; file nộp là bản xuất chính thức từ CVAT.

## B. Chế độ nháp AI (chỉ khi giảng viên cho phép, ghi vào báo cáo)
```powershell
python -m cvat_tools detect       --project day05-mot17 --profile balanced --allow-ai-draft
python -m cvat_tools track bench  --project day05-mot17 --profile balanced --allow-ai-draft
python -m cvat_tools track keyframes --project day05-mot17 --tracker bytetrack --allow-ai-draft
python -m cvat_tools track review --project day05-mot17 --allow-ai-draft      # mở data\exports\day05-mot17\review.html
```
Quyết định trong review.html lưu riêng (nút tải JSON). Ánh xạ P1-P5 là của người duyệt, không phải ID tracker. Ghi lên CVAT chỉ qua
`python -m mtm apply --job 15 --allow...` (dry-run mặc định, `--yes` mới ghi, backup + rollback).

## C. Benchmark tái lập
```powershell
python scripts\run_detector_bench.py --limit 30 --idle-wait 120
python -m cvat_tools.benchmark.ablation --limit 60 --idle-wait 120
python -m cvat_tools.benchmark.figures --limit 60 --frame 30
```
