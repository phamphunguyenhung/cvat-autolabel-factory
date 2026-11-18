# F03 — Face50 Topology & Lip/Eye Audit Report (Job 1975 / Task 473)

- **Source:** Live CVAT read-only (`Cvat.from_env('edufun', write_enabled=False)`), `30` frames (`90..119`), `196` shapes (`source=manual` across all 28 annotated frames; `0` shapes on `102, 106`).
- **Cross-references:** [`gold.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/week02/task473-face/job1975-face50/metrics/gold.json), [`issues.md`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/week02/issues.md) (E1, E2), [`1975_90_104.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/reports/w2_vlm/1975_90_104.json), [`1975_105_119.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/reports/w2_vlm/1975_105_119.json).
- **Machine-readable output:** [`F03_audit.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/agents/F03_audit.json).

---

## 1. Executive Summary

### A. Raw `cvat_tools.pose.face50_engine.validate_face50_frame` Output (Live CVAT)
- **0 findings (`23` frames):** `90, 91, 92, 93, 96, 97, 98, 99, 101, 103, 104, 105, 107, 108, 109, 110, 112, 113, 114, 115, 116, 117, 119`
  *(Note: frames `96, 99, 101, 104, 107, 108` reflect previously synced surgical patches on CVAT: `kp 42` nudged inside `moingoai` on `99, 101, 108`, and `V/Q` visibility updated on `96, 104, 107`.)*
- **`INNER_LIP_OUTSIDE_OUTER` (`5` frames):** `94, 95, 100, 111, 118`
- **`MISSING_ANNOTATION` (`2` frames):** `102, 106`
- **Zero occurrences on live CVAT** of `LIP_INVERSION_LOCAL`, `EYE_LID_INVERSION_LOCAL`, `EYE_CLUSTER_COLLAPSE`, `NOSE_NON_MONOTONIC_LOCAL`, `BROW_EXTREME_DRIFT`, `COORD_OOB`, `Q_AND_O_CONFLICT`, `SKELETON_BULK_OCCLUDED`, or `KP_COUNT_MISMATCH`.

### B. Holistic 4-Bucket Classification (Validator + Deep Topology + Visibility + `issues.md` E1/E2)

| Bucket | Count | Frames | Key Issues |
|---|---:|---|---|
| **1. Clean (0 findings)** | **12** | `91, 93, 99, 101, 103, 108, 109, 113, 114, 115, 117, 119` | `validate_face50_frame=0`, clean rings & monotonic brows, E1/E2 `pass` (`f91` has `Q=16` on `14..29`; `f114` flagged in `issues.md` F5 for human double-check despite `E2=pass`) |
| **2. Minor/Geometric errors** | **10** | `90, 94, 95, 96, 97, 98, 100, 105, 111, 118` | `5` `INNER_LIP_OUTSIDE_OUTER` (`94, 95, 100, 111, 118`), `3` self-intersecting lip rings (`94, 96, 111`), `1` sub-threshold inner-lip escape (`105`: `-0.22px`), `2` non-monotonic brows (`90, 100`), `2` brow-below-eye (`111, 118`), `1` sky-drifted brow (`118`: kps `8,9` marked `Q` instead of `O`), eye cluster compression / offset (`97, 98, 100, 105`) |
| **3. Visibility/Occlusion errors** | **6** | `92, 104, 107, 110, 112, 116` | Sunglasses (`104`: `14..29` `Q`, `Q` vs `O` check + `51.2x34.9px` compact face), hands over mouth/face (`107`: `11..13, 30..49` `Q`, `Q` vs `O` check), dark IR `LOW_VISIBILITY` (`92, 110, 112, 116` with `luma` `15.7..47.3` and `V=50/Q=0`; `112` also has `47.0x38.0px` compression & `-0.16px` `kp 42`) |
| **4. Missing annotations** | **2** | `102, 106` | `0` shapes (`MISSING_ANNOTATION`); dark IR (`luma=29.9` and `15.1`), `102` occluded by hands/glasses, `106` 90° horizontal fisheye with glasses |

---

## 2. Gold Reference (`gold.json`) & `issues.md` (E1, E2) Cross-Check

### Frame 93 vs `week02/task473-face/job1975-face50/metrics/gold.json`
- `gold.json` contains **45 / 50** keypoints for frame `93` (`G06_094.jpg`, `1280x720`, `angle=1.0°`); **5 keypoints are omitted in `gold.json`**: `[2, 10, 11, 12, 13]` (`longmaytrai` mid-point `2` and all 4 `songmui` nose-bridge points `10..13`).
- Across the **45** matched keypoints:
  - `within_5px`: **45 / 45** (`100%`)
  - `mean_l2_px`: **0.034 px**, `max_l2_px`: **1.141 px**
  - `43` keypoints match to `0.000 px`; only `kp 15` (`1.141 px`: live `(565.542, 336.032)` vs gold `(564.841, 336.932)`) and `kp 16` (`0.411 px`: live `(575.700, 334.768)` vs gold `(575.799, 335.167)`) differ.

### `issues.md` (E1 & E2) Reconciliation
- **Batch E1 (`90..104`):** `5` pass (`91, 93, 99, 101, 103`), `10` uncertain (`90, 92, 94, 95, 96, 97, 98, 100, 102, 104`). Every uncertain frame maps to an active geometric (`90, 94, 95, 96, 97, 98, 100`), visibility (`92, 104`), or missing (`102`) finding.
- **Batch E2 (`105..119`):** `7` pass (`108, 109, 113, 114, 115, 117, 119`), `3` refine (`105, 107, 118`), `5` uncertain (`106, 110, 111, 112, 116`). Every refine/uncertain frame maps to a geometric (`105, 111, 118`), visibility (`107, 110, 112, 116`), or missing (`106`) finding.

---

## 3. Validator Blind Spots Found During Deep Audit

1. **Containment tolerance (`d < -0.3`):** Misses slight inner-lip escapes on `f105` (`kp 42: -0.22 px`) and `f112` (`kp 42: -0.16 px`).
2. **Self-intersecting polygons:** Not checked by `validate_face50_frame`; occurs on `f94` (`moitrong`), `f96` (`moingoai`), and `f111` (`moitrong`).
3. **Relative `BROW_EXTREME_DRIFT` (`brow_r_span > 1.25 * eye_span`):** On `f118`, `kps 8, 9` (`(267,76)`, `(282,66)`) drift into the bright window sky (`brow_r_span = 59.0 px` vs `brow_l_span = 30.7 px`), but `kp 26` (`(263,87)`) also drifted outward so `1.25 * eye_span = 83.7 px` masked the drift.
4. **Brow monotonicity & vertical order:** `validate_face50_frame` does not check brow point order along face-local `u` (`f90`, `f100`, `f107`, `f112` fail) or brow-above-eye order along `v` (`f111`, `f118` fail).
5. **IR dark & compact-face compression:** `validate_face50_frame` does not flag low luma or compressed `< 55 px` face boxes (`f104`: `51.2x34.9 px`, `f112`: `47.0x38.0 px`, `luma < 35` on `94, 95, 102, 104, 106, 110, 111, 112, 116`).

---

## 4. Complete 30-Frame Audit Table

| Frame | Image | Res | Luma | Angle | V/Q/O | `validate_face50_frame` | Deep / E1-E2 Observations | Bucket |
|---:|---|---|---:|---:|---|---|---|---|
| `90` | `G06_091.jpg` | `640x480` | `101.6` | `-13.4°` | `50/0/0` | `0` | `longmaytrai` non-monotonic (`13.0px`); E1: mouth ~10-15px high / beard | **Minor/Geometric** |
| `91` | `G06_092.jpg` | `640x480` | `101.4` | `-14.0°` | `34/16/0` | `0` | Eyes `14..29` marked `Q`; clean topology; E1: pass | **Clean** |
| `92` | `G06_093.jpg` | `1280x1024` | `47.3` | `79.1°` | `50/0/0` | `0` | Dark IR, ~90° fisheye; E1: `LOW_VISIBILITY` (lids/lips unclear) | **Visibility/Occlusion** |
| `93` | `G06_094.jpg` | `1280x720` | `89.8` | `1.0°` | `50/0/0` | `0` | `gold.json` match (`45/45` ≤ `1.14px`, `mean=0.034px`; `[2,10..13]` omitted in gold) | **Clean** |
| `94` | `G06_095.jpg` | `1280x1024` | `16.5` | `16.1°` | `50/0/0` | `INNER_LIP_OUTSIDE_OUTER` (`46: -1.05`) | `moitrong` self-intersects; dark IR + glasses frame on eyes (E1) | **Minor/Geometric** |
| `95` | `G06_096.jpg` | `1280x1024` | `27.1` | `0.1°` | `50/0/0` | `INNER_LIP_OUTSIDE_OUTER` (`42: -4.83, 46: -4.00`) | Dark IR, flat eyes, mouth shifted toward chin (E1/F5) | **Minor/Geometric** |
| `96` | `G06_097.jpg` | `960x540` | `70.4` | `-47.7°` | `50/0/0` | `0` | `moingoai` self-intersects (`minLipD=-0.00`); E1/F5: brow/eye offset, mouth on chin | **Minor/Geometric** |
| `97` | `G06_098.jpg` | `960x540` | `64.3` | `-69.3°` | `50/0/0` | `0` | Head tilted (`eR=4.8x8.4px`); E1/F5: eyes on glasses frame, mouth shifted | **Minor/Geometric** |
| `98` | `G06_099.jpg` | `960x540` | `90.1` | `-46.6°` | `50/0/0` | `0` | `eye_center_dist=26.7px`, `eye_inner_gap=15.5px`, `bR=7.8px`; E1: eyes overlapping | **Minor/Geometric** |
| `99` | `G06_100.jpg` | `640x480` | `116.9` | `4.0°` | `50/0/0` | `0` | Clean (`kp 42` fixed & synced); E1: pass | **Clean** |
| `100` | `G06_101.jpg` | `960x540` | `98.5` | `-35.8°` | `50/0/0` | `INNER_LIP_OUTSIDE_OUTER` (`42: -1.49, 47: -1.11`) | `longmayphai` non-monotonic (`5.3px`), `eye_center_dist=25.1px`; beard/mouth (E1/F5) | **Minor/Geometric** |
| `101` | `G06_102.jpg` | `1280x720` | `88.3` | `-1.6°` | `50/0/0` | `0` | Clean (`kp 42` fixed & synced); E1: pass | **Clean** |
| `102` | `G06_103.jpg` | `1280x1024` | `29.9` | `0.0°` | `0/0/0` | `MISSING_ANNOTATION` | `0` shapes; dark IR, hands & glasses occlude face (E1/B3/F2) | **Missing** |
| `103` | `G06_104.jpg` | `640x480` | `82.9` | `-16.6°` | `50/0/0` | `0` | Clean topology; E1: pass (notes ~5-8px minor left-eye shift) | **Clean** |
| `104` | `G06_105.jpg` | `512x424` | `21.5` | `-55.9°` | `34/16/0` | `0` | Dark sunglasses (`14..29` `Q`), dark IR, `51.2x34.9px` compact (`eye_dist=18.1px`); E1/F5 `Q` vs `O` | **Visibility/Occlusion** |
| `105` | `G06_106.jpg` | `960x540` | `66.8` | `-59.1°` | `50/0/0` | `0` | `kp 42` at `-0.22px` (sub-threshold); E2/F5 refine: eyes/brows compressed (`eye_dist=33.2px`) | **Minor/Geometric** |
| `106` | `G06_107.jpg` | `1280x1024` | `15.1` | `0.0°` | `0/0/0` | `MISSING_ANNOTATION` | `0` shapes; very dark IR, 90° horizontal fisheye with glasses (E2/B1/F2) | **Missing** |
| `107` | `G06_108.jpg` | `640x480` | `104.9` | `-7.3°` | `27/23/0` | `0` | Hand covers mouth/nose (`11..13, 30..49` `Q`), `longmaytrai` non-monotonic (`11.0px`); E2/F6 `Q` vs `O` | **Visibility/Occlusion** |
| `108` | `G06_109.jpg` | `1280x720` | `96.2` | `1.5°` | `50/0/0` | `0` | Clean (`kp 42` fixed & synced); E2: pass | **Clean** |
| `109` | `G06_110.jpg` | `640x480` | `90.6` | `-12.1°` | `50/0/0` | `0` | Clean topology; E2: pass | **Clean** |
| `110` | `G06_111.jpg` | `1280x1024` | `29.2` | `37.9°` | `50/0/0` | `0` | Very dark IR (`luma=29.2`); E2: `LOW_VISIBILITY` (brow/eye/lip unclear) | **Visibility/Occlusion** |
| `111` | `G06_112.jpg` | `1280x1024` | `33.4` | `28.9°` | `50/0/0` | `INNER_LIP_OUTSIDE_OUTER` (`42: -1.64, 46: -0.53`) | `moitrong` self-intersects, `brow_below_eye_local`; dark IR & head turn (E2) | **Minor/Geometric** |
| `112` | `G06_113.jpg` | `512x424` | `15.7` | `-55.5°` | `50/0/0` | `0` | Very dark IR, `47.0x38.0px` compression (`eye_dist=15.5px`), `bR=0.6px` non-monotonic, `kp 42` `-0.16px` (E2/F7) | **Visibility/Occlusion** |
| `113` | `G06_114.jpg` | `640x480` | `98.8` | `-6.8°` | `50/0/0` | `0` | Clean topology; E2: pass | **Clean** |
| `114` | `G06_115.jpg` | `640x480` | `97.9` | `-16.1°` | `50/0/0` | `0` | Clean topology; E2: pass (medium conf; `issues.md` F5 lists for human check) | **Clean** |
| `115` | `G06_116.jpg` | `640x480` | `102.8` | `-7.2°` | `50/0/0` | `0` | Clean topology; E2: pass | **Clean** |
| `116` | `G06_117.jpg` | `1280x1024` | `21.8` | `89.0°` | `50/0/0` | `0` | Dark IR, 89.0° horizontal fisheye with glasses; E2: uncertain + A4 L/R check | **Visibility/Occlusion** |
| `117` | `G06_118.jpg` | `640x480` | `90.6` | `-15.7°` | `50/0/0` | `0` | Clean topology; E2: pass | **Clean** |
| `118` | `G06_119.jpg` | `960x540` | `60.5` | `-49.5°` | `40/10/0` | `INNER_LIP_OUTSIDE_OUTER` (`42: -0.63, 46: -1.20`) | `longmayphai` kps `8,9` drifted to window sky (`Q` instead of `O`, `brow_r_span=59.0px`); `brow_below_eye_local` | **Minor/Geometric** |
| `119` | `G06_120.jpg` | `640x480` | `90.0` | `-15.0°` | `50/0/0` | `0` | Clean topology (open mouth); E2: pass | **Clean** |
