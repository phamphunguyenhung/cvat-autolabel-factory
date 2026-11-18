# F01 — CVAT Face50 Reader Report (Job 1975 / Task 473)

**Mode:** Read-only (`Cvat.from_env('edufun', write_enabled=False)`)  
**Task:** `473` (`W2-FACE-G6-T1`) | **Job:** `1975` | **Project:** `229`  
**Job State:** `state="in progress"`, `stage="annotation"`, `status="annotation"`  
**Updated Date (live):** `2026-11-18T04:43:41.224172Z` (refreshed from `2026-11-18T01:36:42.919331Z`)  
**Frame Range:** `90..119` (`30` frames total)

---

## 1. Snapshot Files Saved / Verified

| Artifact | Status | Notes |
| :--- | :--- | :--- |
| [job_1975_live_pre_goal.json](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/snapshots/job_1975_live_pre_goal.json) | Saved (live) | `version=0`, `196` shapes, `0` tracks, `0` tags |
| [job_1975.json](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/snapshots/job_1975.json) | Refreshed | `updated_date` updated to `2026-11-18T04:43:41.224172Z` |
| [job_1975_meta.json](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/snapshots/job_1975_meta.json) | Unchanged (`same=True`) | `30` frames (`90..119`), resolutions verified |
| [job_1975_labels.json](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/snapshots/job_1975_labels.json) | Unchanged (`same=True`) | `7` skeleton labels, `50` sublabels total |

### Delta vs Prior `job_1975_annotations_raw.json`
- Shape IDs are identical (`196` shapes; no added/deleted shapes).
- `19` shapes have updated coordinates/attributes across `7` frames:
  - `f090`: 7 (`songmui`, `mattrai`, `longmaytrai`, `longmayphai`, `matphai`, `moingoai`, `moitrong`)
  - `f096`: 2 (`moitrong`, `moingoai`)
  - `f099`: 1 (`moitrong`)
  - `f101`: 1 (`moitrong`)
  - `f104`: 2 (`matphai`, `mattrai`)
  - `f107`: 5 (`songmui`, `moingoai`, `moitrong`, `longmaytrai`, `longmayphai`)
  - `f108`: 1 (`moitrong`)

---

## 2. Label Schema Summary

| Label ID | Name | Type | Keypoints |
| ---: | :--- | :--- | ---: |
| `17732` | `longmaytrai` | `skeleton` | 5 |
| `17738` | `longmayphai` | `skeleton` | 5 |
| `17744` | `songmui` | `skeleton` | 4 |
| `17749` | `mattrai` | `skeleton` | 8 |
| `17758` | `matphai` | `skeleton` | 8 |
| `17767` | `moingoai` | `skeleton` | 12 |
| `17780` | `moitrong` | `skeleton` | 8 |
| **Total** | **7 labels** | `skeleton` | **50** |

---

## 3. Aggregate Inventory (Frames `90..119`)

- **Annotated frames:** `28 / 30` (every annotated frame has all `7` skeleton shapes and `50` keypoints; `0` incomplete frames)
- **Missing frames (0 shapes):** `2 / 30` — **Frame `102`** (`G06_103.jpg`, `1280x1024`) and **Frame `106`** (`G06_107.jpg`, `1280x1024`)
- **Total shapes:** `196` (`type="skeleton"`, `group=0`, `attributes=0`, shape-level `occluded=0`, `outside=0`)
- **Total keypoints:** `1400`
  - **Visible** (`occluded=False, outside=False`): `1335` (`95.36%`)
  - **Occluded (`Q`)** (`occluded=True`): `65` (`4.64%`)
  - **Outside (`O`)** (`outside=True`): `0` (`0.00%`)
  - **Both `Q` & `O`:** `0`
  - **`Q+O` total:** `65`
- **Source field:** `manual` on all `196` shapes and all `1400` keypoint elements (`100% manual`)
- **Out-of-bounds keypoint coordinates** (`x < 0` or `x > width` or `y < 0` or `y > height`): `0`

### Per-Label Breakdown on Frames with `Q+O > 0`
- **Frame `91`** (`G06_092.jpg`): `Q=16, O=0` -> `mattrai` (`8/8` occ), `matphai` (`8/8` occ)
- **Frame `104`** (`G06_105.jpg`): `Q=16, O=0` -> `mattrai` (`8/8` occ), `matphai` (`8/8` occ)
- **Frame `107`** (`G06_108.jpg`): `Q=23, O=0` -> `songmui` (`3/4` occ), `moingoai` (`12/12` occ), `moitrong` (`8/8` occ)
- **Frame `118`** (`G06_119.jpg`): `Q=10, O=0` -> `longmayphai` (`3/5` occ), `matphai` (`7/8` occ)

---

## 4. Per-Frame Inventory (All 30 Frames)

| Frame | Image File | Size | Shapes | Keypoints | Visible | Occluded (`Q`) | Outside (`O`) | `Q+O` | Source (Shapes / Elements) | Status |
| ---: | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | :--- | :--- |
| `90` | `G06_091.jpg` | `640x480` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `91` | `G06_092.jpg` | `640x480` | 7 | 50 | 34 | 16 | 0 | 16 | `manual:7` / `manual:50` | Complete (`Q` on eyes) |
| `92` | `G06_093.jpg` | `1280x1024` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `93` | `G06_094.jpg` | `1280x720` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `94` | `G06_095.jpg` | `1280x1024` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `95` | `G06_096.jpg` | `1280x1024` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `96` | `G06_097.jpg` | `960x540` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `97` | `G06_098.jpg` | `960x540` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `98` | `G06_099.jpg` | `960x540` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `99` | `G06_100.jpg` | `640x480` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `100` | `G06_101.jpg` | `960x540` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `101` | `G06_102.jpg` | `1280x720` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `102` | `G06_103.jpg` | `1280x1024` | 0 | 0 | 0 | 0 | 0 | 0 | `-` | **MISSING** |
| `103` | `G06_104.jpg` | `640x480` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `104` | `G06_105.jpg` | `512x424` | 7 | 50 | 34 | 16 | 0 | 16 | `manual:7` / `manual:50` | Complete (`Q` on eyes) |
| `105` | `G06_106.jpg` | `960x540` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `106` | `G06_107.jpg` | `1280x1024` | 0 | 0 | 0 | 0 | 0 | 0 | `-` | **MISSING** |
| `107` | `G06_108.jpg` | `640x480` | 7 | 50 | 27 | 23 | 0 | 23 | `manual:7` / `manual:50` | Complete (`Q` on nose/mouth) |
| `108` | `G06_109.jpg` | `1280x720` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `109` | `G06_110.jpg` | `640x480` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `110` | `G06_111.jpg` | `1280x1024` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `111` | `G06_112.jpg` | `1280x1024` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `112` | `G06_113.jpg` | `512x424` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `113` | `G06_114.jpg` | `640x480` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `114` | `G06_115.jpg` | `640x480` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `115` | `G06_116.jpg` | `640x480` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `116` | `G06_117.jpg` | `1280x1024` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `117` | `G06_118.jpg` | `640x480` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
| `118` | `G06_119.jpg` | `960x540` | 7 | 50 | 40 | 10 | 0 | 10 | `manual:7` / `manual:50` | Complete (`Q` on right brow/eye) |
| `119` | `G06_120.jpg` | `640x480` | 7 | 50 | 50 | 0 | 0 | 0 | `manual:7` / `manual:50` | Complete |
