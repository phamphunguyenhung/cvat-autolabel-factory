# A05 — Difficult Case Miner Report (Job 1623, Frames 90–119)

**Scope & Sources:**
- Raw annotations: `artifacts/pose17_research/snapshots/job_1623_annotations_raw.json`
- Frame metadata & labels: `artifacts/pose17_research/snapshots/job_1623_meta.json`, `job_1623_labels.json`
- Domain notes & VLM audits: `week02/task402-pose/job1623-pose17/EDGE_CASES.md`, `week02/issues.md` (E3/E4), `reports/w2_vlm/1623_90_104.json`, `reports/w2_vlm/1623_105_119.json`
- Structured output: [`A05_cases.json`](A05_cases.json)
- Overlays (all 30 frames rendered): `artifacts/pose17_research/evidence/overlays/f{090..119}_{G06_091..120}.jpg`

---

## 1. Dataset & Objective Metrics Overview (30 Frames)

- **Modalities:** 18 IR grayscale (`max_rgb_diff = 0.0`, `sat = 0.0`) · 12 RGB color (`sat = 78.8–110.7`).
- **Resolutions (`RESOLUTION_MISMATCH`):**
  - `960×540` (BTC guideline nominal): **12 frames** (all 12 RGB side-views).
  - `1280×1024`: **15 frames** (frontal IR + 2 horizontal fisheye IR `f106, f110`).
  - `512×424`: **3 frames** (`f103, f104, f112` — reclined side-view IR).
  - **18/30 frames (60.0%)** deviate from BTC's `960×540` assumption, making unscaled `±5 px` / `±20 px` pixel tolerance inconsistent across cameras.
- **Brightness (`LOW_LIGHT`):** All 18 IR frames have `mean_luma` between **12.8** (`f116`) and **36.4** (`f119`), with `dark_fraction (luma < 40)` between **0.68** and **0.93** (`f099` highest dark fraction `0.93`; `f116` lowest mean luma `12.8`).
- **Sharpness / Blur (`MOTION_BLUR`):** RGB Laplacian variance ranges `183.7–378.8`, with lowest RGB sharpness on `f118` (`183.7`) and `f100` (`192.8`, strong foreground hand/arm motion blur), plus `f108` (`283.5`, local hand blur) and `f113` (`218.9`, blurred raised arm). IR Laplacian variance is much lower (`3.5–62.8`), dropping below `10.0` on `f116` (`3.5`), `f110` (`5.3`), `f099` (`7.2`), `f091` (`7.8`), `f094` (`9.7`).
- **Annotation Coverage:** 28/30 frames have 1 skeleton (`28 × 17 = 476` keypoints); **2 frames have 0 shapes (`MISSING_ANNOTATION`: `f100`, `f118`)**.

---

## 2. Taxonomy Distribution (All 30 Frames)

| Category | Count | % | Key Trigger / Representative Frames |
|---|---:|---:|---|
| `SITTING_POSE` | 30 | 100% | In-cabin seated driver across all frames |
| `OCCLUSION` | 29 | 96.7% | Steering wheel, dashboard/taplo, newspaper (`f094`), book (`f093, f105, f111`), laptop (`f096`), bags (`f090, f091, f109`), phone (`f103, f115`), hands (`f118`) |
| `JOINT_INFERENCE` | 28 | 93.3% | Inferring occluded knees/ankles under taplo, ears under hair, head under hands (`f118`), hips under bags/newspaper |
| `VISIBILITY_CONFLICT` | 25 | 83.3% | **24 annotated frames** mark keypoints `outside` while well inside frame bounds (`>15 px` from border); `f093` marks all 14 in-frame points `occluded` (`V=0, Q=14, O=3`); `f101` has `2` (V) and `4` (Q) at identical `(265, 141)`; `f112` has `10` (Q) and `11` (V) ~8.1 px apart |
| `KEYPOINT_MISPLACEMENT` | 24 | 80.0% | Ankles `16/17` placed on hand/newspaper (`f094`), thighs (`f095, f099`), door/console/bag (`f093, f098, f101, f108, f113, f115, f117`), or above knee `15` (`f119`); `6` on nose (`f117`); `10` on nose (`f116`); `1` below chin (`f092`); `11` mid-forearm (`f114`) |
| `LOW_LIGHT` | 18 | 60.0% | All 18 IR frames (`mean_luma < 40`); severe (`mean_luma < 25`) in `f092, f099, f103, f104, f110, f112, f114, f116` |
| `RESOLUTION_MISMATCH` | 18 | 60.0% | `1280×1024` (15) + `512×424` (3: `f103, f104, f112`) vs BTC `960×540` |
| `SELF_OCCLUSION` | 18 | 60.0% | Far-side ear/shoulder/elbow in side views; folded/crossed arms (`f099, f110, f114`); face covered by hands (`f118`) |
| `FISHEYE_ROTATION` *(new)* | 17 | 56.7% | 12 RGB + 3 IR side-mount views (head left, feet right) + 2 horizontal fisheye IR (`f106, f110`: head right, feet left) |
| `LEFT_RIGHT_AMBIGUITY` | 17 | 56.7% | R/L pairs separated vertically (`|dy| > |dx|`), causing `rl_x_inverted` in 15 annotated side/horizontal frames (all 7 pairs inverted in `f106`; 6 in `f096, f098, f101, f104, f105, f113, f117`) |
| `OUT_OF_FRAME` | 14 | 46.7% | Feet/ankles exiting bottom or right edge; head/wrists near top/left edge (`f092, f097, f118`) |
| `HAND_OVERLAP` | 11 | 36.7% | Hands clasped (`f099`), on steering wheel (`f112`), holding bottle (`f114`), phone (`f103`), pen/paper (`f102, f107, f117`), bag (`f091`), covering face (`f118`), on lap (`f110, f119`) |
| `TRUNCATION` | 9 | 30.0% | Lower legs/head cut by frame edges (`f092, f093, f095, f096, f097, f098, f100, f102, f118`) |
| `CROSS_LIMB` | 7 | 23.3% | Crossed lower legs in draft (`f093, f096`), arms crossed over chest (`f110`), jacket donning (`f113`), reaching across lap/torso (`f091, f094, f114`) |
| `FORESHORTENING` | 4 | 13.3% | Close-to-camera leaning (`f092`), deep forward bend (`f097`), extreme right lean (`f116`), reclined leg/arm foreshortening (`f104`) |
| `MOTION_BLUR` | 4 | 13.3% | Foreground hand/arm blur (`f100`), reaching hand (`f108`), raised arm (`f113`), arm motion (`f118`) |
| `MISSING_ANNOTATION` *(new)* | 2 | 6.7% | `f100` (`G06_101.jpg`), `f118` (`G06_119.jpg`) — 0 shapes in raw snapshot |

---

## 3. Severity Breakdown & Critical Difficult Cases

- **Critical (8 frames):** `f093, f094, f100, f106, f110, f112, f116, f118`
- **High (12 frames):** `f091, f092, f096, f097, f099, f101, f103, f104, f113, f114, f115, f117`
- **Medium (8 frames):** `f095, f098, f105, f107, f108, f109, f111, f119`
- **Low (2 frames):** `f090, f102`

### Representative Critical & High-Difficulty Cases (Visually Verified)

1. **`f100` (`G06_101.jpg`, 960×540 RGB)** — `MISSING_ANNOTATION`, `MOTION_BLUR`, `FISHEYE_ROTATION`
   - Overlay: `artifacts/pose17_research/evidence/overlays/f100_G06_101.jpg`
   - 0 shapes present; driver's left arm/hand exhibits heavy motion smear (`Lap=192.8`), legs tucked under dashboard.
2. **`f118` (`G06_119.jpg`, 960×540 RGB)** — `MISSING_ANNOTATION`, `OCCLUSION`, `HAND_OVERLAP`, `OUT_OF_FRAME`
   - Overlay: `artifacts/pose17_research/evidence/overlays/f118_G06_119.jpg`
   - 0 shapes present; driver raises both hands/blue cloth covering nose/eyes/mouth; head touches upper-left border; mild blur (`Lap=183.7`). Requires `JOINT_INFERENCE` for `1..5` (`occluded` vs `outside`).
3. **`f093` (`G06_094.jpg`, 960×540 RGB)** — `VISIBILITY_CONFLICT`, `CROSS_LIMB`, `KEYPOINT_MISPLACEMENT`
   - Overlay: `artifacts/pose17_research/evidence/overlays/f093_G06_094.jpg`
   - **V/Q/O = 0/14/3**: every clearly visible joint (`1,3,5,6,7,8,9,10,11,12,13,14,15`) is erroneously marked `occluded`; `7Q` is ~80 px low on the sleeve; `14→16` and `15→17` cross onto console/gearshift.
4. **`f094` (`G06_095.jpg`, 1280×1024 IR)** — `OCCLUSION`, `KEYPOINT_MISPLACEMENT`, `VISIBILITY_CONFLICT`
   - Overlay: `artifacts/pose17_research/evidence/overlays/f094_G06_095.jpg`
   - Newspaper covers lap; `17O` (left ankle) is placed directly on the left hand `(324, 729)`; `14O/15O/16O` are marked `outside` while inside the frame.
5. **`f106` (`G06_107.jpg`, 1280×1024 IR)** — `FISHEYE_ROTATION`, `LEFT_RIGHT_AMBIGUITY`, `VISIBILITY_CONFLICT`
   - Overlay: `artifacts/pose17_research/evidence/overlays/f106_G06_107.jpg`
   - Horizontal fisheye IR (head right, feet left). **All 7 R/L pairs (`6/7..16/17`) are x-inverted (`rlInv=7`)**; `3O` and `5O` are marked `outside` on the visible face; `16O/17O` are inside frame on steering wheel.
6. **`f110` (`G06_111.jpg`, 1280×1024 IR)** — `LOW_LIGHT`, `FISHEYE_ROTATION`, `CROSS_LIMB`, `SELF_OCCLUSION`
   - Overlay: `artifacts/pose17_research/evidence/overlays/f110_G06_111.jpg`
   - Dark horizontal fisheye IR (`L=17.0, Dark=0.89, Lap=5.3`), head right; arms folded across chest (`7-9-11` crossing `6-8-10`); `rlInv=4`; `16O/17O` marked `outside` inside frame.
7. **`f112` (`G06_113.jpg`, 512×424 IR)** — `RESOLUTION_MISMATCH`, `LOW_LIGHT`, `HAND_OVERLAP`, `VISIBILITY_CONFLICT`
   - Overlay: `artifacts/pose17_research/evidence/overlays/f112_G06_113.jpg`
   - Lowest-resolution dark IR (`512×424`, `L=17.9, Dark=0.84`); wrists `10Q` and `11` (visible) collapse to `8.1 px` on steering wheel; `2/3/4Q` compressed on tiny head; `16O/17O` on dashboard/gearshift.
8. **`f116` (`G06_117.jpg`, 1280×1024 IR)** — `LOW_LIGHT`, `KEYPOINT_MISPLACEMENT`, `FORESHORTENING`
   - Overlay: `artifacts/pose17_research/evidence/overlays/f116_G06_117.jpg`
   - Darkest frame (`L=12.8, Dark=0.91, Lap=3.5`); driver leans far right; `10O` (right wrist) placed on the nose/face `(1173, 507)`, `8O` floating off torso `(1186, 650)`, `6Q` on neck, `4O/2Q` clustered.
9. **Other notable high-severity patterns verified on overlays:**
   - **`f092`**: Nose `1` ~35 px below nose tip on chin; `8Q/10O` float off right side of torso; `11O` on passenger seat. *(Note: in current snapshot `15=(769,908)` is above `17=(782,974)`, unlike earlier VLM draft note).*
   - **`f099`**: Dark IR (`L=18.9, Dark=0.93`); `15O` and `17O` collapsed on left thigh and marked `outside`.
   - **`f101`**: Exact duplicate coordinate `(265, 141)` for `2` (`visible`) and `4` (`occluded`).
   - **`f103` & `f104`**: `512×424` dark IR (`L=21.1–23.9`), `2/4` within `2.2–4.5 px`; `f104` wrist `10` stops at sleeve cuff short of hand on top of wheel.
   - **`f114`**: Wrist `11` placed mid-forearm (~100 px from hand holding bottle); `8` and `10Q` within ~28 px.
   - **`f115` & `f117`**: `16/17` placed on door trim/paper bag; `f117` places `6` (right shoulder) on the nose/chin `(340, 171)`.
   - **`f119`**: Otherwise cleanest IR frame, yet `17O` (`y=907`) is placed **above** knee `15` (`y=938`) and marked `outside`.

---

## 4. Systemic Rules Needed for Pose17 Gold Reference & Guideline Engine

1. **Disambiguate `occluded` vs `outside` inside frame bounds:** 24/28 annotated frames misuse `outside` for occluded interior joints (`16/17` under dashboard/steering wheel, `4` on forehead, `14/15` under newspaper/laptop). Enforce: `outside` ONLY when keypoint lies outside `[0, W] × [0, H]` or cannot be anatomically inferred from visible limb chains.
2. **Resolve `FISHEYE_ROTATION` / `LEFT_RIGHT_AMBIGUITY` rule:** In 17/30 frames (side-mounted 90° and horizontal fisheye `f106, f110`), body `R/L` pairs separate along `y` rather than `x`. Image-`x` heuristic breaks down and causes systematic `R/L` inversion (`rlInv=7` in `f106`). Guideline must specify an unambiguous convention (anatomical `R/L` vs image-axis projection when torso axis is horizontal).
3. **Zero-overlap & kinematic sanity checks:** Block exact/near-duplicate distinct joints (`2/4` in `f101, f103, f104`; `3/5` in `f091`; `10/11` in `f112`), knee-above-ankle inversion (`f119`), `shank > 1.5× thigh` (`f115`), and `V=0` bulk-occlusion accidents (`f093`).
4. **Resolution-normalized QA thresholds:** Scale pixel-distance rules (`±5 px` / `±20 px`) relative to frame diagonal (`512×424` vs `960×540` vs `1280×1024`).
5. **Annotate missing frames (`f100`, `f118`) with explicit `LOW_VISIBILITY` / `JOINT_INFERENCE` rules** for motion-blurred hands (`f100`) and hand-occluded face (`f118`).

---

## 5. Complete 30-Frame Index

| Frame | Image | Size | Mod | Luma | Dark | Lap | V/Q/O | Sev | Primary Issues |
|---:|---|---|---|---:|---:|---:|---|---|---|
| 90 | G06_091.jpg | 1280×1024 | IR | 35.9 | 0.79 | 25.4 | 14/2/1 | low | Cleanest IR baseline; 14Q, 17Q, 16O at bottom edge |
| 91 | G06_092.jpg | 1280×1024 | IR | 28.1 | 0.82 | 7.8 | 14/1/2 | high | 3/5 collapse (~2px); 7 inward; 12/13 high; 14O/16O in-frame |
| 92 | G06_093.jpg | 1280×1024 | IR | 22.9 | 0.85 | 18.6 | 11/4/2 | high | Foreshortened; 1 on chin (~35px low); 8Q/10O/11O misplaced |
| 93 | G06_094.jpg | 960×540 | RGB | 72.1 | 0.51 | 325.4 | 0/14/3 | critical | Bulk V=0/Q=14 bug; 7Q low; crossed 16O/17O; 2O on forehead |
| 94 | G06_095.jpg | 1280×1024 | IR | 33.9 | 0.68 | 9.7 | 12/1/4 | critical | Newspaper occlusion; 17O on left hand; 14O/15O/16O in-frame |
| 95 | G06_096.jpg | 1280×1024 | IR | 31.7 | 0.79 | 18.4 | 15/0/2 | medium | 16O on right thigh in-frame; 17O at bottom shin |
| 96 | G06_097.jpg | 960×540 | RGB | 71.1 | 0.51 | 262.5 | 13/1/3 | high | Laptop occlusion; rlInv=3; 14O on knee; crossed 16O/17O |
| 97 | G06_098.jpg | 960×540 | RGB | 54.6 | 0.60 | 253.7 | 13/3/1 | high | Deep forward lean; 14/15/16O/17Q on dashboard/door |
| 98 | G06_099.jpg | 960×540 | RGB | 91.4 | 0.46 | 378.8 | 14/2/1 | medium | 16Q/17Q on door panel; 4O on forehead; rlInv=2 |
| 99 | G06_100.jpg | 1280×1024 | IR | 18.9 | 0.93 | 7.2 | 12/1/4 | high | Severe dark IR; 15O/17O collapsed on thigh; 7 inward |
| 100 | G06_101.jpg | 960×540 | RGB | 90.7 | 0.40 | 192.8 | 0/0/0 | critical | **MISSING SKELETON**; strong arm/hand motion blur |
| 101 | G06_102.jpg | 960×540 | RGB | 72.6 | 0.44 | 306.0 | 15/1/1 | high | Duplicate coords 2=4 at (265,141); 17O on gearshift; rlInv=3 |
| 102 | G06_103.jpg | 1280×1024 | IR | 33.0 | 0.81 | 17.0 | 14/1/2 | low | Writing on lap; 14 in dark shadow; 16O/17O at bottom edge |
| 103 | G06_104.jpg | 512×424 | IR | 21.1 | 0.81 | 35.6 | 13/3/1 | high | 512×424 dark IR; reclined phone; 2Q/4O ~4.5px; rlInv=3 |
| 104 | G06_105.jpg | 512×424 | IR | 23.9 | 0.77 | 62.8 | 15/1/1 | high | 512×424 dark IR; 2/4O ~2.2px; 10 short on sleeve; rlInv=5 |
| 105 | G06_106.jpg | 960×540 | RGB | 66.9 | 0.54 | 308.3 | 13/3/1 | medium | Book occludes 8Q/10; 4O on forehead; rlInv=4 |
| 106 | G06_107.jpg | 1280×1024 | IR | 26.9 | 0.82 | 14.0 | 13/0/4 | critical | Horizontal fisheye (head right); rlInv=7; 3O/5O/16O/17O in-frame |
| 107 | G06_108.jpg | 1280×1024 | IR | 33.9 | 0.79 | 22.7 | 14/1/2 | medium | 14 visible in dark shadow behind wheel; 16O/17O in-frame |
| 108 | G06_109.jpg | 960×540 | RGB | 74.5 | 0.43 | 283.5 | 14/1/2 | medium | Hand motion blur; 16O/17O on gearshift/console; rlInv=3 |
| 109 | G06_110.jpg | 1280×1024 | IR | 27.8 | 0.81 | 19.9 | 14/2/1 | medium | Bag over hips; 16O high near steering wheel center |
| 110 | G06_111.jpg | 1280×1024 | IR | 17.0 | 0.89 | 5.3 | 13/2/2 | critical | Severe dark horizontal fisheye; crossed arms; rlInv=4 |
| 111 | G06_112.jpg | 1280×1024 | IR | 32.8 | 0.79 | 12.8 | 12/3/2 | medium | Book on lap occludes 10Q; 16O/17O inside frame |
| 112 | G06_113.jpg | 512×424 | IR | 17.9 | 0.84 | 30.3 | 12/3/2 | critical | 512×424 very dark IR; wrists 10Q/11 ~8.1px; rlInv=4 |
| 113 | G06_114.jpg | 960×540 | RGB | 70.0 | 0.52 | 218.9 | 14/1/2 | high | Putting on jacket (blur/cross-limb); 16O/17O on yellow bag |
| 114 | G06_115.jpg | 1280×1024 | IR | 22.2 | 0.87 | 17.1 | 13/2/2 | high | Dark IR; 11 mid-forearm (~100px off); 8/10Q near bottle |
| 115 | G06_116.jpg | 960×540 | RGB | 60.3 | 0.59 | 283.1 | 14/3/0 | high | 16Q/17Q on door trim (shank > thigh); rlInv=3 |
| 116 | G06_117.jpg | 1280×1024 | IR | 12.8 | 0.91 | 3.5 | 10/2/5 | critical | Darkest IR (L=12.8); 10O on nose; 8O outside body; 6Q on neck |
| 117 | G06_118.jpg | 960×540 | RGB | 70.5 | 0.47 | 280.0 | 13/1/3 | high | 6 on nose/chin; 4O on forehead; 16O/17O on paper bag; rlInv=3 |
| 118 | G06_119.jpg | 960×540 | RGB | 56.8 | 0.62 | 183.7 | 0/0/0 | critical | **MISSING SKELETON**; hands/cloth cover face; head near top-left |
| 119 | G06_120.jpg | 1280×1024 | IR | 36.4 | 0.78 | 28.0 | 15/0/2 | medium | Clearest IR yet 17O placed above knee 15; 16O inside frame |
