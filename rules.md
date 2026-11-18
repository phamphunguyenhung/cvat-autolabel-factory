# CVAT Tools Rules (`rules.md`)

> Quy chuẩn bắt buộc khi vận hành, cải tiến và mở rộng `cvat_tools` cho mọi CVAT job mới.
> Tham chiếu thêm: `AGENTS.md` và `memory-bank/`.

## 1. Agent-Agnostic & CLI-First
- Mọi lệnh `python -m cvat_tools ...` / `cvat-tools ...` **phải chạy độc lập** không cần Pi, DeepSeek hay bất kỳ LLM nào.
- Pi extension (`.pi/extensions/cvat-tools.ts`) chỉ là lớp vỏ gọi CLI `--json`, tuyệt đối không chứa logic inference.

## 2. An toàn dữ liệu & Read-Only mặc định
- **Mặc định chỉ đọc CVAT**: mọi thao tác ghi lên CVAT (`store push`, `store rollback`) bắt buộc dry-run mặc định; chỉ ghi thật khi có `--yes` và `write_enabled=True`.
- **Tách biệt Ground Truth vs Draft**: mọi dự đoán tự động lưu trong `ShapeStore` (`data/store/shapes.sqlite`) ở stage `rule_draft` / `ai_draft` / `llm_edit`, tách khỏi `human_final`.
- **Backup + Audit + Rollback**: mỗi lần push thật phải tạo backup trước khi ghi, lưu run log vào `data/runs/*.json`, ghi ngược `cvat_id` về SQLite, và giữ nguyên shape `human_final` khi rollback.
- Khi push shape đã duyệt lên CVAT, giữ `source="manual"` (theo quy ước CVAT, không gắn nhãn `[AI]` lên preview hay annotation).

## 3. Tối ưu RAM 16 GB (CPU-First & Lazy Load)
- **Không import nặng khi khởi động CLI**: `torch`, `ultralytics`, `onnxruntime`, `transformers` chỉ được import lười khi tool thực sự chạy.
- **Tối đa 1 model nặng trong RAM**: `ModelRegistry` (`src/cvat_tools/core/model_registry.py`) tự `unload()` + `gc.collect()` model nặng trước khi nạp model nặng khác.

## 4. Quy chuẩn hiển thị & hình học CVAT (Áp dụng cho mọi Job mới)
- **Đúng loại hình (Shape Type)**:
  - **Things** (`car`, `truck`, `bus`, `motorcycle`, `bicycle`, `pedestrian`, `rider`, `traffic light`, `traffic sign`): xuất `rectangle`.
  - **Stuff / Areas / Lanes** (`road`, `sidewalk`, `building`, `vegetation`, `pole`, `sky`, `fence`, `terrain`, `area/direct`, `area/alternative`, `lane/*`): xuất **`polygon`** (bảo toàn danh sách đỉnh `points` trong JSON, không làm bẹp thành `rectangle`).
  - **Rule cứng cho `building` / `wall` (`geomrefine.py`)**: tòa nhà là khối kiến trúc — tối ưu bằng **`max_points=20`, `eps=1.5`, snap vuông góc `0°/90°`** (đã ablation với Agent C: giữ `straightness=0.933`, chỉ lệch `-0.0022` IoU so với bản thô 84 đỉnh mà không làm bẹp nhà có bậc/phối cảnh; không ép thành 4 đỉnh khi hình học không hỗ trợ).
- **Preview giống CVAT Web UI**:
  - Polygon tô mờ trong suốt theo tầng (`stuff 0.16`, `lane/area 0.26`, `rect 0.12`) + viền đúng màu hex CVAT của job.
  - Frame ban đêm (`is_night=True`) dùng halo sáng 1px sau viền màu tối (`luma < 75`) để không chìm vào nền tối.
  - Grid tổng quan (`summary_grid_20frames.jpg`) dùng `compact=True` (bỏ tag chữ nhỏ trên tile) và vẽ header sau khi resize để luôn sắc nét.

## 5. Quy tắc tổng quát hóa (Không overfit Job cũ)
- **Không copy/hardcode ground truth** từ job cũ sang job mới; mọi cải tiến phải đặt trong `src/cvat_tools/` để chạy tự động trên job chưa có nhãn.
- **Lane & Night (`lanes/framegen.py`)**:
  - Truyền **ảnh gốc (`img`)** vào `SegFormer-Lane-Marking` (tăng sáng CLAHE `enh` làm mờ vạch trên frame đêm); chỉ fallback top-hat khi `seg_m.sum() < 150`.
  - Lấy mẫu màu vàng (`warm` / `Lab b*`) bằng **p75 trong dải `±2px`** quanh tia để không bị nền nhựa đường pha loãng.
  - Ghép vạch đôi với `double_min = 10`, `double_gap_fill = 0.88`.
  - Crosswalk dùng **top-hat sọc ngựa vằn** (`paint_m=None`), kiểm tra độ đều khoảng cách sọc (`reg >= 0.45`).
  - `build_area`: fallback mép đường tối đa `1.35 * prior_half` và `min_alt_area = 15000.0` để tránh phình `area/direct` và sinh giả `area/alternative`.
- **Detection (`export` / `detection/`)**:
  - Lọc containment `_iomin >= 0.72` tránh box lồng nhau.
  - Loại `traffic light` giả ở nửa dưới mặt đường (`cy > 0.55 * H`) và nhiễu mui xe (`car` ở `y1 > 500`, `area < 2500`).

## 6. Quy chuẩn Pose17 Proposal, Review VS Code & Sync CVAT (`pose17_sync.py`)
- **Luôn đọc CVAT live mặc định khi `propose`**: `build_proposals` mặc định phải kéo annotation mới nhất từ CVAT qua PAT token (`offline=False`); chỉ đọc snapshot local khi truyền rõ `--offline`.
- **Cấm tuyệt đối tự ý dời tọa độ hoặc hardcode theo frame**: `build_proposals` trên shape đã có (`action="update"`) **chỉ được sửa cờ lỗi** (`skeleton.occluded`, xung đột `Q+O`, mặt/vai/hông `O` trong khung), phải giữ nguyên 100% tọa độ `(x, y)` người dùng đã đặt (`before_el["points"] == proposed_el["points"]`). Nghiêm cấm hardcode `if fidx == ...` để đảo cổ tay/gối.
- **Tôn trọng cờ `O` (`outside`) ở tay/chân khi gỡ xung đột `Q+O`**: `Q+O` trên tay/chân (`LIMB_IDS = {8..11, 14..17}`) luôn xóa `Q` và giữ `O` (`occluded=False, outside=True`); chỉ mặt/vai/hông (`FACE_TORSO_IDS`) nằm trong khung mới đưa về `Q`.
- **Mở ảnh in đậm trong VS Code trước khi sync**: Luôn render ảnh Before/Proposed nét dày + contact sheet và **tự động mở ngay bằng `code.cmd --reuse-window` trong VS Code** (không bắt người dùng tự bấm mở link). **Mọi case/frame cần người dùng review (`review_frames`, `proposed_corrections`, `before_after`) BẮT BUỘC phải tự động mở ảnh trên VS Code** thì người dùng mới xem và duyệt được. Áp dụng cho mọi ảnh kiểm chứng/so sánh (Pose17, Face50, Autolabel V2).
- **Chốt chặn chống ghi đè bản mới (Staleness Guard)**: `sync` mặc định dry-run; khi `--yes` bắt buộc đối chiếu `before_shape` với CVAT live hiện tại, nếu frame đã bị sửa trên CVAT sau lúc `propose` thì dừng và báo lỗi `Stale proposal` (không ghi đè). Luôn backup `before_sync_*.json` + `run_sync_*.json` và giữ `source="manual"`.

## 7. Quy chuẩn Face50 Verification & Alignment (`face50_engine.py`)
- **Kiểm tra hình học chặt theo tọa độ cục bộ (`validate_face50_frame`)**:
  - **Tight Inner-Lip Containment (`F50-R11`)**: `moitrong` (`42..49`) phải nằm trong `moingoai` (`30..41`) với ngưỡng **`d >= -0.05` px** (bắt cả lỗi lọt biên sub-pixel như `f105`, `f112`).
  - **Lip Self-Intersection (`F50-R10`, `LIP_SELF_INTERSECT`)**: Cấm các cạnh không kề nhau của `moingoai` (`30..41`) và `moitrong` (`42..49`) tự cắt nhau.
  - **Brow Local Geometry (`BROW_BELOW_EYE`, `BROW_NON_MONOTONIC_LOCAL`)**: Trong hệ tọa độ cục bộ khuôn mặt `(u, v)`, mọi điểm lông mày (`0..4`, `5..9`) phải có `u` đơn điệu tăng và nằm phía trên mí mắt trên (`15..17`, `23..25`).
- **Chuẩn hóa căn chỉnh ảnh tối / IR / xoay (`align_face50_clahe_fan`)**:
  - Tự động áp dụng **Gamma (`0.55` khi mean luma < 90) + LAB CLAHE (`clipLimit=2.5`)** trước khi chạy `FaceLandmarker(try_rotations=True)`.
  - Bắt buộc qua hậu xử lý **`BrowEdgeSnap`** (`F50-R09`: bám biên gradient Sobel quanh lông mày, giữ đơn điệu `u` và nằm trên mí mắt) và **`InnerLipClamp`** (ép `42..49` vào trong `moingoai`).
- **An toàn Sync (`sync_face50_eligible`)**:
  - Hỗ trợ cả `action="update"` (minimal PATCH) và `action="create"` (`cv.create_shapes`), bắt buộc dry-run mặc định, staleness guard chống ghi đè/trùng frame, giữ `source="manual"` trên mọi shape & element, backup trước ghi và read-back verification sau ghi.
