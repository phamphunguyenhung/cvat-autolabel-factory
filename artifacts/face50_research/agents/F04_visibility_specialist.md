# F04 — Face50 Occlusion & Visibility Specialist Report (Job 1975 / Task 473)

- **Role:** F04 — Face50 Occlusion & Visibility Specialist (`V` / `Q` / `O`)
- **Mode:** Read-only audit (no CVAT or `src/` edits)
- **Primary Sources:**
  - [`job_1975_live_pre_goal.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/snapshots/job_1975_live_pre_goal.json) (`30` frames `90..119`, `28` annotated / `1,400` keypoints, `2` missing: `102, 106`)
  - [`F03_audit.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/agents/F03_audit.json)
  - [`issues.md`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/week02/issues.md) (A4, B1, B3, E1, E2, F2, F5–F8)
  - [`w2-face50-pose17.md`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/weeks/guidelines/w2-face50-pose17.md) (§2.1, §4, §5, §5A, §5B)
  - Visual inspection of all 30 frame crops in `artifacts/face50_research/evidence/crops/` and `00_FACE50_CONTACT_SHEET.jpg`

---

## 1. BTC V1 Visibility Decision Framework (`V` vs `Q` vs `O`)

| State | CVAT Flag | BTC V1 Rule ([`w2-face50-pose17.md`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/weeks/guidelines/w2-face50-pose17.md)) | Face50 Application Rules |
| :--- | :--- | :--- | :--- |
| **`V` (Visible)** | `occluded=False, outside=False` | **§5, §5A.C, §5A.E:** Landmark clearly seen within `±5 px`. Includes **closed/squinted eyes** if eyelid crease is identifiable, and **clear glasses** if eye contour is visible. | Default when unobstructed and resolvable after CVAT brightness/zoom (`≥ 300%`). |
| **`Q` (Occluded)** | `occluded=True, outside=False` | **§5, §2.1, §5A.B/C/F:** Obscured by external object (hand, dark sunglasses, thick rim/glare, beard), self-occlusion (far eye/brow/mouth corner in strong profile), or extreme dark/blurry IR (`LOW_VISIBILITY`), **yet inside frame and inferable within `±20 px`** from adjacent features/symmetry/glasses frame. | **Group + BTC V1 priority for Face:** *"toàn bộ 50 điểm face: ưu tiên Visible hoặc Occluded, gần như không bao giờ v0."* Even below §2.1 visibility thresholds (`<4/8` eyes/inner lip, `<3/5` brow, `<6/12` outer lip, `<2/4` nose), keep all points `Q` if visual basis remains, and log `ATTRIBUTE_CHECK`. |
| **`O` (Outside)** | `outside=True` | **§5, §2.1, §5A.D:** Outside image bounds (`x<0, x>W, y<0, y>H`), **or** occluded with **zero visual basis** to infer within `±20 px`. Coordinates of `O` points are unused. | **0 `O` points across all 30 frames of Job 1975.** All 30 faces are fully inside bounds (`near_edge=[]` on all 28 annotated frames). **Never** assign `O` merely because a buggy draft point drifted into background sky (e.g., `f118` kps `8,9`). |

### Live Baseline vs. F04 Audit Summary (`30` Frames = `1,500` Target Keypoints)
- **Live CVAT (`job_1975_live_pre_goal.json`):** `28` annotated frames (`1,400` kps: `1,335 V`, `65 Q` across `f091, f104, f107, f118`, `0 O`) + `2` missing frames (`f102, f106`).
- **F04 Audit Result:**
  - **Visibility already compliant (`13` frames):** `f091` (`34/16/0`), `f093`, `f099`, `f101`, `f103`, `f108`, `f109`, `f113`, `f114`, `f115`, `f117`, `f119` (`50/0/0`), plus `f104` (`34/16/0` core eye occlusion compliant; optional `Q` on `5..10` in dark profile).
  - **Missing frames requiring full new annotation + `V`/`Q` assignment (`2` frames):** `f102`, `f106`.
  - **Frames with visibility (`V` ↔ `Q`) updates recommended (`14` annotated frames, plus optional/borderline refinements):**
    - High-priority dark IR / profile / occlusion mismatches (`10` frames): `f092`, `f094`, `f095`, `f097`, `f098`, `f100`, `f105`, `f110`, `f111`, `f112`, `f116`, `f118` (and minor `f107` kp `0` finger edge, `f096` far eye behind thick rim, `f090` optional beard check).
  - **`O` (`outside`) recommended anywhere in Job 1975:** **`0` keypoints** (`0 / 1,500`).

---

## 2. Deep-Dive Audit of Focus Frame Groups

### Group A — `f102` (`G06_103.jpg`, `1280x1024`, IR `luma=29.9`, Live: `MISSING`)
- **Visual Observation:** Driver is present, upright, adjusting glasses with both hands. Left-of-image hand/knuckles cover the **lower nasal bridge/base** and **100% of the mouth**, and fingertips/frame cross the **lower/outer left-of-image eye (`mattrai`)**. Right-of-image hand holds the temple away from the right-of-image eye (`matphai`) and brow (`longmayphai`).
- **Exact `V`/`Q`/`O` Recommendation (`21 V / 29 Q / 0 O` conservative; `29 V / 21 Q / 0 O` if `mattrai` upper lid resolves):**
  - `longmaytrai (0..4)`: **`V`** (`1..4` clear above knuckles; `0` borderline **`Q`** if outer tip is behind index fingertip edge).
  - `longmayphai (5..9)`: **`V`** (completely unobstructed).
  - `songmui (10..13)`: `10` = **`V`** (nasion visible between eyes); **`11, 12, 13` = `Q`** (occluded behind hand/fingers; inferable from `10` + nose root/face axis).
  - `mattrai (14..21)`: **`Q`** on **`14, 15, 19, 20, 21`** (or **all `14..21` = `Q`**) — fingertips and lowered glasses rim cross the lower/outer socket in `luma=29.9` IR.
  - `matphai (22..29)`: **`V`** if upper/lower lid crease resolves after CVAT brightness boost (`LOW_VISIBILITY`); **`Q`** if deep brow shadow hides lids.
  - `moingoai (30..41)` & `moitrong (42..49)`: **All `20` points (`30..49`) = `Q`** (placed at anatomical mouth behind hand, never on knuckles).
- **BTC V1 Backing:** §2.1 & §5 (*"Miệng bị che (tay, khẩu trang): môi bấm Q, đặt theo dáng môi ước lượng"*). Even though `0/12` and `0/8` mouth points are visible, head orientation, chin, and `kp 10` provide clear `±20 px` inference, so `Q` wins over `O` with **`ATTRIBUTE_CHECK`** raised (matching `f107`).

### Group B — `f106` (`G06_107.jpg`, `1280x1024`, IR `luma=15.1`, Live: `MISSING`)
- **Visual Observation:** Driver is lying horizontally (`~90°` rotated in fisheye IR, head on right of image, hands on stomach — **no hand on face**), wearing **dark/reflective IR glasses** with two bright IR LED glare spots on the lenses/rims at `luma=15.1`.
- **Exact `V`/`Q`/`O` Recommendation (`16 Q` minimum on eyes; `27 Q` conservative dark-IR; `0 O`):**
  - **Class Orientation (`issues.md` A4 / §5A.B):** Raise **`UNCERTAIN_CLASS`** for 90° horizontal face L/R convention (consistent with `f092` & `f116`, where `trai` is top-in-image and `phai` is bottom-in-image).
  - `mattrai (14..21)` & `matphai (22..29)`: **All `16` points (`14..29`) = `Q`**. Both eyes are invisible behind dark IR lenses + bright specular glare (`0/8` each). Per §5A.C (*"Kính râm / tròng tối: 16 điểm hai mắt Q, đặt theo hình dáng tròng kính/gọng... Nếu lóa che hết mắt: Q"*) and `EDGE_CASES.md`.
  - `longmaytrai (0..4)` & `longmayphai (5..9)`: **`Q`** if brow hair border is obscured by glasses top rim and `luma=15.1` shadow (`LOW_VISIBILITY`); `V` only if brow edge clearly resolves with CVAT brightness stretch.
  - `songmui (10..13)`: **`10` = `Q`** (under dark glasses bridge), **`11..13` = `V`** (nose silhouette faintly visible).
  - `moingoai (30..41)` & `moitrong (42..49)`: **`30..41` = `V`** (if outer lip silhouette resolves after CVAT brightness boost, `LOW_VISIBILITY`); **`42..49` = `Q`** if inner seam is blurred out at `luma=15.1` (§5A.F). **Zero `O`**.

### Group C — `f094`, `f095`, `f111` (Dark IR with Glasses + Pitch/Turn; Live: all `50/0/0`)
All three currently have `V=50, Q=0, O=0` on live CVAT and also have `INNER_LIP_OUTSIDE_OUTER` geometric defects (`F03_audit.json`). None have out-of-frame points (`0 O`).

1. **`f094` (`G06_095.jpg`, `1280x1024`, IR `luma=16.5`, `16.1°`):**
   - **Visual:** Head pitched down (`cúi đầu`), thick dark glasses rim cuts directly across `kp 10` and the lower/middle half of **`matphai` (`22..29`)** in deep IR shadow (`luma=16.5`). Above the rim, the closed/downgazing crease of `mattrai` (`14..21`) is faintly visible (though lower rim touches `19..21`).
   - **Recommended `V`/`Q`/`O` (`41 V / 9 Q / 0 O` core, or `38 V / 12 Q / 0 O` if `19..21` behind rim):**
     - `10` = **`Q`** (behind thick dark glasses bridge).
     - `22..29` (`matphai`) = **`Q`** (all 8 points: thick black rim + dark IR shadow occlude inner/lower eye boundary).
     - `14..21` (`mattrai`) = **`V`** above rim (`14..18`), **`19..21` = `Q`** if lower rim clips lower lid (or all `14..21` `V` if lid crease above rim is clear after brightness boost; log `LOW_VISIBILITY`).
     - `0..9`, `11..13`, `30..49` = **`V`** (unobstructed; fix `kp 46` containment & `moitrong` self-intersection).

2. **`f095` (`G06_096.jpg`, `1280x1024`, IR `luma=27.1`, `0.1°`):**
   - **Visual:** Head pitched strongly down (`cúi đầu`), eyes nearly closed; thick dark upper glasses rim runs right beneath/across the lower lids of **`mattrai` (`19..21`)** and across **`matphai` (`22, 26..29`)** and bridge **`10`**. Forehead top is near image top, but `0..9` are well inside frame (`O=0`).
   - **Recommended `V`/`Q`/`O` (`38 V / 12 Q / 0 O` or `41 V / 9 Q / 0 O`):**
     - `10` = **`Q`** (behind thick black glasses bridge).
     - `22..29` (`matphai`) = **`Q`** (thick black rim crosses lower/inner eye in shadow).
     - `19..21` (`mattrai` lower lid) = **`Q`** if clipped by top edge of thick rim (`14..18` = **`V`** along visible upper closed crease).
     - `0..9`, `11..13`, `30..49` = **`V`** (unobstructed; fix `42, 46` containment & mouth shift).

3. **`f111` (`G06_112.jpg`, `1280x1024`, IR `luma=33.4`, `28.9°`):**
   - **Visual:** Head pitched down AND turned right into a strong 3/4-profile (`angle=28.9°`) with glasses. The far side (`longmayphai 5..9`, `matphai 22..29`) is foreshortened and shadowed behind the nose bridge and dark glasses rim. On the near side, `mattrai (14..21)` closed crease is visible along the upper rim (`19..21` touch the dark temple/rim).
   - **Recommended `V`/`Q`/`O` (`36 V / 14 Q / 0 O` to `33 V / 17 Q / 0 O`):**
     - `longmayphai (5..9)` = **`Q`** (far brow foreshortened & blurred in IR turn; `5..6` borderline `V` if ridge resolves, `7..9` definitely `Q`).
     - `matphai (22..29)` = **`Q`** (all 8 points: far eye occluded by nose bridge + dark glasses rim/shadow).
     - `10` = **`Q`** if behind dark bridge, else `V`; `14..21` = **`V`** (`19..21` **`Q`** if covered by dark temple/rim).
     - `0..4` (fix `2..4` brow-below-eye drift), `11..13`, `30..49` (fix `42, 46` containment) = **`V`**.

### Group D — `f100` & `f118` (Extreme Profiles: Far-Side `Q` vs `V`, and `f118` Kps `8,9` vs `Outside`)

1. **`f100` (`G06_101.jpg`, `960x540`, RGB `luma=98.5`, `-35.8°`, Live: `50/0/0`):**
   - **Visual:** ~60–70° profile looking up/right with clear glasses and beard.
   - **Far-side Brow (`longmayphai 5..9`):** Inner root `5` sits just above glabella (`V` or `Q`); **`6, 7, 8, 9` = `Q`** (outer brow wraps around far forehead silhouette edge, visually compressed/occluded — per §5 *"mày, mắt, má phía xa bị che thì Q"*).
   - **Far-side Eye (`matphai 22..29`):** **All `8` points (`22..29`) = `Q`** (currently collapsed on nose bridge; anatomically, `22, 23, 29` sit behind nasal bridge/thick rim, and `24..28` are foreshortened behind the far glasses rim/orbital edge in ~65° profile).
   - **Near-side (`0..4`, `14..21`) & Nose (`10..13`):** **`V`** (note `14` or `21` **`Q`** only if dark outer rim obscures corner).
   - **Mouth (`30..49`):** Far-side corner **`35, 36, 37, 46` (and `45, 47` if behind cheek/beard turn) = `Q`**; near/center `30..34, 38..44, 48..49` = **`V`** (requires geometric fix for `42, 47` outside `moingoai` and beard placement). **Zero `O`**.

2. **`f118` (`G06_119.jpg`, `960x540`, RGB `luma=60.5`, `-49.5°`, Live: `40/10/0` with `Q=[7,8,9,23..29]`):**
   - **CRITICAL BTC V1 RULING — `f118` Kps `8, 9` (`Q` vs `O` / `outside`):**
     - `issues.md` E2 reported Haiku's suggestion to mark `8, 9` as `outside` because on the **current buggy annotation**, `8=(267,76)` and `9=(282,66)` drifted out into the bright white car window sky.
     - **Under BTC V1 §2.1 & §5, marking `8, 9` as `O` (`outside`) is INCORRECT:**
       1. `8, 9` are **inside** the `960x540` image frame (`x=267..282, y=66..76`).
       2. The driver's actual forehead and far brow ridge ARE visible inside the head contour (`x~230..250, y~85..100`) — `8, 9` only appear in the sky because of **coordinate drift**, NOT because the brow is out-of-frame or uninferable!
       3. Under §5 (*"Điểm outside không dùng đến tọa độ"* and *"toàn bộ 50 điểm face: ưu tiên Visible hoặc Occluded, gần như không bao giờ v0"*) and §2.1 (`5, 6` and brow ridge give `≥ 3/5` visual basis), **`8, 9` MUST be relocated back onto the far supraorbital rim / temple silhouette edge and kept as `Q`** (NEVER `O`).
   - **Exact Far-Side `Q` vs `V` Breakdown on `f118`:**
     - `longmayphai (5..9)`: **`5, 6` = `V`** (clearly visible along far brow ridge above glasses bridge); **`7` = `Q`** (at silhouette turn edge, borderline `V`/`Q`); **`8, 9` = `Q`** (relocated onto far temple silhouette edge, occluded by 3/4-profile curve).
     - `matphai (22..29)`: **All `8` points (`22..29`) = `Q`** (including `22`, which sits directly against/behind the thick gray glasses bridge in live crop; `23..29` must be relocated down from the upper rim into the far eye socket behind the lens/frame and kept **`Q`**).
     - `longmaytrai (0..4)`, `mattrai (14..21)`, `songmui (10..13)`: **`V`** (clear in RGB; glasses temple sits to the left of `14`).
     - `moingoai (30..41)`, `moitrong (42..49)`: **`V`** if far mouth corner silhouette against bright background resolves (`35, 36, 37, 46` = **`Q`** if far corner wraps behind cheek turn; fix `42, 46` containment error). **Zero `O`**.

### Group E — `f092`, `f110`, `f112`, `f116` (Dark IR / Compact Faces / 90° Fisheye; Live: all `50/0/0`)

1. **`f092` (`G06_093.jpg`, `1280x1024`, IR `luma=47.3`, `79.1°`):**
   - **Visual:** Horizontal ~79° fisheye IR, no glasses, no hand/book on face (shirt/shoulder behind cheek). Bottom-in-image side (`5..9`, `22..29`) is in deep IR shadow; closed eye seams and lip corners are indistinct (`E1`: `LOW_VISIBILITY`).
   - **Recommended `V`/`Q`/`O` (`21 V / 29 Q / 0 O` to `29 V / 21 Q / 0 O`):**
     - `longmayphai (5..9)` & `matphai (22..29)`: **All `13` points = `Q`** (deep shadow on lower-in-image half of face).
     - `mattrai (14..21)`: **`Q`** if closed eyelid crease cannot be confirmed within `±5 px` in dark IR (or `V` if resolved with CVAT brightness boost; `LOW_VISIBILITY`).
     - `longmaytrai (0..4)`, `songmui (10..13)`: **`V`** (`0` borderline `Q` in hair/shadow).
     - `moingoai (30..41)`, `moitrong (42..49)`: **`V`** if outer silhouette resolves after brightness boost, **`42..49` = `Q`** if closed mouth seam is unresolvable (`LOW_VISIBILITY`, `UNCERTAIN_CLASS` for ~79° rotation).

2. **`f110` (`G06_111.jpg`, `1280x1024`, IR `luma=29.2`, `37.9°`):**
   - **Visual:** Very dark IR (`luma=29.2`), strong head turn to the right + tilt (`37.9°`), glasses with a bright white IR glare streak across `10` and `22..24`.
   - **Recommended `V`/`Q`/`O` (`25 V / 25 Q / 0 O` to `17 V / 33 Q / 0 O`):**
     - `longmayphai (5..9)` & `matphai (22..29)`: **All `13` points = `Q`** (far-side turn + IR glare streak + deep shadow).
     - `10` (`songmui` top): **`Q`** (under IR glare streak/bridge); `11..13` = **`V`**.
     - `mattrai (14..21)`: **`Q`** if lower/outer lid is blurred into dark glasses temple/shadow (`14, 19..21` `Q`, or all `14..21` `Q` per `E2` `LOW_VISIBILITY`).
     - `longmaytrai (0..4)` & `moingoai (30..41)`: **`V`** (or `Q` on `42..49` inner lip seam if unresolvable in `luma=29.2` blur). **Zero `O`** (`near_edge=[]`).

3. **`f112` (`G06_113.jpg`, `512x424`, IR `luma=15.7`, `-55.5°`):**
   - **Visual:** Very dark IR (`luma=15.7`), low-res `512x424`, compact `47.0x38.0 px` face (`eye_dist=15.5 px`), extreme profile tilted back, no glasses. Far brow (`5..9`) & far eye (`22..29`) are collapsed/foreshortened away from camera.
   - **Recommended `V`/`Q`/`O` (`21 V / 29 Q / 0 O` to `17 V / 33 Q / 0 O`):**
     - `longmayphai (5..9)` & `matphai (22..29)`: **All `13` points = `Q`** (far side hidden by extreme profile + `luma=15.7` darkness).
     - `mattrai (14..21)`: **`Q`** if nearly closed tiny eye (`<10 px`) is unresolvable at `luma=15.7`, or `V` if lid slit resolves on 400%+ zoom + brightness boost.
     - `moingoai (30..41)` & `moitrong (42..49)`: Far corner **`35, 36, 37, 46` = `Q`** (wraps away in profile) + **`42..49` = `Q`** if inner seam is indistinguishable at `47x38 px` (`luma=15.7`). Fix `kp 42` (`-0.16 px`) containment. **Zero `O`**.

4. **`f116` (`G06_117.jpg`, `1280x1024`, IR `luma=21.8`, `89.0°`):**
   - **Visual:** Horizontal `89.0°` fisheye IR, **no hand on face**, wearing **dark/reflective IR glasses** with bright white IR LED reflection dots directly over both lenses (`14..29`) at `luma=21.8`.
   - **Recommended `V`/`Q`/`O` (`23 V / 27 Q / 0 O` to `15 V / 35 Q / 0 O`):**
     - **Class Check:** **`UNCERTAIN_CLASS`** for `89.0°` horizontal rotation (`issues.md` A4).
     - `mattrai (14..21)` & `matphai (22..29)`: **All `16` points (`14..29`) = `Q`** (dark IR lenses + bright IR LED reflections completely obscure eyelids — clear visibility error on live `V=50`).
     - `10` = **`Q`** (behind dark glasses bridge); `11..13` = **`V`**.
     - `longmayphai (5..9)` (and `longmaytrai 0..4` if rim/shadow hides brow hair): **`Q`** (`5..9` in deep bottom-of-face shadow; `0..4` `V` if clear above rim after brightness boost, else `Q`).
     - `moingoai (30..41)` & `moitrong (42..49)`: `30..41` = **`V`** (after brightness boost, `LOW_VISIBILITY`); `42..49` = **`Q`** if inner lip line cannot be resolved at `luma=21.8`. **Zero `O`**.

---

## 3. Complete Per-Frame `V` / `Q` / `O` Recommendations (All 30 Frames `90..119`)

> **Legend:** `Live V/Q/O` comes directly from `job_1975_live_pre_goal.json`. `Rec V/Q/O` gives the recommended target counts (with borderline IR/profile ranges noted). `O=0` on all 30 frames.

| Frame | Image | Live `V/Q/O` | Rec `V/Q/O` | Exact `Q` Keypoints Recommended (`O=[]` all frames) | BTC V1 Rule & Issue / Action |
|---:|---|---|---|---|---|
| `90` | `G06_091.jpg` | `50/0/0` | `50/0/0` *(or `45/5/0`)* | `[]` *(optional `31..35` `Q` if beard hides upper lip edge)* | **§5, §5A.C:** Clear glasses -> `V`. Fix `longmaytrai` order & verify mouth behind beard. |
| `91` | `G06_092.jpg` | `34/16/0` | **`34/16/0`** | `[14..29]` (both eyes behind dark/glare sunglasses) | **§5A.C:** **Live compliant.** Keep `14..29` = `Q`. |
| `92` | `G06_093.jpg` | `50/0/0` | **`21/29/0`** *(up to `29/21/0`)* | `[5..9, 22..29, 14..21?, 42..49?]` (`5..9, 22..29` shadow `Q`; `14..21, 42..49` `Q` if unresolvable in IR) | **§5A.B, §5A.F:** Dark IR + `79.1°` rotation. Change from `V=50`; log `LOW_VISIBILITY`, `UNCERTAIN_CLASS`. |
| `93` | `G06_094.jpg` | `50/0/0` | **`50/0/0`** | `[]` | **§5:** Gold frame (`100%` within `1.14 px`). **Live compliant.** |
| `94` | `G06_095.jpg` | `50/0/0` | **`41/9/0`** *(or `38/12/0`)* | `[10, 22..29]` *(+`19..21` if rim clips lower lid)* | **§5A.C, §5A.F:** Thick dark rim crosses `10` & `matphai` in `luma=16.5` IR. Fix `kp 46` & `moitrong` + `LOW_VISIBILITY`. |
| `95` | `G06_096.jpg` | `50/0/0` | **`38/12/0`** *(or `41/9/0`)* | `[10, 19..21, 22..29]` *(rim clips `19..21` & crosses `10, 22..29`)* | **§5A.C, §5A.F:** Thick black rim over lower/right eye in pitch-down IR. Fix `42, 46` + `LOW_VISIBILITY`. |
| `96` | `G06_097.jpg` | `50/0/0` | `42/8/0` *(or `50/0/0`)* | `[22..29]` *(if thick upper-right rim/turn obscures far eye)* | **§5A.B/C:** Mouth `Q->V` already synced; check far eye `22..29` vs rim & fix `moingoai` self-intersect. |
| `97` | `G06_098.jpg` | `50/0/0` | **`40/10/0`** *(or `42/8/0`)* | `[22..29]` *(+`8, 9` if brow tail obscured at edge)* | **§5A.C:** Heavy glare + rim over far eye `22..29` (`-69.3°` tilt). Also fix eye/mouth coords. |
| `98` | `G06_099.jpg` | `50/0/0` | **`35/15/0`** *(or `37/13/0`)* | `[5..9 (or 7..9), 22..29, 35..37?, 46?]` | **§5, §5A.B:** ~80° profile; nose bridge hides `22..29` & far brow `5..9` foreshortened. Separate eye clusters. |
| `99` | `G06_100.jpg` | `50/0/0` | **`50/0/0`** | `[]` | **§5A.E:** Closed eyes with clear lid crease -> `V`. **Live compliant.** |
| `100` | `G06_101.jpg` | `50/0/0` | **`32/18/0`** *(to `38/12/0`)* | `[6..9 (or 5..9), 22..29, 35..37, 45..47]` | **§5, §5A.B:** Extreme profile; far eye `22..29`, far brow `6..9`, far mouth corner `Q`. Fix `42, 47` & un-stack `22..29`. |
| `101` | `G06_102.jpg` | `50/0/0` | **`50/0/0`** | `[]` | **§5:** Clear glasses. **Live compliant.** |
| `102` | `G06_103.jpg` | `MISSING` | **`21/29/0`** *(to `29/21/0`)* | `[0?, 11..13, 14..21 (or 14,15,19..21), 30..49]` | **§2.1, §5, §5A.C:** Hand covers `11..13` & `30..49` (`Q`), fingertips/rim cross `mattrai`. Never `O`; log `ATTRIBUTE_CHECK`. |
| `103` | `G06_104.jpg` | `50/0/0` | **`50/0/0`** | `[]` | **§5:** Clear glasses, slight beard. **Live compliant.** |
| `104` | `G06_105.jpg` | `34/16/0` | **`34/16/0`** *(or `27/23/0`)* | `[14..29]` *(+`5..10` if dark IR profile/bridge obscures)* | **§5A.C:** Dark sunglasses `14..29` = `Q` (never `O`, §2.1). **Live `34/16/0` core compliant.** |
| `105` | `G06_106.jpg` | `50/0/0` | **`35/15/0`** *(to `39/11/0`)* | `[7..9, 22..29, 35..37?, 46?]` | **§5, §5A.B:** Extreme profile `-59.1°`; far eye `22..29` behind nose bridge & `7..9` at edge. Fix `kp 42` (`-0.22px`). |
| `106` | `G06_107.jpg` | `MISSING` | **`23/27/0`** *(to `15/35/0`)* | `[10, 14..29, 0..9?, 42..49?]` | **§5A.C/F, §5A.B:** Dark IR (`luma=15.1`) + reflective glasses + `90°` fisheye. Eyes `14..29` = `Q`. Log `UNCERTAIN_CLASS`, `LOW_VISIBILITY`. |
| `107` | `G06_108.jpg` | `27/23/0` | **`26/24/0`** *(or `25/25/0`)* | `[0 (and 1?), 11..13, 30..49]` | **§2.1, §5:** `11..13, 30..49` = `Q` (compliant, never `O`; log `ATTRIBUTE_CHECK` for F6). **Add `0` (and `1` if on finger) -> `Q`**; fix `30..49` off knuckles. |
| `108` | `G06_109.jpg` | `50/0/0` | **`50/0/0`** | `[]` | **§5:** Clear glasses. **Live compliant.** |
| `109` | `G06_110.jpg` | `50/0/0` | **`50/0/0`** | `[]` | **§5:** Clear glasses, beard doesn't hide lip border. **Live compliant.** |
| `110` | `G06_111.jpg` | `50/0/0` | **`25/25/0`** *(to `17/33/0`)* | `[5..9, 10, 22..29, 14..21 (or 14,19..21), 42..49?]` | **§5A.B/C/F:** Very dark IR (`luma=29.2`) + turn + glare over `10, 22..24`. Log `LOW_VISIBILITY`, `UNCERTAIN_BOUNDARY`. |
| `111` | `G06_112.jpg` | `50/0/0` | **`36/14/0`** *(to `33/17/0`)* | `[5..9, 22..29, 10?, 19..21?]` | **§5A.B/C/F:** Dark IR turn + glasses rim over far eye `22..29` & far brow `5..9`. Fix `2..4` & `42, 46`. |
| `112` | `G06_113.jpg` | `50/0/0` | **`21/29/0`** *(to `17/33/0`)* | `[5..9, 22..29, 14..21?, 35..37, 42..49]` | **§5A.B/F:** `47x38 px` compact face in `luma=15.7` IR + extreme profile. Far eye/brow/mouth + blurred inner lip `Q`. Fix `kp 42`. |
| `113` | `G06_114.jpg` | `50/0/0` | **`50/0/0`** | `[]` | **§5:** Hand near visor/mirror, face unobstructed. **Live compliant.** |
| `114` | `G06_115.jpg` | `50/0/0` | **`50/0/0`** | `[]` | **§5:** Unobstructed RGB. **Live compliant.** |
| `115` | `G06_116.jpg` | `50/0/0` | **`50/0/0`** | `[]` | **§5:** Hair frames cheeks, not eyes/brows/mouth. **Live compliant.** |
| `116` | `G06_117.jpg` | `50/0/0` | **`23/27/0`** *(to `15/35/0`)* | `[5..9, 10, 14..29, 0..4?, 42..49?]` | **§5A.C/F, §5A.B:** Dark IR (`luma=21.8`) + IR glare on glasses (`14..29` MUST be `Q`) + `89.0°` fisheye. Log `UNCERTAIN_CLASS`, `LOW_VISIBILITY`. |
| `117` | `G06_118.jpg` | `50/0/0` | **`50/0/0`** | `[]` | **§5A.C:** Phone at ear/cheek does not cover eyes/mouth. **Live compliant.** |
| `118` | `G06_119.jpg` | `40/10/0` | **`39/11/0`** *(or `35/15/0`)* | `[7, 8, 9, 22..29]` *(+`35..37, 46` if far corner wraps)* | **§2.1, §5, §5A.B:** **Keep `8, 9` as `Q` (relocate off sky, NEVER `O`)**; set `22` to `Q`; move `23..29` into socket; fix `42, 46`. |
| `119` | `G06_120.jpg` | `50/0/0` | **`50/0/0`** | `[]` | **§5A.E:** Smile/squint with visible eye slits & open mouth -> `V`. **Live compliant.** |

---

## 4. Escalations & Next-Step Checklist (Read-Only Summary)

1. **Mentor / Human Clarifications Required (`issues.md`):**
   - **`A4` (`UNCERTAIN_CLASS`):** 90° horizontal fisheye IR L/R convention for Face50 on **`f092`, `f106`, `f116`** (currently `trai` = top-in-image, `phai` = bottom-in-image on `f092`/`f116`).
   - **`F6` & `B3` (`ATTRIBUTE_CHECK`):** Confirm group policy (`Q` instead of `O` for 100% hand-occluded mouth) on **`f107`** and new annotation **`f102`** (`moingoai 30..41`, `moitrong 42..49`).
   - **`F7` (`LOW_VISIBILITY`):** Confirm `Q` vs `V` cutoff on sub-55 px dark IR frames (`f104`, `f112`) and `luma < 35` IR frames (`f094, f095, f106, f110, f111, f116`).
2. **Do NOT apply `V`→`Q` patches blindly on geometry-broken frames:** Frames `f094, f095, f100, f105, f107, f111, f112, f118` require coordinate repairs alongside or prior to final `V/Q` lock (especially `f118` kps `8,9` & `23..29`, `f100` `22..29`, and `f107` `30..49`).
