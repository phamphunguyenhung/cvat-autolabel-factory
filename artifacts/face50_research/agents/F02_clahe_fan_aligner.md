# F02 — CLAHE + FAN2D + BrowEdgeSnap Aligner Report (Job 1975 / Task 473)

**Mode:** Read-only on CVAT (`write_enabled=False`) and `src/`.  
**Output JSON:** `artifacts/face50_research/fan_candidates_1975.json`  
**Comparison Renders (12 frames):** `artifacts/face50_research/evidence/candidates/`

---

## 1. Pipeline Configuration

1. **Photometric Pre-processing (30 frames `90..119`, `G06_091.jpg..G06_120.jpg`):**
   - Computed BT.601 grayscale mean luma per frame.
   - Gamma LUT: `gamma = 0.55` for dark IR (`mean_luma < 50.0`, 10 frames: `92, 94, 95, 102, 104, 106, 110, 111, 112, 116`) and `gamma = 0.65` for RGB/bright (`mean_luma >= 50.0`, 20 frames).
   - LAB-space CLAHE on L channel: `clipLimit=3.0, tileGridSize=(8, 8)`.
2. **Landmark Detection:**
   - `cvat_tools.pose.face50.FaceLandmarker().landmarks68(enh, try_rotations=True)` + `map68_to_50(det['p68'])`.
3. **Post-Alignment Refinement:**
   - **BrowEdgeSnap:** Searches bright-to-dark upper brow edge gradient along face-local down vector `v` around keypoints `0..4` (`longmaytrai`) and `5..9` (`longmayphai`), then fits a degree-2 polynomial in face-local `(u, v)` coordinates (with span guard `ptp(s) >= 6.0` px for steep profiles).
   - **Inner-Lip Containment:** Nudges inner-lip keypoints (`42..49`) toward mouth center until `cv2.pointPolygonTest(outer_poly, pt, True) >= 1.05` px (falling back to max inscribed distance when closed lips are `< 2 px` thick).

---

## 2. Detection Rate & Rotations

| Metric | Value | Details |
|---|---:|---|
| Total frames processed | **30** (`90..119`) | 20 RGB/bright (`gamma=0.65`), 10 dark IR (`gamma=0.55`) |
| Detected faces | **29 / 30 (96.7%)** | Only **`f102`** (`luma=29.89`, hands occluding face) returned `None` |
| Empty CVAT frame recovered | **`f106`** (`luma=15.07`) | `face_score=0.9987`, `rot=90°`, `mean_kp_score=0.7988` |
| Rotation distribution | `0°`: **17**, `90°`: **3**, `180°`: **1**, `270°`: **8** | `90°`: `f092, f106, f116`; `180°`: `f095` (false positive); `270°`: `f096, f097, f098, f100, f104, f105, f112, f118` |
| Inner-lip containment | **29 / 29 inside `moingoai`** | `0` points outside (`dist < 0`); 3 tight closed-mouth frames (`f098: 0.417px`, `f104: 0.935px`, `f111: 0.071px`) capped by lip thickness |

---

## 3. Drift Metrics

### A. vs `gold.json` (Frame 93 — 45 labeled gold keypoints)
- **After BrowEdgeSnap + InnerLip:** `mean_px = 4.456 px`, `max_px = 13.057 px` (`kp 31`), `NME = 0.0315`, `brow_mean_px = 6.207 px`.
- **Pre-BrowEdgeSnap (`map68_to_50` raw):** `mean_px = 4.764 px`, `max_px = 13.057 px` (`kp 31`), `NME = 0.0337`, `brow_mean_px = 5.919 px`.
- Note: Overall `f093` mean error improved slightly (`4.764 -> 4.456 px`), though BrowEdgeSnap added `+0.288 px` mean brow drift on `f093` due to localized brow-hair contrast shifts (`-3.84` to `+3.66 px`).

### B. vs Current Live CVAT (`job_1975_live_pre_goal.json`, 28 annotated frames compared)
- **All 28 compared frames:** `mean_of_mean_drift_px = 11.017 px`, `median_of_mean_drift_px = 3.216 px`, `max_frame_drift_px = 331.042 px` (`f095`).
- **Excluding 2 false/degraded IR detections (`f095`, `f110`) -> 26 clean frames:**
  - `mean_of_mean_drift_px = 3.676 px`, `median_of_mean_drift_px = 3.098 px`, `max_frame_mean = 8.690 px` (`f104`).

---

## 4. Per-Frame Summary (Target Comparison Frames + Outliers)

| Frame | Image | Luma | Gamma | Det | Score | Rot | Mean Drift vs CVAT (px) | Max Drift (px) | Visual / Alignment Notes |
|---:|---|---:|---:|---|---:|---:|---:|---:|---|
| 91 | `G06_092.jpg` | 101.4 | 0.65 | True | 1.000 | 0° | 6.239 | 12.640 | Clean alignment; sunglasses glare slightly lifts `5..9` |
| 93 | `G06_094.jpg` | 89.8 | 0.65 | True | 1.000 | 0° | 4.785 | 13.472 | Gold frame (`mean=4.456px`, `NME=0.0315` vs `gold.json`) |
| 94 | `G06_095.jpg` | 16.5 | 0.55 | True | 0.990 | 0° | 3.180 | 20.320 | Very dark IR recovered cleanly by CLAHE+Gamma |
| 95 | `G06_096.jpg` | 27.1 | 0.55 | True | 0.773 | 180° | 177.215 | 331.042 | **FALSE POSITIVE:** SFD missed upright face at 0°, picked torso box at 180° |
| 99 | `G06_100.jpg` | 116.8 | 0.65 | True | 1.000 | 0° | 1.781 | 4.417 | Tight match with CVAT; inner lip valid |
| 100 | `G06_101.jpg` | 98.5 | 0.65 | True | 0.999 | 270° | 4.773 | 10.358 | **Improved vs CVAT:** uncollapses `matphai` (`22..29`) off nose bridge |
| 101 | `G06_102.jpg` | 88.3 | 0.65 | True | 1.000 | 0° | 2.715 | 8.737 | **Improved brows:** `0..9` hug upper brow edge closer than CVAT |
| 102 | `G06_103.jpg` | 29.9 | 0.55 | False | — | — | — | — | 0 CVAT shapes; hands adjusting glasses block face detection |
| 106 | `G06_107.jpg` | 15.1 | 0.55 | True | 0.999 | 90° | — | — | **Recovered 0-shape dark IR frame** (`luma=15.1`); clean 50-pt fit |
| 108 | `G06_109.jpg` | 96.2 | 0.65 | True | 1.000 | 0° | 1.902 | 7.696 | **Improved brows:** `0..9` sit cleanly on upper brow edge |
| 110 | `G06_111.jpg` | 29.2 | 0.55 | True | 0.846 | 0° | 35.690 | 68.604 | Low `mean_kp_score=0.452`; degraded dark-IR alignment |
| 111 | `G06_112.jpg` | 33.4 | 0.55 | True | 0.950 | 0° | 3.649 | 30.789 | Good overall face alignment; minor `kp 0` outer brow shift |
| 116 | `G06_117.jpg` | 21.8 | 0.55 | True | 1.000 | 90° | 7.193 | 23.296 | Strong 90° IR detection; eyes inside glasses lenses |
| 118 | `G06_119.jpg` | 60.5 | 0.65 | True | 1.000 | 270° | 6.852 | 50.503 | **Major fix vs CVAT:** recovers `8,9` out of sky & uncollapses `22..29` |

---

## 5. Key Findings for Downstream Integration

1. **High-value candidate frames:** `f106` (currently empty in CVAT), `f100`, and `f118` (currently broken `longmayphai`/`matphai` in CVAT) have `face_score >= 0.9987` and visually verified landmark geometry.
2. **Quality gate threshold needed:** Rejecting candidates with `face_score < 0.90` or `mean_kp_score < 0.55` cleanly filters out both false/degraded detections (`f095`: `face_score=0.773, rot=180°`; `f110`: `face_score=0.846, mean_kp_score=0.452`).
3. **Strict read-only compliance:** No writes to CVAT or `src/`.
