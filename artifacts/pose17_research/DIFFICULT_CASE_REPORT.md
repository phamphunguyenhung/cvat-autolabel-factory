# DIFFICULT_CASE_REPORT — Job 1623 (Frames 90–119)

> Tổng hợp từ [`difficult_cases.csv`](../../docs/guidelines/pose17/difficult_cases.csv), [`A05_cases.json`](agents/A05_cases.json), [`A04_visibility_audit.json`](agents/A04_visibility_audit.json), [`A06_geometry_metrics.json`](agents/A06_geometry_metrics.json) và ảnh overlay thực tế trong [`evidence/overlays/`](evidence/overlays/).

---

## 1. Phân bố mức độ & loại khó khăn (30 frame)

- **Tổng số frame phân tích:** `30` (`90..119`)
- **Mức độ nghiêm trọng:** `critical`: **8** (`f093, f094, f100, f106, f110, f112, f116, f118`), `high`: **12**, `medium`: **8**, `low`: **2** (`f090, f102`)
- **Phân loại theo taxonomy (một frame có thể thuộc nhiều nhóm):**
  - `SITTING_POSE`: 30/30
  - `VISIBILITY_CONFLICT`: 25/30
  - `KEYPOINT_MISPLACEMENT` (nhóm mới có bằng chứng): 24/30
  - `LOW_LIGHT`: 18/30 (toàn bộ 18 frame IR, `mean_luma` 12.8–36.4, tối nhất `f116` luma 12.8)
  - `RESOLUTION_MISMATCH` (nhóm mới): 18/30 (`15` frame `1280x1024`, `3` frame `512x424` so với `960x540` của BTC V1)
  - `FISHEYE_ROTATION` (nhóm mới) & `LEFT_RIGHT_AMBIGUITY`: 17/30 (15 frame nhìn nghiêng đầu bên trái + 2 frame fisheye nằm ngang đầu bên phải `f106, f110`)
  - `OCCLUSION` / `TRUNCATION` / `OUT_OF_FRAME` / `JOINT_INFERENCE`: phổ biến ở chi dưới (vô-lăng, bảng taplo, báo/sách, mép dưới/phải khung hình)
  - `MISSING_ANNOTATION` (nhóm mới): 2/30 (`f100` nhòe chuyển động, `f118` gục mặt)
  - `MOTION_BLUR`: `f100` (Laplacian variance thấp ở vùng tay chuyển động)

---

## 2. Các case tiêu biểu cần ưu tiên xử lý (trong `proposed_corrections.csv`)

| Frame | Ảnh | Mức độ | Vấn đề thực tế quan sát được | Rule liên quan | Bằng chứng overlay & Before/After |
|---:|---|---|---|---|---|
| 93 | `G06_094.jpg` | `critical` | Skeleton-level `occluded=True` làm cả 17 điểm thành Q/O (`V:0 Q:14 O:3`), `7Q` lệch xuống ~80 px, `2O` (mắt R) đặt `outside`, `16O/17O` chéo sang bệ | `P17-G11, P17-G13, P17-G15, P17-G23` | [`f093_G06_094.jpg`](evidence/overlays/f093_G06_094.jpg) · [`before_after`](evidence/before_after/f093_before_after.jpg) |
| 100 | `G06_101.jpg` | `critical` | `0` skeleton (`MISSING_ANNOTATION`), ảnh RGB có nhòe chuyển động ở tay/bút | `P17-G02, P17-G20` | [`f100_G06_101.jpg`](evidence/overlays/f100_G06_101.jpg) |
| 101 | `G06_102.jpg` | `high` | `kpt 2 (eye_R, visible)` và `kpt 4 (ear_R, occluded)` trùng gần như tuyệt đối (`0.2657 px` tại `(265, 141)`) | `P17-G07, P17-G10` | [`f101_G06_102.jpg`](evidence/overlays/f101_G06_102.jpg) · [`before_after`](evidence/before_after/f101_before_after.jpg) |
| 106 | `G06_107.jpg` | `critical` | Fisheye IR nằm ngang (đầu phải); toàn bộ 7 cặp R/L đảo theo trục dọc ảnh; `3O` (mắt L) và `5O` (tai L) đánh `outside` dù đầu nằm rõ trong ảnh | `P17-G06, P17-G08, P17-G15, P17-G17` | [`f106_G06_107.jpg`](evidence/overlays/f106_G06_107.jpg) |
| 113 | `G06_114.jpg` | `high` | Cổ tay `10/11` đảo ngược (`-134.39 px` theo trục thân), gây 4 đoạn tự cắt và `forearm_L` kéo dài (`0.872x` thân) | `P17-G06, P17-G07, P17-G23` | [`f113_G06_114.jpg`](evidence/overlays/f113_G06_114.jpg) · [`before_after`](evidence/before_after/f113_before_after.jpg) |
| 114 | `G06_115.jpg` | `high` | Sau chỉnh tay `kpt 8` (+65.31 px), `forearm_R (8-10)` chỉ còn `48.83 px` (`0.139x` thân, ngoại lai thống kê) | `P17-G07, P17-G25` | [`f114_G06_115.jpg`](evidence/overlays/f114_G06_115.jpg) · [`before_after`](evidence/before_after/f114_before_after.jpg) |
| 116 | `G06_117.jpg` | `critical` | IR rất tối (`mean_luma=12.8`); `5` xung đột `occluded+outside`; `10O` đặt lên mũi/mặt, `8O` trôi ngoài thân, `6Q` lệch lên cổ | `P17-G07, P17-G11, P17-G15` | [`f116_G06_117.jpg`](evidence/overlays/f116_G06_117.jpg) · [`before_after`](evidence/before_after/f116_before_after.jpg) |
| 117 | `G06_118.jpg` | `high` | `kpt 6 (vai R)` đặt nhầm lên cằm/mũi `(340, 171)`; `4O (tai R)` đánh `outside` trên trán | `P17-G07, P17-G15, P17-G17` | [`f117_G06_118.jpg`](evidence/overlays/f117_G06_118.jpg) · [`before_after`](evidence/before_after/f117_before_after.jpg) |
| 118 | `G06_119.jpg` | `critical` | `0` skeleton (`MISSING_ANNOTATION`), tài xế gục mặt sát góc trên trái | `P17-G02, P17-G15, P17-G20` | [`f118_G06_119.jpg`](evidence/overlays/f118_G06_119.jpg) |

> Toàn bộ 30 case có thể tra cứu tự động bằng CLI: `python -m tools.pose17 open-case --case-id CASE-1623-F093` hoặc lọc theo rule: `python -m tools.pose17 lookup-rule --rule-id P17-G11`.
