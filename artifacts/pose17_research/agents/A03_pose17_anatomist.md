# A03 — Pose17 Anatomist Report (`person_vf17`)

**Task:** Pose17 Gold Reference & Guideline Engine  
**Role:** A03 — Pose17 Anatomist  
**Date:** 2026-11-18  

---

## 1. Sources Inspected & Availability

| Artifact / File | Status | Key Contents Used |
|---|---|---|
| `data/jobs/edufun/1623/labels.json` | Found | CVAT skeleton `person_vf17` (`id=12322`, `project_id=159`), 17 sublabels (`"1"`..`"17"`, IDs `12323`..`12339`), SVG `<line>` edges and `<circle>` coordinates |
| `weeks/guidelines/w2-face50-pose17.md` | Found | Internal G06 guideline synced 2026-11-17 with BTC V1 (Sections 1, 3, 4, 5, 5A, 5B, 7, 8, G) |
| `weeks/guidelines/images/pose17_template.png` | Found | Visual verification of CVAT `person_vf17` template (nodes `1`–`17` and 18 edges) |
| `src/cvat_tools/pose/person17.py` | Found | `COCO`, `LIMB_IDX`, `Q_CONF`, `V0_CONF`, `BORDER_PX`, `detect`, `point_state`, `plausibility_pose`, `enforce_image_lr`, `frame_people` |
| `scripts/eval_pose17.py` | Found | `NAMES`, `sigmas()`, `evaluate()` (OKS + mean px against `gold.json`) |
| `src/cvat_tools/pose/gold.py` | Found | `draft_points()`, `refresh_gold()`, `load_gold()` |
| `src/cvat_tools/pose/week2.py` | Found | `_person17_frame()`, `_shape()`, `person_frame()` |
| `scripts/w2_qc_rules.py` | Found | `PAIRS`, `check_pose()` deterministic QC rules |
| `week02/task402-pose/job1623-pose17/EDGE_CASES.md` & `SPEC.md` | Found | Job 1623 frame-by-frame edge cases (`f90`–`f119`), `source=file` frames, `skip_frames` |
| `../tools/skeleton-pose-manager/config/schema.json` | Found (at `paths.REPO / "tools/skeleton-pose-manager/config/schema.json"`) | COCO 17 keypoints, 19-edge `skeleton`, `flip_pairs`, `sigmas` |
| `HumanPose17_Annotation_Guideline_V1.docx` | **Not found in repo** | Searched recursively under `D:\06-Learning\AIA-VINGROUP\learning`; rules are incorporated into `weeks/guidelines/w2-face50-pose17.md` |

---

## 2. Exact 17-Keypoint Mapping Table (`person_vf17`)

Under **BTC V1** (`w2-face50-pose17.md` §3–4), `R` / `L` is **image-based** (`R` = image right, `L` = image left). In standard front-facing COCO (`schema.json`), the person's anatomical `left_*` appears on **image right** (`cx > 50` in `labels.json`), and anatomical `right_*` appears on **image left** (`cx < 50`). Thus, numeric sublabel indices `1..17` map 1-to-1 to COCO indices `0..16` in front-facing view, while BTC V1 names even points `R` and odd points `L`.

| `cvat_sublabel_id` | `cvat_sublabel_name` | `coco_index` | `coco_name` | `vietnamese_name` (BTC/G06) | `anatomical_landmark` (`w2-face50-pose17.md` §3) | `body_region` | `side_rule` | SVG `(cx, cy)` & Color | COCO `sigma` |
|---:|:---:|---:|---|---|---|---|---|---|---:|
| `12323` | `"1"` | `0` | `nose` | mũi | Chóp mũi (mặt nghiêng vẫn đặt tại chóp mũi, không dời về giữa mặt) | `head` | `1=center` | `(50, 15)` `#d12345` | `0.026` |
| `12324` | `"2"` | `1` | `left_eye` | mắt R | Tâm đồng tử (mắt nhắm: tâm khe mí) | `head` | `even=R=image_right` | `(55, 14)` `#350dea` | `0.025` |
| `12325` | `"3"` | `2` | `right_eye` | mắt L | Tâm đồng tử (mắt nhắm: tâm khe mí) | `head` | `odd=L=image_left` | `(45, 14)` `#479ffe` | `0.025` |
| `12326` | `"4"` | `3` | `left_ear` | tai R | Ống tai (không phải chóp tai hay dái tai) | `head` | `even=R=image_right` | `(60, 18)` `#4a649f` | `0.035` |
| `12327` | `"5"` | `4` | `right_ear` | tai L | Ống tai (không phải chóp tai hay dái tai) | `head` | `odd=L=image_left` | `(40, 18)` `#478144` | `0.035` |
| `12328` | `"6"` | `5` | `left_shoulder` | vai R | Tâm khớp vai (điểm xoay của cánh tay) | `torso` | `even=R=image_right` | `(60, 30)` `#57236b` | `0.079` |
| `12329` | `"7"` | `6` | `right_shoulder` | vai L | Tâm khớp vai (điểm xoay của cánh tay) | `torso` | `odd=L=image_left` | `(40, 30)` `#1cdda5` | `0.079` |
| `12330` | `"8"` | `7` | `left_elbow` | khuỷu R | Tâm khớp khuỷu | `upper_limb` | `even=R=image_right` | `(68, 45)` `#e2bc6e` | `0.072` |
| `12331` | `"9"` | `8` | `right_elbow` | khuỷu L | Tâm khớp khuỷu | `upper_limb` | `odd=L=image_left` | `(32, 45)` `#f067db` | `0.072` |
| `12332` | `"10"` | `9` | `left_wrist` | cổ tay R | Nếp gấp cổ tay (tay cầm vô-lăng/vật vẫn đặt tại khớp, không dời lên vành vô-lăng/vật) | `upper_limb` | `even=R=image_right` | `(74, 60)` `#63bbfa` | `0.062` |
| `12333` | `"11"` | `10` | `right_wrist` | cổ tay L | Nếp gấp cổ tay (tay cầm vô-lăng/vật vẫn đặt tại khớp, không dời lên vành vô-lăng/vật) | `upper_limb` | `odd=L=image_left` | `(26, 60)` `#22b16f` | `0.062` |
| `12334` | `"12"` | `11` | `left_hip` | hông R | Tâm khớp háng (không phải mép ngoài hông hay cạp quần) | `torso` | `even=R=image_right` | `(55, 62)` `#daddec` | `0.107` |
| `12335` | `"13"` | `12` | `right_hip` | hông L | Tâm khớp háng (không phải mép ngoài hông hay cạp quần) | `torso` | `odd=L=image_left` | `(45, 62)` `#2ac791` | `0.107` |
| `12336` | `"14"` | `13` | `left_knee` | gối R | Giữa xương bánh chè | `lower_limb` | `even=R=image_right` | `(58, 80)` `#de22a0` | `0.087` |
| `12337` | `"15"` | `14` | `right_knee` | gối L | Giữa xương bánh chè | `lower_limb` | `odd=L=image_left` | `(42, 80)` `#a7a570` | `0.087` |
| `12338` | `"16"` | `15` | `left_ankle` | cổ chân R | Ngang mắt cá | `lower_limb` | `even=R=image_right` | `(60, 97)` `#74db1b` | `0.089` |
| `12339` | `"17"` | `16` | `right_ankle` | cổ chân L | Ngang mắt cá | `lower_limb` | `odd=L=image_left` | `(40, 97)` `#aaa246` | `0.089` |

Notes on `body_region` grouping in `person17.py`:
- `LIMB_IDX = {7, 8, 9, 10, 13, 14, 15, 16}` (0-based) cleanly isolates `upper_limb` (`8–11` CVAT) + `lower_limb` (`14–17` CVAT) from `head` (`1–5` CVAT) + `torso` (`6, 7, 12, 13` CVAT).
- `torso_quality()` uses indices `5:13` (`6..13` CVAT = shoulders, elbows, wrists, hips).
- `plausibility_pose()` computes `torso` length as `||mean(shoulders 5,6) - mean(hips 11,12)||`.

---

## 3. Exact Skeleton Topology (CVAT SVG vs COCO Edges)

### 3.1 `person_vf17` SVG Edges (`data/jobs/edufun/1623/labels.json`)
The CVAT skeleton SVG defines **18 directed `<line>` edges** (`data-node-from` → `data-node-to`), matching `weeks/guidelines/images/pose17_template.png`:

| # | `data-node-from` | `data-node-to` | SVG `(x1,y1) -> (x2,y2)` | Anatomical / Kinematic Connection | In COCO `schema.json`? |
|---:|:---:|:---:|---|---|---|
| 1 | `1` | `2` | `(50,15) -> (55,14)` | mũi → mắt R | Yes `[1, 2]` |
| 2 | `1` | `3` | `(50,15) -> (45,14)` | mũi → mắt L | Yes `[1, 3]` |
| 3 | `2` | `4` | `(55,14) -> (60,18)` | mắt R → tai R | Yes `[2, 4]` |
| 4 | `3` | `5` | `(45,14) -> (40,18)` | mắt L → tai L | Yes `[3, 5]` |
| 5 | `4` | `6` | `(60,18) -> (60,30)` | tai R → vai R | Yes `[4, 6]` |
| 6 | `5` | `7` | `(40,18) -> (40,30)` | tai L → vai L | Yes `[5, 7]` |
| 7 | `6` | `7` | `(60,30) -> (40,30)` | vai R → vai L | Yes `[6, 7]` |
| 8 | `6` | `8` | `(60,30) -> (68,45)` | vai R → khuỷu R | Yes `[6, 8]` |
| 9 | `8` | `10` | `(68,45) -> (74,60)` | khuỷu R → cổ tay R | Yes `[8, 10]` |
| 10 | `7` | `9` | `(40,30) -> (32,45)` | vai L → khuỷu L | Yes `[7, 9]` |
| 11 | `9` | `11` | `(32,45) -> (26,60)` | khuỷu L → cổ tay L | Yes `[9, 11]` |
| 12 | `6` | `12` | `(60,30) -> (55,62)` | vai R → hông R | Yes `[6, 12]` |
| 13 | `7` | `13` | `(40,30) -> (45,62)` | vai L → hông L | Yes `[7, 13]` |
| 14 | `12` | `13` | `(55,62) -> (45,62)` | hông R → hông L | Yes `[12, 13]` |
| 15 | `12` | `14` | `(55,62) -> (58,80)` | hông R → gối R | Yes `[12, 14]` |
| 16 | `14` | `16` | `(58,80) -> (60,97)` | gối R → cổ chân R | Yes `[14, 16]` |
| 17 | `13` | `15` | `(45,62) -> (42,80)` | hông L → gối L | Yes `[13, 15]` |
| 18 | `15` | `17` | `(42,80) -> (40,97)` | gối L → cổ chân L | Yes `[15, 17]` |

### 3.2 Comparison with Standard COCO Edges (`schema.json`)
`tools/skeleton-pose-manager/config/schema.json` defines **19 edges** under `"person"."skeleton"`:
`[16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13], [6, 7], [6, 8], [7, 9], [8, 10], [9, 11], [2, 3], [1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7]`.

- **Exact topology difference:** Standard COCO includes **`[2, 3]` (eye-to-eye: `mắt R`–`mắt L`)**, whereas CVAT `person_vf17` (`labels.json` SVG and `pose17_template.png`) **omits `[2, 3]`** (18 edges total). All other 18 edges match identically (undirected).

---

## 4. Left / Right Rule: Image-Based R/L (BTC V1) vs Anatomical R/L

### 4.1 Core Rule (`w2-face50-pose17.md` §3, §4, §5A.G)
- **BTC V1 convention:** Even sublabels (`2, 4, 6, 8, 10, 12, 14, 16`) = **`R` = Image Right (`phải ảnh`, larger `x`)**; Odd sublabels (`3, 5, 7, 9, 11, 13, 15, 17`) = **`L` = Image Left (`trái ảnh`, smaller `x`)**.
- **No anatomical inference:** Even when the driver turns around, faces away, twists, leans sideways, or appears rotated 90° in fisheye IR images, annotators MUST NOT infer anatomical left/right (and MUST NOT guess by seatbelt or gaze direction).
- **Kinematic continuity check (§3, §5A.G):** On each side, the chains `vai–khuỷu–cổ tay` (`6–8–10` and `7–9–11`) and `hông–gối–cổ chân` (`12–14–16` and `13–15–17`) must remain continuous without crossing over to the opposite side (crossing indicates an L/R swap mistake).
- **Why front-facing COCO still aligns:** When a subject faces the camera, their anatomical `left_*` lies on image right (`R`, even sublabels) and anatomical `right_*` lies on image left (`L`, odd sublabels). When facing away or rotated 180°, anatomical pose models (YOLO/ViTPose) flip relative to image R/L, so all 8 pairs must swap together.

### 4.2 90°-Rotated Fisheye Images & `UNCERTAIN_CLASS` Edge Case
- **Guideline (`w2-face50-pose17.md` §4, §5A.G, §5B, §8 Q2):**
  - When the person lies horizontally or the fisheye IR image is rotated ~90° such that corresponding left/right keypoints share nearly the same `x` coordinate (impossible to distinguish "image right" vs "image left"), **do not guess**.
  - Raise CVAT issue **`UNCERTAIN_CLASS`**, resolve via group majority vote (inter-annotator agreement) first, and escalate to mentor if needed.
  - Affected frames in Job 1623 flagged in `w2-face50-pose17.md` §5A.G / §8 Q2: **`f96, f103, f105, f106, f110, f112`** (plus high-risk frames `f104, f92, f97, f116, f118`).
- **Implementation in `person17.py`:**
  1. `detect(backend, img_bgr)` tests rotation `k=0` first; if no person is found or `torso_quality(p) < 0.6`, it tries `k in (1, 2, 3)` (`90°, 180°, 270°`, penalized by `rot_bias=0.08`) so YOLO/ViTPose sees an upright person, then calls `unrotate()` back to original image coordinates.
  2. `enforce_image_lr(xy, conf)` evaluates `LR_PAIRS = [(1, 2), (3, 4), (5, 6), (11, 12)]` (eyes, ears, shoulders, hips; 0-based `(r, l)` where `r` is odd=image-R and `l` is even=image-L):
     - `w = min(conf[r], conf[l])`
     - `score += w * (xy[r][0] - xy[l][0])`
     - `sep += w * abs(xy[r][0] - xy[l][0])`
     - `torso` = distance between mean confident (`>= 0.3`) shoulders and hips.
     - If `wsum <= 0` or `torso < 15` or `sep / wsum < 0.12 * torso` (`LR_MIN_SEP = 0.12`): returns `"uncertain"` (no swap; attaches tool flag `UNCERTAIN_CLASS_LR`).
     - If `score >= 0`: returns `"ok"`.
     - If `score < 0`: swaps **all 8 pairs** `(1,2), (3,4), ..., (15,16)` together, preserving limb chain continuity, and returns `"swapped"` (`LR_SWAPPED_THEO_ANH`).

---

## 5. Visibility / State Attributes & Pixel Tolerances

### 5.1 CVAT Point States (`w2-face50-pose17.md` §5, `week2.py:_shape`)
Every skeleton must have all 17 points with explicit state (no missing/extra points, Shape mode only):

| State | CVAT Flags (`_shape`) | CVAT Hotkey | Definition & Rules (BTC V1 + G06 Policy) |
|---|---|---|---|
| **Visible** (`bình thường`) | `occluded: false`, `outside: false` | *(none)* | Clearly visible. Closed eyes (if eyelid seam is identifiable) and transparent glasses (if eyes visible) remain **Visible** (BTC). Two `visible` points MUST NOT share identical coordinates. |
| **Occluded (`v1`)** | `occluded: true`, `outside: false` | **`Q`** | Inside frame, occluded (sunglasses, hair, hands, steering wheel, seat, self-occlusion), **but position can be inferred within ±20 px** from adjacent joints, pose, and body proportions. Place at estimated position + `Q`. **Default for head (`1–5`), shoulders (`6–7`), hips (`12–13`)** when occluded inside frame (never `v0` for occlusion). |
| **Outside (`v0`)** | `occluded: false`, `outside: true` | **`O`** | Point lies outside the image frame, **OR** for limbs (`8–11, 14–17`: elbows, wrists, knees, ankles) is so completely hidden (e.g., under newspaper/laptop/seat/steering wheel with no adjacent segment visible) that position cannot be estimated. **BTC rule:** `outside` points do NOT use coordinates; do NOT drag out-of-bounds points onto the image border. |
| **Hidden** | *(prohibited)* | **`H`** | **PROHIBITED** as a substitute for `Q` — `hidden` is not persisted to the CVAT server. |

### 5.2 Auto-Draft State Thresholds (`src/cvat_tools/pose/person17.py`)
- `Q_CONF = 0.5`: `conf < 0.5` → `"occluded"`; `conf >= 0.5` → `"visible"`.
- `V0_CONF = 0.3`: for `LIMB_IDX = {7, 8, 9, 10, 13, 14, 15, 16}` (elbows, wrists, knees, ankles), `conf < 0.3` → `"outside"` even inside frame.
- `BORDER_PX = 8`: `(x <= 0.5 and y <= 0.5)` or outside `[0, w] × [0, h]`, OR (`conf < 0.3` and within `8 px` of any border) → `"outside"`.
- Non-limb keypoints (`{0..6, 11, 12}`: nose, eyes, ears, shoulders, hips) never become `"outside"` solely for low confidence inside the frame (excluding the `8 px` border strip).

### 5.3 Exact Pixel Tolerances (`w2-face50-pose17.md` §3, §5, §7, §8)
- **Visible keypoints:** **`±5 px`**
- **Occluded keypoints:** **`±20 px`**
- *(Open question in §8 Q6: BTC guideline lists pose resolution as `960×540` whereas Job 1623 images are `1280×1024`; pending mentor confirmation on whether pixel tolerances scale.)*

---

## 6. Discrepancies Between Code (`person17.py`, `eval_pose17.py`, `gold.py`, `w2_qc_rules.py`, `week2.py`) and `w2-face50-pose17.md`

1. **`scripts/eval_pose17.py` (`NAMES`, lines 25–26) uses anatomical T/P labels instead of BTC image-based R/L:**
   - Code: `NAMES = ["mũi", "mắt T", "mắt P", "tai T", "tai P", "vai T", "vai P", "khuỷu T", "khuỷu P", "cổ tay T", "cổ tay P", "hông T", "hông P", "gối T", "gối P", "cổ chân T", "cổ chân P"]`.
   - Guideline (`w2-face50-pose17.md` §3): sublabel `2` (`COCO[1]`) is **`mắt R`** (image right) and `3` (`COCO[2]`) is **`mắt L`** (image left), etc.
   - Impact: Numeric `sigmas` and OKS are unaffected because pair sigmas are symmetric, but printed per-keypoint error keys invert `T` and `P` relative to BTC V1.
2. **`src/cvat_tools/pose/person17.py` (`plausibility_pose`, lines 174–175) also names limbs anatomically (`T`/`P`):**
   - `(5, 7)` is labeled `"cánh tay trên T"` and `(6, 8)` `"cánh tay trên P"`, etc., because `plausibility_pose` runs on raw model coordinates before `enforce_image_lr()` in `week2.py:167–170`. Only affects `reject` message text.
3. **`scripts/eval_pose17.py` & `src/cvat_tools/pose/gold.py` ignore visibility states (`visible` / `occluded` / `outside`) and `±5 px` / `±20 px` tolerances:**
   - `gold.py:34–45` extracts only `(x, y)` tuples into `metrics/gold.json` without `occluded`/`outside` state.
   - `eval_pose17.py:34–55` computes `area` and `OKS`/`mean_px` over all present points without filtering out `outside` points (even though BTC V1 states `outside` points do not use coordinates) and does not break down pass/fail rates against `±5 px` (visible) and `±20 px` (occluded).
4. **Global vs per-pair image R/L check & flag naming (`person17.py` vs `w2-face50-pose17.md` & `w2_qc_rules.py`):**
   - `person17.enforce_image_lr` makes a single global swap decision using weighted `x_R - x_L` over `LR_PAIRS = [(1,2), (3,4), (5,6), (11,12)]` and never inspects limb pairs `(7,8), (9,10), (13,14), (15,16)` when deciding to swap. By contrast, `w2_qc_rules.py:131–135` checks every pair `2/3..16/17` individually for `R["x"] <= L["x"]` (`PROBABLE: pose_lr_swapped`).
   - `person17.py:225` emits internal flag `"UNCERTAIN_CLASS_LR"`, whereas BTC CVAT issue taxonomy (`w2-face50-pose17.md` §5B) uses `UNCERTAIN_CLASS` (acknowledged in §5A.G).
5. **`BORDER_PX = 8` + coordinate clamping vs `w2_qc_rules.py` & `w2-face50-pose17.md`:**
   - `person17.py:154–156` marks any point with `conf < 0.3` within `8 px` of an edge as `"outside"`, and `frame_people` (`line 223`) clamps `(x, y)` to `[0, w] × [0, h]`. Consequently, `w2_qc_rules.py:137–140` can flag those auto-drafted `outside` points as `PROBABLE: pose_outside_but_inside_frame`, and `w2-face50-pose17.md` §5 line 113 instructs human annotators not to drag outside points onto the border.
6. **Legacy `week2.py:person_frame` vs `_person17_frame`:**
   - `week2.py:114–127` (`person_frame`) delegates to `spm.draft.person_drafts` without 4-way rotation, `V0_CONF` limb `outside`, or `enforce_image_lr`; the active pipeline `_person17_frame` (`week2.py:160–170`) uses `person17.py`.
7. **Skeleton edge count (`schema.json` vs `labels.json`):**
   - `schema.json` has 19 edges (includes `[2, 3]` eye-to-eye), whereas CVAT `person_vf17` (`labels.json`) has 18 edges (no `[2, 3]`).
8. **`MIN_PERSON_PX = 60` & image size mismatch (`w2-face50-pose17.md` §8 Q6, Q8):**
   - `person17.py:22,116` hardcodes `MIN_PERSON_PX = 60`, whereas BTC V1 has not confirmed a minimum pixel threshold; Job 1623 images are `1280×1024` vs `960×540` stated in BTC V1.
