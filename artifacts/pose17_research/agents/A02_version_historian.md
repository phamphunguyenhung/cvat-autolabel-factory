# A02 — Version Historian Report: Pose17 (Task 402 / Job 1623)

Generated: 2026-11-18 | Role: **A02 — Version Historian** | Scope: Read-only forensic audit of git history, `week02/task402-pose/job1623-pose17/` (`backups/`, `drafts/`, `SPEC.md`, `EDGE_CASES.md`, `push_policy.json`), `week02/issues.md`, `week02/README.md`, `weeks/guidelines/w2-face50-pose17.md`, `scripts/`, and `reports/w2_recovery/`.

---

## 1. Git History Trace (`week02`, `src/cvat_tools/pose`, `scripts/eval_pose17.py`, `weeks/`)

| Commit | Timestamp | Author | Scope & Key Changes |
|---|---|---|---|
| `c77f66e8` | 2026-11-13 18:48:48 +0700 | `cet` | Workspace init (`src/cvat_tools/pose/__init__.py` empty). |
| `138543e1` | 2026-11-16 18:40:21 +0700 | Phạm Phú Nguyễn Hưng | Added `src/cvat_tools/pose/week2.py` (331 lines, Day 4 `spm` YOLO pose + `LOW_CONF_Q=0.5`, `apply_draft`, `rollback`) and `face50.py`. |
| `3f5391cb` | 2026-11-16 18:40:21 +0700 | Phạm Phú Nguyễn Hưng | Added `week02/README.md`, `job1623-pose17/{SPEC.md, EDGE_CASES.md, push_policy.json}`, initial drafts `person17_20261116_172258.json` & `174945.json`, `weeks/2026-W47.yaml`, and pre-BTC internal guideline `weeks/guidelines/w2-face50-pose17.md` (anatomical R/L). |
| `cd129065` | 2026-11-17 11:34:44 +0700 | Phạm Phú Nguyễn Hưng | Added `src/cvat_tools/pose/person17.py` (236 lines: `yolo`, `vitpose`, `auto` consensus, `detect` 4-way rotation, `LIMB_IDX` `V0_CONF=0.3`, `enforce_image_lr`), `gold.py`, `scripts/eval_pose17.py`, `scripts/compare_drafts.py`; updated `week2.py`, `SPEC.md`, `push_policy.json`, `w2-face50-pose17.md` (aligned to BTC V1), and committed drafts through `person17_auto_20261117_102313.json`. |
| Working tree (uncommitted) | 2026-11-17 – 2026-11-18 | — | Modified: `scripts/eval_pose17.py`, `scripts/eval_face50.py`, `weeks/2026-W47.yaml`. Untracked: `week02/issues.md`, `week02/prompts/`, `scripts/w2_source_manual.py`, `scripts/w2_recovery_compare.py`, `scripts/w2_inventory.py`, `scripts/w2_qc_rules.py`, `scripts/w2_final_report.py`, etc. (`backups/`, `reports/`, `data/` are gitignored). |

---

## 2. Exact Chronology of Job 1623 Annotations, Drafts, Backups & Source Conversions

### 2.1 Initial Pre-Label (`source=file`, 10 shapes)
- **Earliest local snapshot:** `week02/task402-pose/job1623-pose17/backups/before_20261116_175014.json` (captured `2026-11-16 17:50:14`, CVAT `version=0`).
- **Contents:** `10` skeleton shapes (`label_id=12322` = `person_vf17`, 17 sublabels `1..17`), all `source="file"`, shape IDs `1163231..1163240` on frames `[91, 92, 97, 98, 103, 104, 109, 110, 115, 116]`.
- **Visibility breakdown (170 keypoints):** `140 visible`, `30 occluded`, `0 outside`.
- **Origin / Creator:** Documented in `weeks/guidelines/w2-face50-pose17.md` (§6) and `week02/issues.md` (A6) as pre-existing BTC pre-labels imported from file (`"10 frame đã có skeleton nhập từ file (source=file)... Coi đây là nháp thô"`). In the CVAT API `annotations()` backup JSON, `created_date` and `updated_date` are `null`/`None` for all shapes, and no pre-17:50 upload script exists in git. Therefore, the exact upstream user/script that imported the `source=file` shapes into CVAT prior to `2026-11-16 17:50:14` is **`history_unavailable`**.

### 2.2 Tool Drafts (`drafts/person17_*.json`) & CVAT Pushes (`backups/run_*.json`)

| Timestamp | Artifact | Pipeline / Operation | Frames & Shape Counts | Notes / Evidence |
|---|---|---|---|---|
| 2026-11-16 17:22:58 | `drafts/person17_20261116_172258.json` | Day 4 `spm` (`yolo11l-pose.pt`, `backend=None`) | 20 frames (all non-`file` frames) | 340 `visible`, 0 `occluded`, 0 `outside`. Local only. |
| 2026-11-16 17:49:45 | `drafts/person17_20261116_174945.json` | `week2.py` + `spm` (`yolo11l-pose.pt`, `LOW_CONF_Q=0.5`) | 15 frames (`[90,93-96,101-102,105,107-108,111,113-114,117,119]`) | Skipped 10 `file` frames + 5 `push_policy.json` skip frames `[99,100,106,112,118]`. 200 `visible`, 55 `occluded`. |
| 2026-11-16 17:50:15 | `backups/run_20261116_175015.json` (bk: `before_20261116_175014.json`) | **Push #1** (`apply_draft` of `174945`) | `before=10`, created `15` `auto` (`1200453..1200462, 1200633..1200637`), `after=25` | `verified: true`. |
| 2026-11-16 19:01:07 | `drafts/person17_yolo_20261116_190107.json` | `person17.py` `backend=yolo` (`yolo11l-pose.pt`) | 29 frames (f118 missing) | 381 V, 111 Q, 1 O. `rot270` on f103. |
| 2026-11-16 19:02:24 | `drafts/person17_vitpose_20261116_190224.json` | `person17.py` `backend=vitpose` (`usyd-community/vitpose-base-simple`, YOLO boxes) | 30 frames | 412 V, 96 Q, 2 O. Non-0° rot on f103, f106, f118. |
| 2026-11-16 19:51:09 | `drafts/person17_yolo_20261116_195109.json` | `person17.py` `backend=yolo` (updated rot thresholds) | 30 frames | 395 V, 114 Q, 1 O. Non-0° rot on f103, f106, f112, f113, f118. |
| 2026-11-16 19:53:27 | `drafts/person17_vitpose_20261116_195327.json` | `person17.py` `backend=vitpose` (updated rot thresholds) | 30 frames | 413 V, 95 Q, 2 O. Non-0° rot on f103, f105, f106, f112, f113, f118. |
| 2026-11-16 19:55:36 | `drafts/person17_auto_20261116_195536.json` | `person17.py` `backend=auto` (`merge_consensus` YOLO+ViTPose) | 30 frames | 393 V, 115 Q, 2 O. |
| 2026-11-16 19:57:04 | `drafts/person17_auto_20261116_195704.json` | `person17.py` `backend=auto` (`push_policy.json` updated to skip `[100,118]`) | 28 frames | Identical coords/states to `195536` on the 28 frames; 372 V, 102 Q, 2 O. |
| 2026-11-17 10:02:10 | `backups/run_20261117_100210.json` (bk: `before_20261117_100209.json`) | **Push #2** (`apply_draft --replace-auto` of `195704`) | `before=25`, deleted `15` old `auto`, created `18` `auto` (`1258145..1258154, 1258325..1258332`), `after=28` | Added f99, f106, f112. `verified: true`. |
| 2026-11-17 10:02–10:13 | *(CVAT human edit #1)* | Manual edits on CVAT | f90 (`id=1258145`), f91 (`id=1163231`) | f90 kpt 17 moved **210.56 px** (`_my_auto_status` subsequently protected f90!); f91 kpts 14,16 `occluded -> outside`. |
| 2026-11-17 10:13:16 | `drafts/person17_auto_20261117_101316.json` | `person17.py` `backend=auto` + `V0_CONF=0.3` (`outside`) | 28 frames | Same `(x,y)` as `195704`; 372 V, 33 Q, 71 O (applied `v0` across all keypoints including ears 4/5). |
| 2026-11-17 10:13:54 | `backups/run_20261117_101354.json` (bk: `before_20261117_101353.json`) | **Push #3** (`apply_draft --replace-auto` of `101316`) | `before=28`, deleted `17` `auto` (`1258146..1258332`), created `17` `auto` (`1258741..1258927`), `after=28` | **f90 (`id=1258145`) skipped/protected** due to 210.56 px human edit. |
| 2026-11-17 10:20:28 | `drafts/person17_auto_20261117_102028.json` | `person17.py` `backend=auto` + `LIMB_IDX` restriction | 28 frames | Ears (4, 5) no longer set to `outside`: 372 V, 40 Q, 64 O. |
| 2026-11-17 10:23:13 | `drafts/person17_auto_20261117_102313.json` | `person17.py` `backend=auto` + `enforce_image_lr` flags | 28 frames | Same `(x,y)` & states as `102028`; added `UNCERTAIN_CLASS_LR` flags on f96, f103, f105, f106, f110, f112. |
| 2026-11-17 10:23:37 | `backups/run_20261117_102337.json` (bk: `before_20261117_102335.json`) | **Push #4** (`apply_draft --replace-auto` of `102313`) | `before=28`, deleted `17` `auto` (`1258741..1258927`), created `17` `auto` (`1259299..1259485`), `after=28` | f90 (`id=1258145`) remained protected. |
| 2026-11-17 10:23–19:29 | *(CVAT human edit #2)* | Manual edit on CVAT | f91 (`id=1163231`, `source=file`) | f91 kpt 5 moved 0.44 px, kpt 13 moved 6.45 px. |

### 2.3 What Happened on 17/11 Evening (`source=file`/`auto` -> `source=manual`) & Post-19:46 Anomaly
1. **19:22:00:** `reports/w2_current/job1623.json` recorded 28 frames (`source=file` on the 10 pre-label frames, `source=auto` on the 18 tool frames).
2. **19:29:10 (`w2_source_manual.py --from-source file --yes`):**
   - Backed up the `10` `source=file` shapes (`1163231..1163240`) into `backups/before_manual_20261117_192910.json` (list of 10 shapes).
   - Recreated them with `source="manual"` (`1319662..1319671`), preserving coordinates/states, and deleted the old `file` IDs. *(Note: no `after_manual_20261117_192910.json` file exists on disk.)*
3. **19:30:49 (`w2_source_manual.py --from-source auto --yes`):**
   - Backed up the `18` `source=auto` shapes (`1258145` on f90 + `1259299..1259485` on the 17 Push #4 frames) into `backups/before_manual_20261117_193049.json` (list of 18 shapes).
   - Recreated them with `source="manual"` (`1320579..1320596`), deleted the old `auto` IDs, and logged `created_ids`/`deleted_ids` (no coordinates) in `backups/after_manual_20261117_193049.json`.
   - **Consequence (`issues.md` A8/F10):** Shape IDs changed, breaking `cvat-tools pose rollback --run` (which keys on `run_*.json` `created_ids`).
4. **19:46:57 (`reports/w2_inventory_1623.csv`):** Live read from CVAT confirmed `28` shapes across 28 frames, `sources="manual:1"` on every labeled frame (`0` `source=file`, `0` `source=auto`), f100 and f118 empty.
5. **Between 17/11 19:46:57 and 18/11 08:24:15 (`reports/w2_recovery/snapshots/live_1623_20261118_082415.json`):**
   - Live CVAT snapshot (`version=0`) shows **29 shapes**: all `28` `source=manual` shapes (`1319662..1319671`, `1320579..1320596`, identical `0.0 px` to `before_manual_*`), **PLUS** the original `source=file` shape **`id=1163232` on frame 92**, now containing **5 human-edited keypoints** (35.55 px to 193.12 px delta vs `before_manual_20261117_192910.json`). Frame 92 currently has **duplicate skeletons** (`id=1319663` `manual` + `id=1163232` `file`).

---

## 3. The Three Distinct Version Axes

| Axis | Versions Observed (with Direct Evidence) |
|---|---|
| **1. Annotation Version** | **(a) Initial Pre-label (`source=file`)**: 10 shapes (`1163231..1163240`) in `before_20261116_175014.json` (140 V, 30 Q, 0 O).<br>**(b) Tool Drafts on CVAT (`source=auto`)**: 15 shapes (`run_20261116_175015`) -> 18 shapes (`run_20261117_100210`) -> 17 replaced + f90 human-edited (`run_20261117_101354`, `run_20261117_102337`).<br>**(c) Source-Converted `source=manual` (pre-human-review)**: 28 shapes (`1319662..1319671`, `1320579..1320596`) created at `19:29:10`/`19:30:49` on 17/11 (`issues.md` A6/A8 explicitly notes `source=manual` does NOT mean human-approved).<br>**(d) Live CVAT State with Partial Human Edits (`live_1623_20261118_082415.json`)**: 29 shapes (28 `manual` + duplicate `file` `id=1163232` on f92); contains unverified human edits on f90 (kpt 17), f91 (kpts 5, 13, 14, 16), and f92 `id=1163232` (kpts 1, 9, 11, 16, 17). Gold count = 0 (`eval_pose17.py`, `issues.md` B5). |
| **2. Guideline Version** | **(a) Pre-BTC Internal Draft (16/11/2026, commit `3f5391cb`)**: `weeks/guidelines/w2-face50-pose17.md` & `SPEC.md` ("Tự viết, chưa phải bản chính thức của BTC"); used **anatomical R/L** ("Trái/phải theo người"), no `v0` limb policy.<br>**(b) BTC V1 (`HumanPose17_Annotation_Guideline_V1.docx`) + Internal G06 Update (17/11/2026, commit `cd129065`, `issues.md`)**: **Image-relative R/L** (even=R=image right, odd=L=image left, even when rotated 90°), `outside` (`v0`) for limbs that cannot be inferred, face/shoulders/hips always V or Q, ±5 px (V) / ±20 px (Q) tolerances, skip if no driver, issue workflow (`UNCERTAIN_CLASS`, etc.). |
| **3. Tool / Pipeline Version** | **(a) Day 4 `spm` (`week2.py` commit `138543e1`)**: `yolo11l-pose.pt` only, `LOW_CONF_Q=0.5`, no rotation, no consensus (`person17_20261116_172258`, `174945`).<br>**(b) `person17.py` Single-Model (`yolo` / `vitpose`, 16/11 19:01–19:53)**: `yolo11l-pose.pt` or `usyd-community/vitpose-base-simple` (YOLO boxes), 4-way orientation `detect()`.<br>**(c) `person17.py` `auto` Consensus (16/11 19:55–19:57)**: `merge_consensus` (`AGREE_FRAC=0.35`, `DISAGREE_CONF=0.4`) + `push_policy` skipping `[100,118]`.<br>**(d) `person17.py` BTC-V1 Aligned (17/11 10:13–10:23, commit `cd129065`)**: `101316` added `V0_CONF=0.3` globally -> `102028` restricted `V0_CONF` to `LIMB_IDX` (`{7,8,9,10,13,14,15,16}`) -> `102313` added `enforce_image_lr` (`UNCERTAIN_CLASS_LR` flags). |

---

## 4. Exact Per-Keypoint Deltas Across Local Snapshots

Full machine-readable JSON saved to [A02_deltas.json](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/agents/A02_deltas.json).

> **Important structural note on snapshot pairs:**
> - `before_20261116_175014.json` contains **10 frames** (`source=file`: 91, 92, 97, 98, 103, 104, 109, 110, 115, 116).
> - `before_manual_20261117_193049.json` contains **18 disjoint frames** (`source=auto`: 90, 93–96, 99, 101–102, 105–108, 111–114, 117, 119), so it has **0 overlapping frames** with `before_20261116_175014.json` (its counterpart for the 10 `file` frames is `before_manual_20261117_192910.json`).
> - `after_manual_20261117_193049.json` stores only `created_ids` and `deleted_ids` (no coordinates); post-conversion coordinates reside in `reports/w2_recovery/snapshots/live_1623_20261118_082415.json`.

### 4.1 `before_20261116_175014.json` vs `before_manual_20261117_192910.json` (10 `source=file` frames)
9 frames (92, 97, 98, 103, 104, 109, 110, 115, 116) have **0.0 px** and **0 visibility** changes. Only **frame 91 (`id=1163231`)** changed:

| Frame | Keypoint | `dx` (px) | `dy` (px) | Euclidean (px) | `visibility_before` | `visibility_after` | When Observed |
|---:|---|---:|---:|---:|---|---|---|
| 91 | `5` (ear L) | +0.1396 | -0.4182 | 0.4409 | `visible` | `visible` | 10:23:35 → 19:29:10 |
| 91 | `13` (hip L) | -5.7651 | +2.8828 | 6.4457 | `visible` | `visible` | 10:23:35 → 19:29:10 |
| 91 | `14` (knee R) | 0.0000 | 0.0000 | 0.0000 | `occluded` | `outside` | 10:02:09 → 10:13:53 |
| 91 | `16` (ankle R) | 0.0000 | 0.0000 | 0.0000 | `occluded` | `outside` | 10:02:09 → 10:13:53 |

### 4.2 `person17_auto_20261117_102313.json` vs `before_manual_20261117_193049.json` (18 `source=auto` frames)
- **17 Push #4 frames** (93–96, 99, 101–102, 105–108, 111–114, 117, 119): **0.00 px** coordinate diff beyond `round(..., 2)` serialization (`<= 0.007 px`), **0 visibility changes**.
- **Frame 90** (protected from Push #3 and #4, still holding `person17_auto_20261116_195704.json` + human edit #1):

| Frame | Keypoint | `dx` (px) | `dy` (px) | Euclidean (px) | `visibility_before` (`102313`) | `visibility_after` (`193049`) |
|---:|---|---:|---:|---:|---|---|
| 90 | `14` (knee R) | -0.0018 | +0.0017 | 0.0024 | `outside` | `occluded` |
| 90 | `17` (ankle L) | +210.4359 | +7.2030 | **210.5592** | `outside` | `occluded` |

*(Other 15 keypoints on f90 differ by `<= 0.007 px` rounding only.)*

### 4.3 `before_manual_20261117_192910.json` + `193049.json` vs `live_1623_20261118_082415.json`
- **All 28 `source=manual` shapes** in `live_1623_20261118_082415.json`: **0.0000 px** and **0 visibility** diffs vs `before_manual_20261117_192910.json` (10 shapes) and `before_manual_20261117_193049.json` (18 shapes).
- **Duplicate `source=file` shape `id=1163232` on frame 92** in `live_1623_20261118_082415.json` vs `before_manual_20261117_192910.json` (and vs `before_20261116_175014.json`, identical):

| Frame | Keypoint | `dx` (px) | `dy` (px) | Euclidean (px) | `visibility_before` | `visibility_after` |
|---:|---|---:|---:|---:|---|---|
| 92 | `1` (nose) | -20.4580 | -29.0700 | 35.5470 | `visible` | `visible` |
| 92 | `9` (elbow L) | +4.9205 | -101.2275 | 101.3470 | `occluded` | `occluded` |
| 92 | `11` (wrist L) | +55.0328 | -185.1156 | **193.1228** | `occluded` | `outside` |
| 92 | `16` (ankle R) | +55.8336 | +53.9719 | 77.6553 | `occluded` | `occluded` |
| 92 | `17` (ankle L) | -8.3750 | +101.4299 | 101.7751 | `occluded` | `occluded` |

### 4.4 Intermediate Pipeline State Transitions (`101353 -> 102335 -> 193049`)
- **`before_20261117_101353.json -> before_20261117_102335.json`** (reflects Push #3 `101316` vs Push #2 `195704` on the 17 non-f90 `auto` frames): `0.0 px` on all keypoints; **40 keypoints** changed `occluded -> outside` (limbs `14–17` plus ears `4` on f93/f105/f112/f117 and `5` on f106).
- **`before_20261117_102335.json -> before_manual_20261117_193049.json`** (reflects Push #4 `102313` vs Push #3 `101316`): `0.0 px` on all keypoints; **5 ear keypoints** reverted `outside -> occluded` (`f93:4`, `f105:4`, `f106:5`, `f112:4`, `f117:4`) due to `LIMB_IDX`.

### 4.5 Pre-label (`before_20261116_175014.json`) vs Final Auto Draft (`person17_auto_20261117_102313.json`) on the 10 Pre-label Frames
All 10 pre-label frames differ substantially between BTC `source=file` and `person17_auto_20261117_102313.json` (mean Euclidean deltas per frame range from **17.61 px** on f109 to **95.63 px** on f110; max single-keypoint delta **421.76 px** on f97), plus systematic `occluded/visible -> outside` shifts on knees/ankles (`14–17`). Detailed per-keypoint rows are in [A02_deltas.json](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/agents/A02_deltas.json) (`10_before_1116_175014_vs_draft_1117_102313_10_prelabel_frames`).
