# F05 — Missing Frames & Extreme Profiles Proposals (Job 1975 / Task 473)

- **Outputs:** [`F05_proposals.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/agents/F05_proposals.json)
- **Validation Gate:** Every `AI_REVIEWED_ELIGIBLE` proposal (`6` frames: `106, 102, 94, 95, 105, 118`) passed `cvat_tools.pose.face50_engine.validate_face50_frame` with **0 findings** (no errors, no warnings, no self-intersections, strict `moitrong` containment inside `moingoai`).
- **Review Queue (`3` frames):** `100, 111, 112` (retained for human review because extreme foreshortening or dark IR brow/eye geometry cannot clear `validate_face50_frame` cleanly without altering non-lip keypoints).

---

## 1. Missing Frames (`create`)

| Frame | Image | Method | Visibility (`V/Q/O`) | `validate_face50_frame` | Visual Verification |
|---:|---|---|---|---:|---|
| `106` | `G06_107.jpg` | FAN2D `rot=90°` (`face_score=0.9994`) + `moitrong` untangle | `50 / 0 / 0` | `0` findings | Verified against [`f106_G06_107.jpg_compare.png`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/candidates/f106_G06_107.jpg_compare.png); matches `f116` (`89.0°`) orientation (`mattrai` top `y≈541`, `matphai` bottom `y≈635`, `songmui` right→left). |
| `102` | `G06_103.jpg` | CLAHE (`clipLimit=4.0`) + Gamma (`0.45`) visual reading + `w2_face_propose.py` spline proportions | `16 / 34 / 0` | `0` findings | `longmaytrai` (`0..4`), `longmayphai` (`5..9`), nasion (`10`), `matphai` (`22..29`) marked `V`; occluded nose (`11..13`), `mattrai` (`14..21`), and mouth (`30..49`) behind hand/glasses marked `Q`. |

---

## 2. Surgical Proposals (`update` — `AI_REVIEWED_ELIGIBLE`)

| Frame | Image | Changed Keypoints | Root Cause & Surgical Fix | `validate_face50_frame` |
|---:|---|---|---|---|
| `94` | `G06_095.jpg` | `43, 46, 49` | Preserved `0..41` (FAN2D had compressed `moitrong` & shifted `mattrai`). Separated identical `43/49` (`±0.6px` along face-down `v`) to resolve `moitrong` self-intersection `(1, 6)`, and nudged `46` (`-1.05px`) inside `moingoai`. | `0` findings |
| `95` | `G06_096.jpg` | `42, 45, 46` | Preserved `0..41` (rejected FAN2D `rot=180°`, `drift_mean=177.2px` false detection on chest). Nudged `42` (`-4.83px`), `45`, `46` (`-4.00px`) inside `moingoai`. | `0` findings |
| `105` | `G06_106.jpg` | `42` | Preserved `0..41`. Nudged `42` (`-0.22px` sub-threshold escape) inside `moingoai`. | `0` findings |
| `118` | `G06_119.jpg` | `5..9, 22..29, 30..49` | Preserved good `longmaytrai` (`0..4`), `songmui` (`10..13`), `mattrai` (`14..21`). Replaced sky-drifted `longmayphai` (`5..9`), stretched `matphai` (`22..29`), and lip rings (`30..49`) with FAN2D `rot=270°` (`face_score=1.000`, verified in [`f118_G06_119.jpg_compare.png`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/candidates/f118_G06_119.jpg_compare.png)), plus `moitrong` untangle, `kp 9` monotonicity (`+1.2px` along `u`), and `7,8,9` set to `V` (now on visible brow ridge; `23..29` kept `Q`). | `0` findings |

---

## 3. Deferred to Human Review (`review_queue`)

- **`f100` (`G06_101.jpg`):** Extreme profile (`-35.8°`). Surgical `moitrong` fix resolves `INNER_LIP_OUTSIDE_OUTER`, but foreshortened `longmayphai` (`5..9`) still triggers `BROW_NON_MONOTONIC_LOCAL` on CVAT, while FAN2D (`rot=270°`) introduces `moingoai` self-intersection `(6, 8)`.
- **`f111` (`G06_112.jpg`):** Dark IR (`luma=33.4`). Surgical `moitrong` fix resolves `INNER_LIP_OUTSIDE_OUTER` + `LIP_SELF_INTERSECT`, but CVAT `kp 5` triggers `BROW_BELOW_EYE`, and FAN2D `moitrong` has 12 self-intersecting edge pairs.
- **`f112` (`G06_113.jpg`):** Very dark IR (`luma=15.7`) + compact `47×38px` face (`512×424`). `BROW_NON_MONOTONIC_LOCAL` (`0..9`) and sub-pixel lip compression require human inspection.
