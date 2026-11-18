# A04 — Occlusion Specialist Report (Job 1623 / Pose17)

**Scope & Sources (Read-Only):**
- `artifacts/pose17_research/snapshots/job_1623_annotations_raw.json` (28 shapes, 476 keypoints, `version=0`)
- `artifacts/pose17_research/snapshots/job_1623_meta.json` (30 frames: `90..119`, `G06_091.jpg..G06_120.jpg`)
- `artifacts/pose17_research/snapshots/keypoint_mapping.json` & `job_1623_labels.json`
- `weeks/guidelines/w2-face50-pose17.md` (§5, §5A, §7) & `scripts/w2_qc_rules.py`
- Machine-readable audit output: `artifacts/pose17_research/agents/A04_visibility_audit.json`

---

## 1. Global Visibility & Flag Summary (476 Keypoints / 28 Shapes)

Because CVAT stores `occluded` (`Q`) and `outside` (`O`) as independent booleans (rather than a mutually exclusive COCO `v ∈ {0, 1, 2}` enum), we report both **mutually exclusive states** (summing to 476) and **marginal flag totals**:

| State / Flag | Count | % of 476 | Notes |
|---|---:|---:|---|
| `visible` (`occluded=False, outside=False`) | **359** | 75.4% | Normal visible keypoints |
| `occluded_only` (`occluded=True, outside=False`) | **59** | 12.4% | Valid `v1` (`Q`) state |
| `outside_only` (`occluded=False, outside=True`) | **36** | 7.6% | Valid `v0` (`O`) state |
| `both_occluded_and_outside` (`occluded=True, outside=True`) | **22** | 4.6% | **Invalid simultaneous flag conflict** across 13 frames |
| `hidden` (`H`) | **0** | 0.0% | Field not present in CVAT JSON schema |
| **Total keypoints** | **476** | **100.0%** | 28 skeletons × 17 keypoints (frames `100`, `118` empty) |
| *Marginal `occluded=True` total* | *81* | *17.0%* | *59 `occluded_only` + 22 `both`* |
| *Marginal `outside=True` total* | *58* | *12.2%* | *36 `outside_only` + 22 `both`* |

**Skeleton-level flag anomaly:**
- **1 of 28 skeletons** has skeleton-level `occluded=True, outside=False`: **Frame 93** (`G06_094.jpg`, `skeleton_id=1320580`, `960×540`). All 17 keypoints in this frame have `occluded=True` (`14` `occluded_only` + `3` `both_occluded_and_outside`, `0` `visible`). All other 27 skeletons have `occluded=False, outside=False`.

---

## 2. Per-Frame & Per-Keypoint Counts

### 2.1 Per-Frame Visibility Breakdown (`frames 90..119`)

| Frame | Image | Size | Skel `occ` | `visible` | `occ_only` | `out_only` | `both` | `occ` tot | `out` tot |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 90 | `G06_091.jpg` | 1280×1024 | False | 14 | 2 | 1 | 0 | 2 | 1 |
| 91 | `G06_092.jpg` | 1280×1024 | False | 14 | 1 | 0 | 2 | 3 | 2 |
| 92 | `G06_093.jpg` | 1280×1024 | False | 11 | 4 | 0 | 2 | 6 | 2 |
| 93 | `G06_094.jpg` | 960×540 | **True** | 0 | 14 | 0 | 3 | 17 | 3 |
| 94 | `G06_095.jpg` | 1280×1024 | False | 12 | 1 | 4 | 0 | 1 | 4 |
| 95 | `G06_096.jpg` | 1280×1024 | False | 15 | 0 | 2 | 0 | 0 | 2 |
| 96 | `G06_097.jpg` | 960×540 | False | 13 | 1 | 2 | 1 | 2 | 3 |
| 97 | `G06_098.jpg` | 960×540 | False | 13 | 3 | 0 | 1 | 4 | 1 |
| 98 | `G06_099.jpg` | 960×540 | False | 14 | 2 | 0 | 1 | 3 | 1 |
| 99 | `G06_100.jpg` | 1280×1024 | False | 12 | 1 | 4 | 0 | 1 | 4 |
| 100 | `G06_101.jpg` | 960×540 | — (empty) | 0 | 0 | 0 | 0 | 0 | 0 |
| 101 | `G06_102.jpg` | 960×540 | False | 15 | 1 | 1 | 0 | 1 | 1 |
| 102 | `G06_103.jpg` | 1280×1024 | False | 14 | 1 | 2 | 0 | 1 | 2 |
| 103 | `G06_104.jpg` | 512×424 | False | 13 | 3 | 1 | 0 | 3 | 1 |
| 104 | `G06_105.jpg` | 512×424 | False | 15 | 1 | 0 | 1 | 2 | 1 |
| 105 | `G06_106.jpg` | 960×540 | False | 13 | 3 | 0 | 1 | 4 | 1 |
| 106 | `G06_107.jpg` | 1280×1024 | False | 13 | 0 | 3 | 1 | 1 | 4 |
| 107 | `G06_108.jpg` | 1280×1024 | False | 14 | 1 | 2 | 0 | 1 | 2 |
| 108 | `G06_109.jpg` | 960×540 | False | 14 | 1 | 2 | 0 | 1 | 2 |
| 109 | `G06_110.jpg` | 1280×1024 | False | 14 | 2 | 0 | 1 | 3 | 1 |
| 110 | `G06_111.jpg` | 1280×1024 | False | 13 | 2 | 0 | 2 | 4 | 2 |
| 111 | `G06_112.jpg` | 1280×1024 | False | 12 | 3 | 2 | 0 | 3 | 2 |
| 112 | `G06_113.jpg` | 512×424 | False | 12 | 3 | 2 | 0 | 3 | 2 |
| 113 | `G06_114.jpg` | 960×540 | False | 14 | 1 | 2 | 0 | 1 | 2 |
| 114 | `G06_115.jpg` | 1280×1024 | False | 13 | 2 | 2 | 0 | 2 | 2 |
| 115 | `G06_116.jpg` | 960×540 | False | 14 | 3 | 0 | 0 | 3 | 0 |
| 116 | `G06_117.jpg` | 1280×1024 | False | 10 | 2 | 0 | 5 | 7 | 5 |
| 117 | `G06_118.jpg` | 960×540 | False | 13 | 1 | 2 | 1 | 2 | 3 |
| 118 | `G06_119.jpg` | 960×540 | — (empty) | 0 | 0 | 0 | 0 | 0 | 0 |
| 119 | `G06_120.jpg` | 1280×1024 | False | 15 | 0 | 2 | 0 | 0 | 2 |

### 2.2 Per-Keypoint Visibility Breakdown (`1..17`, across 28 shapes)

| KP | Name | `visible` | `occ_only` | `out_only` | `both` | `occ` tot | `out` tot | `hidden` |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `nose` | 27 | 1 | 0 | 0 | 1 | 0 | 0 |
| 2 | `eye_R` | 24 | 3 | 0 | 1 | 4 | **1** | 0 |
| 3 | `eye_L` | 26 | 1 | 1 | 0 | 1 | **1** | 0 |
| 4 | `ear_R` | 8 | 14 | 1 | 5 | 19 | **6** | 0 |
| 5 | `ear_L` | 24 | 3 | 0 | 1 | 4 | **1** | 0 |
| 6 | `shoulder_R` | 26 | 2 | 0 | 0 | 2 | 0 | 0 |
| 7 | `shoulder_L` | 27 | 1 | 0 | 0 | 1 | 0 | 0 |
| 8 | `elbow_R` | 24 | 3 | 0 | 1 | 4 | 1 | 0 |
| 9 | `elbow_L` | 26 | 2 | 0 | 0 | 2 | 0 | 0 |
| 10 | `wrist_R` | 22 | 4 | 0 | 2 | 6 | 2 | 0 |
| 11 | `wrist_L` | 25 | 2 | 0 | 1 | 3 | 1 | 0 |
| 12 | `hip_R` | 27 | 1 | 0 | 0 | 1 | 0 | 0 |
| 13 | `hip_L` | 27 | 1 | 0 | 0 | 1 | 0 | 0 |
| 14 | `knee_R` | 20 | 4 | 2 | 2 | 6 | 4 | 0 |
| 15 | `knee_L` | 24 | 2 | 2 | 0 | 2 | 2 | 0 |
| 16 | `ankle_R` | 2 | 5 | 15 | 6 | 11 | 21 | 0 |
| 17 | `ankle_L` | 0 | 10 | 15 | 3 | 13 | 18 | 0 |

---

## 3. Face / Shoulder / Hip (`1..7, 12, 13`) Marked `outside=True`

Per G06/BTC §5, head/face (`1..5`), shoulders (`6, 7`), and hips (`12, 13`) should **almost never** be `v0` (`outside=True`) unless physically outside frame bounds.

- **Shoulders (`6, 7`) and Hips (`12, 13`):** **0** `outside=True` instances (100% compliant).
- **Nose (`1`):** **0** `outside=True` instances.
- **Eyes (`2, 3`) and Ears (`4, 5`):** **9** instances across **8 frames** (`f93, f98, f103, f104, f105, f106 [×2], f116, f117`) — **all 9 lie deep inside frame bounds (`58.08 px` to `226.82 px` from the nearest edge)**:

| Frame | Image | W×H | KP | Name | `(x, y)` | `occ` | `out` | Min Border Dist | Violation Assessment |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| 93 | `G06_094.jpg` | 960×540 | 2 | `eye_R` | `(239.41, 186.96)` | True | True | 186.96 px | **High**: Eye inside frame; should be `occluded_only` (`Q`) per §5 |
| 98 | `G06_099.jpg` | 960×540 | 4 | `ear_R` | `(187.65, 203.49)` | True | True | 187.65 px | **Med**: Ear inside frame + `both` conflict; §5 prefers `Q`, or `O` + `ATTRIBUTE_CHECK` |
| 103 | `G06_104.jpg` | 512×424 | 4 | `ear_R` | `(98.00, 105.60)` | False | True | 98.00 px | **Med**: Ear inside frame; no `ATTRIBUTE_CHECK` issue (`issues=0`) |
| 104 | `G06_105.jpg` | 512×424 | 4 | `ear_R` | `(78.98, 110.86)` | True | True | 78.98 px | **Med**: Ear inside frame + `both` conflict |
| 105 | `G06_106.jpg` | 960×540 | 4 | `ear_R` | `(238.80, 150.53)` | True | True | 150.53 px | **Med**: Ear inside frame + `both` conflict |
| 106 | `G06_107.jpg` | 1280×1024 | 3 | `eye_L` | `(1053.18, 420.86)` | False | True | 226.82 px | **High**: Eye inside frame (`eye_R` visible nearby at `(1056.72, 466.94)`); should be `Q` |
| 106 | `G06_107.jpg` | 1280×1024 | 5 | `ear_L` | `(1060.75, 522.86)` | True | True | 219.25 px | **Med**: Ear inside frame + `both` conflict |
| 116 | `G06_117.jpg` | 1280×1024 | 4 | `ear_R` | `(1221.92, 491.65)` | True | True | 58.08 px | **Med**: Ear inside frame + `both` conflict |
| 117 | `G06_118.jpg` | 960×540 | 4 | `ear_R` | `(309.53, 128.08)` | True | True | 128.08 px | **Med**: Ear inside frame + `both` conflict |

---

## 4. Spatial Audit of `outside=True` vs `visible` / `occluded_only`

### 4.1 `outside=True` Keypoints (58 total) vs Frame Bounds `[0, W] × [0, H]`

Every single `outside=True` keypoint (`58 / 58`) has coordinates within `[0, W] × [0, H]`, which explains why `w2_qc_rules.py` flags all of them under `pose_outside_but_inside_frame`:

| Spatial Bucket | Count | `outside_only` | `both` | Interpretation |
|---|---:|---:|---:|---|
| Strictly outside `[0, W] × [0, H]` | **0** | 0 | 0 | None placed out-of-bounds |
| Exact frame border (`dist = 0.0 px`) | **2** | 2 | 0 | **True edge cutoff** (clamped to `y=1024.0`): `f90 kp 16 ankle_R (1102.33, 1024.0)` & `f102 kp 17 ankle_L (768.03, 1024.0)` in `1280×1024` |
| Near border (`0 < dist < 8 px`) | **0** | 0 | 0 | None |
| Strictly inside (`dist ≥ 8 px`) | **56** | 34 | 22 | `min_dist` ranges `11.96 px` (`f116 kp 17`) to `339.50 px` (`f92 kp 10`). Consists of **32** `outside_only` lower-limb (`14..17`), **2** `outside_only` face (`f103 kp4`, `f106 kp3`), and **22** `both_occluded_and_outside` conflicts |

*Note:* Per §5, `outside` (`v0`) coordinates are unused by BTC, and `v0` is valid inside the frame **only** for limbs (`8..11, 14..17`) occluded beyond estimation (e.g., ankles/knees behind steering wheel/door/newspaper). However, keeping `occluded=True` simultaneously or marking face points `v0` triggers ambiguity and QC warnings.

### 4.2 `visible` & `occluded_only` Boundary Check (`[0, W] × [0, H]` and `≤ 2px` Edge)

- `visible` (`occluded=False, outside=False`) outside `[0, W] × [0, H]`: **0**
- `visible` within `2 px` of frame edge: **0**
- `occluded_only` (`occluded=True, outside=False`) outside `[0, W] × [0, H]`: **0**
- `occluded_only` within `2 px` of frame edge: **1** — `f97` (`G06_098.jpg`, `960×540`) `kp 11 wrist_L` at `(348.20, 539.00)` (`1.00 px` from bottom edge; verify whether `wrist_L` is actually cropped out of frame → `O` or resting at bottom edge → `Q`).

---

## 5. Simultaneous `occluded=True` AND `outside=True` Conflicts (22 Instances)

22 keypoints across 13 frames have **both** `occluded=True` and `outside=True`. Downstream COCO/BTC converters that check `occluded` before `outside` will emit `v=1` instead of `v=0` (and vice versa). All 22 are strictly inside frame (`min_dist` `11.96 px` to `339.50 px`):

- **Ankles (`16` ×6, `17` ×3):** `f91 kp16`, `f93 kp16 & kp17`, `f97 kp16`, `f109 kp16`, `f110 kp16 & kp17`, `f116 kp16 & kp17`
- **Ears (`4` ×5, `5` ×1):** `f98 kp4`, `f104 kp4`, `f105 kp4`, `f106 kp5`, `f116 kp4`, `f117 kp4`
- **Wrists (`10` ×2, `11` ×1):** `f92 kp10 & kp11`, `f116 kp10`
- **Knees (`14` ×2):** `f91 kp14`, `f96 kp14`
- **Eye (`2` ×1):** `f93 kp2`
- **Elbow (`8` ×1):** `f116 kp8`

*(Frame `116` alone accounts for 5 of the 22 conflicts: `kp 4, 8, 10, 16, 17`.)*

---

## 6. Bilateral & Limb-Chain Visibility Asymmetry

- **Proximal-`outside` with distal-present chain anomalies (`shoulder→elbow→wrist` or `hip→knee→ankle`):** **0** instances. Whenever a proximal joint is `outside`, no distal joint on that limb is `visible` or `occluded_only`.
- **Bilateral `outside` asymmetry (one side `outside=True`, contralateral side non-`outside`):** **18** pair instances across **14 frames**:
  - **Ankles (`16/17`, 6 frames):** `f90` (`16` border `out_only`, `17` `occ_only`), `f91` (`16` `both`, `17` `occ_only`), `f97` (`16` `both`, `17` `occ_only`), `f101` (`17` `out_only` at `(654.15, 295.10)` `dist=244.9 px` while `16` is `visible` at `(693.00, 116.72)` — check if occluded or misflagged), `f109` (`16` `both`, `17` `occ_only`), `f110`? *(no, f110 has both 16 & 17 as `both`)*.
  - **Knees (`14/15`, 2 frames):** `f91` (`14` `both`, `15` `visible`), `f96` (`14` `both`, `15` `occ_only`).
  - **Ears (`4/5`, 7 frames):** `f98, f103, f104, f105, f116, f117` (`4` `out/both`, `5` `visible`), and `f106` (`5` `both`, `4` `visible`). Reflects side-view camera self-occlusion where the far-side ear was flagged `outside` instead of `occluded_only`.
  - **Eyes (`2/3`, 2 frames):** `f93` (`2` `both`, `3` `occ_only`), `f106` (`3` `out_only`, `2` `visible`).
  - **Elbow & Wrist (`8/9`, `10/11`, 1 frame):** `f116` (`8, 10` `both` on image-right side while `9, 11` are `visible` and `shoulder_R 6` is `occ_only`).
- **Bilateral `occluded_only` vs `visible` asymmetry:** **26** pair instances, dominated by `ears (4/5)` (`14` frames, `ear_R` occluded while `ear_L` visible in 13 of them), followed by `wrists` (`4`), `knees` (`3`), `eyes` (`3`), `shoulders` (`1`: `f116`), `elbows` (`1`: `f105`), `ankles` (`1`: `f104`).

---

## 7. Actionable Checklist for Gold Cleanup (Job 1623)

1. **Clear all 22 `both_occluded_and_outside` conflicts:** Decide strictly `Q` (`occluded=True, outside=False`) vs `O` (`occluded=False, outside=True`); pay special attention to `f116` (5 conflicts) and `f93` (3 conflicts + skeleton-level `occluded=True`).
2. **Fix `eye_R` (`f93`) and `eye_L` (`f106`):** Change from `outside=True` to `occluded_only` (`Q`) with estimated coordinates per §5.
3. **Standardize the 7 `ear` `outside=True` cases (`f98, f103, f104, f105, f106, f116, f117`):** Per §5, change to `occluded_only` (`Q`) if head/hair occlusion can be estimated within ±20 px; otherwise keep `O` and log an `ATTRIBUTE_CHECK` issue.
4. **Verify `f97 kp 11 wrist_L` `(348.2, 539.0)`** (`1 px` from bottom border) and **`f101 kp 17 ankle_L`** (`outside_only` while `ankle_R` is `visible`).
5. **Update `w2_qc_rules.py` awareness:** `w2_qc_rules.py` currently does not flag `occluded=True AND outside=True`, skeleton-level `occluded=True`, or face/shoulder/hip `outside=True` separately; adding those deterministic checks will prevent recurrence.
