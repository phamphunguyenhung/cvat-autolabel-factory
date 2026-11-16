# Job theo tuần (CVAT edufun)

Mỗi tuần 1 file `weeks/<năm>-W<tuần ISO>.yaml` liệt kê job được giao. Dữ liệu job edufun nằm ở `data/jobs/edufun/<job_id>/`; job local giữ `data/jobs/<job_id>/` (vd 285). `week status` tự tạo thư mục khi job tồn tại trên CVAT.

```powershell
# 1. Cấu hình 1 lần: trong cvat\.env thêm  CVAT_EDUFUN_PAT=<PAT lớp edufun>
python -m cvat_tools week new                 # tạo file tuần hiện tại từ _template.yaml
# 2. sửa weeks\2026-W47.yaml: điền job id, kind, due
python -m cvat_tools week status              # chỉ đọc: trạng thái thật trên CVAT của mọi job trong tuần hiện tại
python -m cvat_tools week status --week 2026-W46
python -m cvat_tools week list                # các tuần đã có
```

Quy ước: `week status` chỉ đọc CVAT. Ghi lên CVAT vẫn đi qua `store push --yes` như `docs/CVAT_SAFETY.md`.

## Hai CVAT, đừng nhầm
| profile | Là gì | Cấu hình |
|---|---|---|
| `edufun` | CVAT online BTC cấp (`https://cvat.edufun.ai`, org `cohort-5a`) | `config/cvat.edufun.yaml` + `CVAT_EDUFUN_PAT` |
| `local` | CVAT docker tự chạy (`http://localhost:8080`) | `config/cvat.local.yaml` + `CVAT_PAT` |

Mặc định cả tuần dùng `edufun`; job nào chạy thử trên docker thì thêm `profile: local` ở job đó. **Job id của 2 server độc lập nhau** (job 3 local ≠ job 3 edufun), luôn kiểm tra cột profile trong `week status`.
