# F09 — Face50 Guideline & History Historian Summary (Job 1975 / Task 473)

- **Mode:** Read-only on CVAT and `src/`; UTF-8 without BOM.
- **Files Updated:**
  - [`docs/guidelines/face50/FACE50_GUIDELINE.md`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/docs/guidelines/face50/FACE50_GUIDELINE.md)
  - [`docs/guidelines/face50/FACE50_DIFFICULT_CASES.csv`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/docs/guidelines/face50/FACE50_DIFFICULT_CASES.csv)
  - [`artifacts/face50_research/agents/F09_guideline_historian.md`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/agents/F09_guideline_historian.md)

---

## 1. Guideline Updates (`FACE50_GUIDELINE.md`)

1. **Alignment & Verification Pipeline (`F50-R09..R11`):**
   - Documented `align_face50_clahe_fan(img_bgr, try_rotations=True, landmarker=None)` in `face50_engine.py`: Adaptive Gamma (`0.55` for `mean_luma < 90`; `0.45` + `clipLimit=4.0` for extreme dark hand-occluded IR `f102`) + LAB CLAHE (`clipLimit=2.5`, `tileGridSize=(8, 8)`), multi-rotation `FaceLandmarker.landmarks68(..., try_rotations=True)` + `map68_to_50`, and confidence gate (`face_score >= 0.90`, `mean_kp_score >= 0.55`).
   - Documented **`F50-R09` (`BrowEdgeSnap`)**: Sobel upper-brow edge snap (`±4 px` along face-local `v`), enforcing monotonic `u` order (`BROW_NON_MONOTONIC_LOCAL`) and placement above upper eyelids `15..17` / `23..25` (`BROW_BELOW_EYE`).
   - Documented **`F50-R10` (`LIP_SELF_INTERSECT`)**: non-adjacent polygon edge intersection checks on `moingoai` (`30..41`) and `moitrong` (`42..49`).
   - Documented **`F50-R11` (`TightInnerLipContainment` & `InnerLipClamp`)**: tightened inner-lip containment threshold from `-0.3` px to `-0.05` px in `validate_face50_frame` plus `_nudge_inner_lip_point` clamping.
2. **Resolution of Missing Frames (`f102`, `f106`):**
   - **`f102` (`G06_103.jpg`):** FAN2D returned `None` due to both hands adjusting glasses in dark IR (`luma=29.9`). Resolved via **CLAHE (`clipLimit=4.0`) + Gamma (`0.45`)** visual reading + `w2_face_propose.py` spline proportions (`16 V / 34 Q / 0 O`, `0` validation findings, `ATTRIBUTE_CHECK` logged; never `O`).
   - **`f106` (`G06_107.jpg`):** `90°` horizontal IR fisheye (`luma=15.1`) with dark/reflective glasses. Recovered via **CLAHE + Gamma (`0.55`) + FAN2D (`try_rotations=True`, `rot=90°`, `face_score=0.9987–0.9994`) + `moitrong` untangle** (`0` findings; matches `f116` `89.0°` orientation; F04 visibility recommends `Q` for `14..29` behind dark IR lenses and `UNCERTAIN_CLASS` / `LOW_VISIBILITY` alignment with `f116`).

---

## 2. Difficult Cases Matrix (`FACE50_DIFFICULT_CASES.csv`)

- **Synced & Verified (`ai_reviewed_synced_not_human_approved`, `6`):** `96, 99, 101, 104, 107, 108` (unchanged).
- **`ai_reviewed_eligible` (`6`):** `94, 95, 102, 105` *(new row `F50-CASE-105`)*, `106, 118` — all verified at `0` findings in `validate_face50_frame`.
- **`needs_human_decision` (`3`):** `100, 111, 112` *(new row `F50-CASE-112`)*.
- **`needs_mentor_decision` (`1`):** `116` (`89.0°` horizontal IR fisheye L/R convention under `F50-R07` & dark IR eyewear `Q` flags).
