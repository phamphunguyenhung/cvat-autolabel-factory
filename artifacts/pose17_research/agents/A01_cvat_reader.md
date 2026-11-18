# A01 — CVAT Reader Report (Job 1623 / Pose17)

**Mode:** Read-only (`Cvat.from_env('edufun', write_enabled=False)`, `https://cvat.edufun.ai`, `X-Organization: cohort-5a`)

## 1. Job 1623 Metadata & Frame Range
- **Job ID:** `1623` (`type: "annotation"`, `mode: "annotation"`, `dimension: "2d"`, `media_type: "image"`)
- **Task ID / Project ID:** `task_id = 402`, `project_id = 159` (`task_name: null`, `project_name: null`, `organization: 1`)
- **Assignee:** `id = 245`, `username = "2A202604062"`, `first_name = "2A202604062"`, `last_name = "ACR"`
- **Status / Stage / State:** `status = "annotation"`, `stage = "annotation"`, `state = "in progress"`
- **Timestamps:** `created_date = "2026-11-16T05:30:22.801240Z"`, `updated_date = "2026-11-18T02:01:44.204818Z"`, `assignee_updated_date = "2026-11-16T05:30:28.109665Z"`
- **Issues:** `count = 0`
- **Frame Range & Count:**
  - `start_frame = 90`
  - `stop_frame = 119`
  - `frame_count = 30` (matches `meta.size = 30` and `len(meta.frames) = 30`)
  - Image filenames in `meta.frames`: `week2-human-pose/G06/G06_091.jpg` (`frame_index = 90`) through `week2-human-pose/G06/G06_120.jpg` (`frame_index = 119`)
  - Image dimensions across the 30 frames: `1280x1024` (15 frames), `960x540` (12 frames), `512x424` (3 frames)

## 2. API Access & History / Events Probe
- **`cv.task(402)` (`GET /api/tasks/402`):** **HTTP 403 Forbidden** — `{"detail":"You do not have permission to perform this action."}`
- **`GET /api/jobs/1623/annotations?org=cohort-5a`:** **HTTP 200 OK** — returns the exact same payload (`same_as_default: true`) as `cv.annotations(1623)` (`version = 0`, 28 shapes, 0 tracks, 0 tags).
- **`GET /api/events` (tested with `job_id=1623`, `task_id=402`, empty params, and `org=cohort-5a`):** **HTTP 500 Server Error** on all four queries on this CVAT instance; no server-side edit history/events log is accessible via `/api/events`.
- **`version` field in annotations:** `0` (CVAT annotation payload revision counter).

## 3. Annotation & Label Summary
- **Label Schema (`job_1623_labels.json`):**
  - 1 skeleton label: `id = 12322`, `name = "person_vf17"`, `type = "skeleton"`, `project_id = 159`
  - 17 point sublabels: `id = 12323..12339`, `name = "1".."17"`, `type = "points"`, `has_parent = true`
- **Totals in `job_1623_annotations_raw.json`:**
  - `version`: `0`
  - `shapes`: `28` (all `type = "skeleton"`; each has `17` keypoint `elements`, totaling `476` keypoint elements)
  - `tracks`: `0`
  - `tags`: `0`
- **Keypoint Flags (across 476 keypoints):**
  - `occluded = true`: `81`
  - `outside = true`: `58`
- **Annotation `source` Values:**
  - Shapes (`28/28`): `source = "manual"`
  - Keypoint elements (`476/476`): `source = "manual"`
  - No `file`, `auto`, or other `source` values present.
- **Skeleton Count per Frame (30 frames total):**
  - **0 skeletons (2 frames):** `100` (`G06_101.jpg`), `118` (`G06_119.jpg`)
  - **1 skeleton (28 frames):** `90–99`, `101–117`, `119` (`G06_091.jpg`–`G06_100.jpg`, `G06_102.jpg`–`G06_118.jpg`, `G06_120.jpg`)
  - **>1 skeletons (0 frames):** None

## 4. Local Frame Cache & SHA256 Verification
- Directory checked: `data/jobs/edufun/1623/frames/`
- All `30` frames (`G06_091.jpg`–`G06_120.jpg`) were already present locally; `0` frames needed downloading.
- SHA256 hashes (`image_hash`) computed for all 30 files and recorded in both `frame_manifest.csv` and `keypoint_mapping.json`.

## 5. Created Files
- `D:\06-Learning\AIA-VINGROUP\learning\cvat\artifacts\pose17_research\snapshots\job_1623.json`
- `D:\06-Learning\AIA-VINGROUP\learning\cvat\artifacts\pose17_research\snapshots\job_1623_meta.json`
- `D:\06-Learning\AIA-VINGROUP\learning\cvat\artifacts\pose17_research\snapshots\job_1623_labels.json`
- `D:\06-Learning\AIA-VINGROUP\learning\cvat\artifacts\pose17_research\snapshots\job_1623_annotations_raw.json`
- `D:\06-Learning\AIA-VINGROUP\learning\cvat\artifacts\pose17_research\snapshots\api_probe.json`
- `D:\06-Learning\AIA-VINGROUP\learning\cvat\artifacts\pose17_research\snapshots\keypoint_mapping.json`
- `D:\06-Learning\AIA-VINGROUP\learning\cvat\artifacts\pose17_research\frame_manifest.csv`
- `D:\06-Learning\AIA-VINGROUP\learning\cvat\artifacts\pose17_research\agents\A01_cvat_reader.md`
