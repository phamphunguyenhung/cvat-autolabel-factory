# A06 — Geometry Auditor Report: Job 1623 (`person_vf17`)

**Task:** Pose17 Gold Reference & Guideline Engine | **Role:** A06 — Geometry Auditor | **Date:** 2026-11-18

## 1. Executive Summary

- **Scope audited:** `artifacts/pose17_research/snapshots/job_1623_annotations_raw.json` (`28` skeletons, `476` keypoints across frames `90–119`, missing `[100, 118]`) against `artifacts/pose17_research/snapshots/job_1623_meta.json`.
- **Visibility breakdown:** `359` `visible` (75.4%), `59` `occluded` (12.4%), `58` `outside` (12.2%).

| Check | Result | Count | Key Finding |
|---|---|---:|---|
| **1a. Coordinate Bounds (`[0, W] x [0, H]`)** | PASS | `0` | `0` `visible`/`occluded` (and `0` `outside`) points out of bounds |
| **1b. Overlapping Keypoints (`< 3.0 px`)** | WARN | `0` vis-vis / `1` vis-occ | **Frame 101**: `kpt 2 (eye_R, visible)` & `kpt 4 (ear_R, occluded)` only **`0.27 px`** apart |
| **1c. Normalized Bone Lengths** | WARN | `1` | **Frame 114**: `forearm_R (8-10)` = `48.83 px` (**`0.139x` torso**, `< 0.15x` threshold) after human moved `kpt 8` by `65.31 px` |
| **1d. Image Left/Right (`x_R > x_L`)** | INFO / WARN | `0` upright / `44` rotated (`4` body-aligned) | **0** inversions on 13 upright frames; **44** raw `x`-inversions on 15 horizontal/lying frames, of which **40** are pure 90°/270° rotation artifacts and **4** persist in torso frame (`f93` knees `14-15`, `f110/f112/f113` wrists `10-11`) |
| **1e. Acute Angles (`< 15°`), Reversals, Crossings** | INFO / WARN | `20` shoulder-torso / `0` joint / `0` reversals / `29` crossings | `0` elbow/knee `< 15°`; `0` limb reversals; `0` torso twists; `29` forearm-vs-torso/thigh/arm crossings across `18` frames (`f113` has 4 crossings + `0.872x` forearm) |
| **2. Live Human-Edit Deltas (`17/11 19:30` & `18/11 08:24` → `09:17`)** | CHANGED | `25 / 28` frames | Duplicate `1163232` on `f92` deleted; **25 frames** edited between `08:24:15` and `09:17` (`148` kpt moves, `51` vis changes); only `f90, f91, f95` untouched |

## 2. Geometry Audit Details (`job_1623_annotations_raw.json`)

### 2.1 (1a) Coordinate Bounds
- **0 violations** across all 476 keypoints (`visible`, `occluded`, and `outside` all lie strictly within `[0, W] x [0, H]`).

### 2.2 (1b) Overlapping / Duplicate Keypoints (`dist < 3.0 px`)
- **`visible` vs `visible` (`< 3.0 px`):** `0` pairs.
- **`visible` vs `occluded` (`< 3.0 px`):** `1` pair:
  - **Frame 101** (`week2-human-pose/G06/G06_102.jpg`, shape `1320585`): `kpt 2 eye_R (anat left_eye)` (visible, `[264.63, 140.7]`) vs `kpt 4 ear_R (anat left_ear)` (occluded, `[264.88, 140.79]`) → **`0.2657 px`**.

### 2.3 (1c) Bone Length Normalization & Outliers
- All 28 skeletons had non-`outside` shoulders `(6,7)` and hips `(12,13)`, so **100% of frames** were normalized by `torso_height = dist(mid(6,7), mid(12,13))`.

| Bone Group | N | Min (`x torso`) | Median (`x torso`) | Mean (`x torso`) | Max (`x torso`) |
|---|---:|---:|---:|---:|---:|
| `upper_arm` | 55 | 0.3009 | 0.6322 | 0.6321 | 1.0308 |
| `forearm` | 53 | 0.1390 | 0.4669 | 0.4942 | 0.9301 |
| `thigh` | 50 | 0.3048 | 0.7560 | 0.7751 | 1.1736 |
| `calf` | 17 | 0.1807 | 0.4504 | 0.4786 | 0.8315 |
| `shoulder_width` | 28 | 0.4621 | 0.7695 | 0.7865 | 1.4986 |
| `hip_width` | 28 | 0.3276 | 0.5073 | 0.5015 | 0.7676 |

**Statistical Outliers (`> 2.5x group median` or `< 0.15x torso`):**
- **Frame 114** (`week2-human-pose/G06/G06_115.jpg`): `forearm_R` (`8-10`, `visible -> occluded`) = **`48.826 px`** = **`0.139x` torso** (torso `351.279 px`; group median `0.4669`; flags: `<0.15x_norm_ref`).

**Notable Borderline / Foreshortened Segments (informational, within threshold):**
- Long segments (`1.80x–1.99x` group median): `f91 forearm_R` (`0.9301`, `1.99x` med), `f92 shoulder_width` (`1.4986`, `1.95x` med — close-up/foreshortened torso), `f113 forearm_L` (`0.8716`, `1.87x` med), `f98 calf_R` (`0.8315`, `1.85x` med), `f110 forearm_L` (`0.8414`, `1.80x` med).
- Short segments (`0.15x–0.20x` torso): `f93 forearm_R` (`0.162`, both `occluded`), `f108 forearm_R` (`0.172`), `f109 forearm_R` (`0.163`), `f111 forearm_R` (`0.172`, `kpt 10 occluded`), `f105 calf_L` (`0.181`, `kpt 17 occluded`).

### 2.4 (1d) Image-Based Left/Right (`R even > L odd` in `x`)
- **Upright frames (13):** `[90, 91, 92, 94, 95, 99, 102, 107, 109, 111, 114, 116, 119]` → **`0` L/R `x`-inversions**.
- **Horizontal/rotated frames (15):** `[93, 96, 97, 98, 101, 103, 104, 105, 106, 108, 110, 112, 113, 115, 117]` (torso tilt `66.3°–87.3°` from vertical; `|dy| > |dx|` on shoulder/eye pairs) → **`44` raw `x_even <= x_odd` pairs**.
  - `13` frames have head on the left (`93, 96, 97, 98, 101, 103, 104, 105, 108, 112, 113, 115, 117`), where image-aligned `R` sits **above** `L` (`y_R < y_L`).
  - `2` frames have head on the right (`106, 110`), where image-aligned `R` sits **below** `L` (`y_R > y_L`).
- **Torso-axis-aligned R/L verification** (projecting `R - L` onto `90° CW` from `mid_hip -> mid_shoulder`): eliminates `40 / 44` rotation artifacts, leaving **only `4` genuine R/L crossings/swaps** across all 28 skeletons:

| Frame | Image | Pair | Vis (`R`, `L`) | Body-Aligned `R-L` (px) | Raw `dx`, `dy` (px) | Assessment |
|---:|---|---|---|---|---|---|
| 93 | `week2-human-pose/G06/G06_094.jpg` | `(14, 15)` | `occluded`, `occluded` | `-69.35` | `-61.78`, `51.51` | Suspected occluded knee swap or crossed legs |
| 110 | `week2-human-pose/G06/G06_111.jpg` | `(10, 11)` | `visible`, `visible` | `-75.42` | `275.0`, `-56.6` | Crossed wrists in front of body |
| 112 | `week2-human-pose/G06/G06_113.jpg` | `(10, 11)` | `occluded`, `visible` | `-2.34` | `-13.59`, `-1.07` | Wrists nearly overlapping/crossed |
| 113 | `week2-human-pose/G06/G06_114.jpg` | `(10, 11)` | `visible`, `visible` | `-134.39` | `52.69`, `146.75` | Crossed arms vs wrist L/R swap (paired with 4 self-crossings & 0.872x forearm_L) |

### 2.5 (1e) Acute Angles (`< 15°`), Limb Reversals, and Self-Crossings
- **Elbow & knee acute angles (`< 15°`):** **`0`**. (All `20` angles `< 15°` are shoulder-to-torso angles `12-6-8` / `13-7-9` ranging `1.60°–13.99°`, representing arms hanging naturally beside the torso.)
- **Limb chain reversals:** **`0`**.
- **Self-crossing segments:** **`29`** intersections across **`18` frames** (`[91, 93, 96, 97, 98, 99, 101, 102, 104, 105, 106, 110, 111, 112, 113, 114, 115, 117]`).
  - **`0` torso twists** (`6-12` never crosses `7-13`; `6-7` never crosses `12-13`).
  - All `29` intersections involve a `forearm` (`8-10` or `9-11`) crossing `torso_R`, `torso_L`, `hip_bar`, `thigh`, or `upper_arm_R` (notably **Frame 113** has 4 crossings involving `forearm_R` and `forearm_L`).

## 3. Exact Live Human-Edit Deltas

### 3.1 Snapshot Reconciliation (`before_manual` → `live_082415` → `job_1623_raw_0917`)
- Comparing `before_manual_20261117_192910.json` (10 `file` shapes) + `before_manual_20261117_193049.json` (18 `auto` shapes) against `live_1623_20261118_082415.json` (29 shapes) and `job_1623_annotations_raw.json` (28 shapes):
  1. All `28` `source=manual` shapes in `live_1623_20261118_082415.json` (`1319662..1319671`, `1320579..1320596`) were **100% identical (`0.0 px`, identical visibility)** to `before_manual_*`.
  2. Between `2026-11-18 08:24:15` and `09:17`, the duplicate `source=file` shape `1163232` on **Frame 92** was **deleted**, and human edits were applied directly to the `source=manual` shapes across **25 frames** (`92, 93, 94, 96, 97, 98, 99, 101–117, 119`).
  3. Only **3 frames** (`90, 91, 95`) remained completely untouched (`0` coord changes, `0` vis changes).
  4. Totals across the 28 matched skeletons (`before_manual` → `raw_0917`): **`148` keypoints moved**, **`51` visibility transitions**.

### 3.2 Frame 92 Duplicate Resolution (`live_082415` → `raw_0917`)
- In `live_082415`, Frame 92 had 2 shapes: `1319663 (manual)` (unedited) and `1163232 (file)` (5 kpts edited). By `raw_0917`, `1163232` was deleted and `1319663 (manual)` was edited on 4 keypoints:
  - `kpt 10 wrist_R (anat left_wrist)`: `dx=+43.60, dy=+56.06` (`dist=71.02 px`), `vis: occluded -> outside`
  - `kpt 11 wrist_L (anat right_wrist)`: `dx=+0.00, dy=+0.00` (`dist=0.00 px`), `vis: occluded -> outside`
  - `kpt 16 ankle_R (anat left_ankle)`: `dx=+41.11, dy=+36.13` (`dist=54.73 px`), `vis: occluded -> occluded`
  - `kpt 17 ankle_L (anat right_ankle)`: `dx=+1.25, dy=+88.45` (`dist=88.46 px`), `vis: occluded -> occluded`

### 3.3 Exact Per-Keypoint Edits Across All 25 Modified Frames (`before_manual` → `job_1623_raw_0917`)

> **Note on whole-skeleton micro-drags:** On 5 frames (`104, 106, 108, 114, 116`), dragging the skeleton shifted all 17 keypoints by a uniform sub-pixel offset (`0.12–0.50 px`). Those uniform-offset keypoints with unchanged visibility are summarized per frame below; all substantive edits (`dist >= 1.0 px` or visibility change) are listed individually. Every single keypoint delta is stored in `A06_geometry_metrics.json`.

| Frame | Shape ID (`before → after`) | Keypoint | `dx` (px) | `dy` (px) | `dist` (px) | Visibility (`before → after`) |
|---:|---|---|---:|---:|---:|---|
| 92 | `1163232 → 1319663` | `10` wrist_R (anat left_wrist) | `+43.60` | `+56.06` | `71.02` | `occluded → outside` |
| 92 | `1163232 → 1319663` | `11` wrist_L (anat right_wrist) | `+0.00` | `+0.00` | `0.00` | `occluded → outside` |
| 92 | `1163232 → 1319663` | `16` ankle_R (anat left_ankle) | `+41.11` | `+36.13` | `54.73` | `occluded → occluded` |
| 92 | `1163232 → 1319663` | `17` ankle_L (anat right_ankle) | `+1.25` | `+88.45` | `88.46` | `occluded → occluded` |
| 93 | `1259299 → 1320580` | ` 1` nose | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 93 | `1259299 → 1320580` | ` 2` eye_R (anat left_eye) | `-0.66` | `+8.85` | `8.88` | `visible → outside` |
| 93 | `1259299 → 1320580` | ` 3` eye_L (anat right_eye) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 93 | `1259299 → 1320580` | ` 5` ear_L (anat right_ear) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 93 | `1259299 → 1320580` | ` 6` shoulder_R (anat left_shoulder) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 93 | `1259299 → 1320580` | ` 7` shoulder_L (anat right_shoulder) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 93 | `1259299 → 1320580` | ` 8` elbow_R (anat left_elbow) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 93 | `1259299 → 1320580` | ` 9` elbow_L (anat right_elbow) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 93 | `1259299 → 1320580` | `10` wrist_R (anat left_wrist) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 93 | `1259299 → 1320580` | `11` wrist_L (anat right_wrist) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 93 | `1259299 → 1320580` | `12` hip_R (anat left_hip) | `-14.46` | `-23.67` | `27.74` | `visible → occluded` |
| 93 | `1259299 → 1320580` | `13` hip_L (anat right_hip) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 93 | `1259299 → 1320580` | `14` knee_R (anat left_knee) | `-40.84` | `+53.56` | `67.36` | `occluded → occluded` |
| 94 | `1259300 → 1320581` | `10` wrist_R (anat left_wrist) | `+29.76` | `-13.67` | `32.75` | `visible → visible` |
| 96 | `1259302 → 1320583` | `12` hip_R (anat left_hip) | `-22.82` | `-18.26` | `29.23` | `visible → visible` |
| 96 | `1259302 → 1320583` | `14` knee_R (anat left_knee) | `+0.00` | `+0.00` | `0.00` | `occluded → outside` |
| 97 | `1163233 → 1319664` | ` 2` eye_R (anat left_eye) | `-0.00` | `+6.87` | `6.87` | `visible → visible` |
| 97 | `1163233 → 1319664` | ` 3` eye_L (anat right_eye) | `+0.24` | `+7.10` | `7.11` | `visible → visible` |
| 97 | `1163233 → 1319664` | ` 5` ear_L (anat right_ear) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 97 | `1163233 → 1319664` | `12` hip_R (anat left_hip) | `-5.33` | `-33.47` | `33.89` | `visible → visible` |
| 97 | `1163233 → 1319664` | `14` knee_R (anat left_knee) | `-4.57` | `-29.67` | `30.02` | `visible → visible` |
| 97 | `1163233 → 1319664` | `16` ankle_R (anat left_ankle) | `+0.00` | `+0.00` | `0.00` | `occluded → outside` |
| 97 | `1163233 → 1319664` | `17` ankle_L (anat right_ankle) | `-47.16` | `-30.43` | `56.13` | `occluded → occluded` |
| 98 | `1163234 → 1319665` | ` 4` ear_R (anat left_ear) | `+5.45` | `-75.31` | `75.51` | `occluded → outside` |
| 99 | `1259303 → 1320584` | `12` hip_R (anat left_hip) | `+73.19` | `-23.32` | `76.81` | `visible → visible` |
| 101 | `1259304 → 1320585` | `12` hip_R (anat left_hip) | `-28.54` | `-31.39` | `42.42` | `visible → visible` |
| 101 | `1259304 → 1320585` | `14` knee_R (anat left_knee) | `-13.00` | `-67.53` | `68.77` | `visible → visible` |
| 101 | `1259304 → 1320585` | `15` knee_L (anat right_knee) | `-12.05` | `-54.22` | `55.54` | `visible → visible` |
| 101 | `1259304 → 1320585` | `16` ankle_R (anat left_ankle) | `+54.53` | `-147.43` | `157.20` | `occluded → visible` |
| 102 | `1259305 → 1320586` | ` 4` ear_R (anat left_ear) | `+0.87` | `+30.71` | `30.72` | `occluded → occluded` |
| 102 | `1259305 → 1320586` | `14` knee_R (anat left_knee) | `+35.53` | `-46.30` | `58.36` | `visible → visible` |
| 102 | `1259305 → 1320586` | `15` knee_L (anat right_knee) | `+5.38` | `+6.46` | `8.41` | `visible → visible` |
| 103 | `1163235 → 1319666` | ` 2` eye_R (anat left_eye) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 103 | `1163235 → 1319666` | ` 4` ear_R (anat left_ear) | `+0.00` | `+0.00` | `0.00` | `visible → outside` |
| 103 | `1163235 → 1319666` | `14` knee_R (anat left_knee) | `-4.24` | `-11.17` | `11.95` | `occluded → visible` |
| 103 | `1163235 → 1319666` | `16` ankle_R (anat left_ankle) | `+85.15` | `-20.81` | `87.66` | `occluded → occluded` |
| 103 | `1163235 → 1319666` | `17` ankle_L (anat right_ankle) | `-12.71` | `-92.09` | `92.96` | `occluded → occluded` |
| 104 | `1163236 → 1319667` | ` 2` eye_R (anat left_eye) | `+1.27` | `-3.70` | `3.91` | `visible → visible` |
| 104 | `1163236 → 1319667` | ` 3` eye_L (anat right_eye) | `-0.46` | `-7.75` | `7.76` | `visible → visible` |
| 104 | `1163236 → 1319667` | ` 4` ear_R (anat left_ear) | `+4.98` | `-2.54` | `5.59` | `visible → outside` |
| 104 | `1163236 → 1319667` | *Micro-drag kpts `[1,5,6,7,8,9,10,11,12,13,14,15,16,17]`* | `-0.00` | `-0.12` | `0.12` | *(unchanged)* |
| 105 | `1259306 → 1320587` | ` 2` eye_R (anat left_eye) | `+16.70` | `+1.20` | `16.74` | `visible → visible` |
| 105 | `1259306 → 1320587` | ` 3` eye_L (anat right_eye) | `+9.20` | `-4.50` | `10.24` | `visible → visible` |
| 105 | `1259306 → 1320587` | ` 4` ear_R (anat left_ear) | `+28.90` | `+1.30` | `28.93` | `occluded → outside` |
| 105 | `1259306 → 1320587` | ` 5` ear_L (anat right_ear) | `-11.01` | `-8.87` | `14.14` | `visible → visible` |
| 105 | `1259306 → 1320587` | ` 8` elbow_R (anat left_elbow) | `+32.81` | `+42.60` | `53.77` | `visible → occluded` |
| 105 | `1259306 → 1320587` | `14` knee_R (anat left_knee) | `-9.79` | `-55.26` | `56.12` | `visible → visible` |
| 105 | `1259306 → 1320587` | `15` knee_L (anat right_knee) | `+13.81` | `-49.50` | `51.39` | `visible → visible` |
| 106 | `1259307 → 1320588` | ` 2` eye_R (anat left_eye) | `+7.73` | `+8.18` | `11.25` | `visible → visible` |
| 106 | `1259307 → 1320588` | ` 3` eye_L (anat right_eye) | `-0.00` | `+0.45` | `0.45` | `visible → outside` |
| 106 | `1259307 → 1320588` | ` 5` ear_L (anat right_ear) | `-0.00` | `+0.45` | `0.45` | `occluded → outside` |
| 106 | `1259307 → 1320588` | *Micro-drag kpts `[1,4,6,7,8,9,10,11,12,13,14,15,16,17]`* | `-0.00` | `+0.45` | `0.45` | *(unchanged)* |
| 107 | `1259308 → 1320589` | ` 4` ear_R (anat left_ear) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 107 | `1259308 → 1320589` | `14` knee_R (anat left_knee) | `+1.83` | `-26.78` | `26.84` | `visible → visible` |
| 108 | `1259479 → 1320590` | ` 2` eye_R (anat left_eye) | `+3.23` | `+3.32` | `4.63` | `visible → visible` |
| 108 | `1259479 → 1320590` | ` 3` eye_L (anat right_eye) | `+2.61` | `+3.11` | `4.06` | `visible → visible` |
| 108 | `1259479 → 1320590` | ` 4` ear_R (anat left_ear) | `+3.03` | `+7.46` | `8.06` | `visible → occluded` |
| 108 | `1259479 → 1320590` | ` 8` elbow_R (anat left_elbow) | `+27.71` | `+0.57` | `27.71` | `visible → visible` |
| 108 | `1259479 → 1320590` | `12` hip_R (anat left_hip) | `-19.90` | `-47.26` | `51.28` | `visible → visible` |
| 108 | `1259479 → 1320590` | `13` hip_L (anat right_hip) | `+12.44` | `-50.74` | `52.25` | `visible → visible` |
| 108 | `1259479 → 1320590` | `14` knee_R (anat left_knee) | `+33.33` | `-53.23` | `62.81` | `occluded → visible` |
| 108 | `1259479 → 1320590` | `15` knee_L (anat right_knee) | `-0.50` | `-0.00` | `0.50` | `occluded → visible` |
| 108 | `1259479 → 1320590` | *Micro-drag kpts `[1,5,6,7,9,10,11,16,17]`* | `-0.50` | `-0.00` | `0.50` | *(unchanged)* |
| 109 | `1163237 → 1319668` | ` 2` eye_R (anat left_eye) | `+3.04` | `+4.06` | `5.07` | `visible → visible` |
| 109 | `1163237 → 1319668` | ` 3` eye_L (anat right_eye) | `+3.80` | `-2.54` | `4.57` | `visible → visible` |
| 109 | `1163237 → 1319668` | ` 4` ear_R (anat left_ear) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 109 | `1163237 → 1319668` | `12` hip_R (anat left_hip) | `+31.11` | `-2.83` | `31.24` | `visible → visible` |
| 109 | `1163237 → 1319668` | `16` ankle_R (anat left_ankle) | `+225.89` | `+63.10` | `234.54` | `occluded → outside` |
| 109 | `1163237 → 1319668` | `17` ankle_L (anat right_ankle) | `+21.83` | `+30.28` | `37.33` | `occluded → occluded` |
| 110 | `1163238 → 1319669` | ` 2` eye_R (anat left_eye) | `+4.40` | `+11.45` | `12.26` | `visible → visible` |
| 110 | `1163238 → 1319669` | ` 3` eye_L (anat right_eye) | `-4.99` | `-4.40` | `6.65` | `visible → visible` |
| 110 | `1163238 → 1319669` | ` 4` ear_R (anat left_ear) | `+17.61` | `+2.11` | `17.73` | `visible → occluded` |
| 110 | `1163238 → 1319669` | ` 5` ear_L (anat right_ear) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 110 | `1163238 → 1319669` | `16` ankle_R (anat left_ankle) | `-251.35` | `-185.62` | `312.46` | `occluded → outside` |
| 110 | `1163238 → 1319669` | `17` ankle_L (anat right_ankle) | `-124.76` | `-34.69` | `129.49` | `occluded → outside` |
| 111 | `1259480 → 1320591` | ` 4` ear_R (anat left_ear) | `+2.26` | `+17.83` | `17.98` | `occluded → occluded` |
| 111 | `1259480 → 1320591` | `10` wrist_R (anat left_wrist) | `+0.00` | `+0.00` | `0.00` | `visible → occluded` |
| 111 | `1259480 → 1320591` | `12` hip_R (anat left_hip) | `-27.70` | `+36.66` | `45.95` | `visible → visible` |
| 111 | `1259480 → 1320591` | `14` knee_R (anat left_knee) | `+107.54` | `+3.26` | `107.59` | `occluded → occluded` |
| 112 | `1259481 → 1320592` | `10` wrist_R (anat left_wrist) | `-4.72` | `-2.36` | `5.28` | `visible → occluded` |
| 112 | `1259481 → 1320592` | `14` knee_R (anat left_knee) | `+5.74` | `+33.06` | `33.55` | `occluded → occluded` |
| 113 | `1259482 → 1320593` | ` 4` ear_R (anat left_ear) | `+17.00` | `+3.11` | `17.29` | `occluded → occluded` |
| 113 | `1259482 → 1320593` | `14` knee_R (anat left_knee) | `-24.94` | `-43.43` | `50.08` | `visible → visible` |
| 113 | `1259482 → 1320593` | `15` knee_L (anat right_knee) | `-24.38` | `-55.72` | `60.82` | `visible → visible` |
| 114 | `1259483 → 1320594` | ` 2` eye_R (anat left_eye) | `+4.24` | `+7.01` | `8.19` | `visible → visible` |
| 114 | `1259483 → 1320594` | ` 4` ear_R (anat left_ear) | `+9.88` | `+11.39` | `15.08` | `occluded → occluded` |
| 114 | `1259483 → 1320594` | ` 8` elbow_R (anat left_elbow) | `+35.92` | `-54.54` | `65.31` | `visible → visible` |
| 114 | `1259483 → 1320594` | `10` wrist_R (anat left_wrist) | `+0.45` | `-0.00` | `0.45` | `visible → occluded` |
| 114 | `1259483 → 1320594` | *Micro-drag kpts `[1,3,5,6,7,9,11,12,13,14,15,16,17]`* | `+0.45` | `-0.00` | `0.45` | *(unchanged)* |
| 115 | `1163239 → 1319670` | ` 2` eye_R (anat left_eye) | `-1.00` | `+6.50` | `6.58` | `visible → visible` |
| 115 | `1163239 → 1319670` | ` 3` eye_L (anat right_eye) | `+1.68` | `+6.48` | `6.69` | `visible → visible` |
| 115 | `1163239 → 1319670` | ` 4` ear_R (anat left_ear) | `+10.70` | `+5.90` | `12.22` | `visible → occluded` |
| 115 | `1163239 → 1319670` | `14` knee_R (anat left_knee) | `-9.14` | `-28.96` | `30.37` | `visible → visible` |
| 115 | `1163239 → 1319670` | `16` ankle_R (anat left_ankle) | `-70.14` | `-137.42` | `154.29` | `occluded → occluded` |
| 116 | `1163240 → 1319671` | ` 2` eye_R (anat left_eye) | `+1.17` | `+2.64` | `2.89` | `visible → occluded` |
| 116 | `1163240 → 1319671` | ` 3` eye_L (anat right_eye) | `+11.74` | `+3.81` | `12.34` | `visible → visible` |
| 116 | `1163240 → 1319671` | ` 4` ear_R (anat left_ear) | `+141.92` | `+27.85` | `144.63` | `occluded → outside` |
| 116 | `1163240 → 1319671` | ` 6` shoulder_R (anat left_shoulder) | `+0.00` | `+0.29` | `0.29` | `visible → occluded` |
| 116 | `1163240 → 1319671` | ` 8` elbow_R (anat left_elbow) | `-0.00` | `+0.29` | `0.29` | `occluded → outside` |
| 116 | `1163240 → 1319671` | `10` wrist_R (anat left_wrist) | `-30.52` | `+16.73` | `34.81` | `occluded → outside` |
| 116 | `1163240 → 1319671` | `16` ankle_R (anat left_ankle) | `+200.79` | `+36.12` | `204.01` | `occluded → outside` |
| 116 | `1163240 → 1319671` | `17` ankle_L (anat right_ankle) | `+24.51` | `+38.94` | `46.01` | `occluded → outside` |
| 116 | `1163240 → 1319671` | *Micro-drag kpts `[1,5,7,9,11,12,13,14,15]`* | `-0.00` | `+0.29` | `0.29` | *(unchanged)* |
| 117 | `1259484 → 1320595` | ` 2` eye_R (anat left_eye) | `+0.48` | `+1.68` | `1.75` | `visible → occluded` |
| 117 | `1259484 → 1320595` | ` 4` ear_R (anat left_ear) | `+0.00` | `+0.00` | `0.00` | `occluded → outside` |
| 117 | `1259484 → 1320595` | ` 8` elbow_R (anat left_elbow) | `+10.83` | `-1.39` | `10.91` | `visible → visible` |
| 117 | `1259484 → 1320595` | `13` hip_L (anat right_hip) | `+29.85` | `+0.00` | `29.85` | `visible → visible` |
| 117 | `1259484 → 1320595` | `14` knee_R (anat left_knee) | `-10.95` | `-110.74` | `111.28` | `visible → visible` |
| 117 | `1259484 → 1320595` | `15` knee_L (anat right_knee) | `+0.00` | `+0.00` | `0.00` | `occluded → visible` |
| 119 | `1259485 → 1320596` | `11` wrist_L (anat right_wrist) | `-23.18` | `-7.28` | `24.30` | `visible → visible` |
| 119 | `1259485 → 1320596` | `12` hip_R (anat left_hip) | `+25.26` | `-6.52` | `26.08` | `visible → visible` |
| 119 | `1259485 → 1320596` | `14` knee_R (anat left_knee) | `+37.48` | `-31.77` | `49.13` | `visible → visible` |
