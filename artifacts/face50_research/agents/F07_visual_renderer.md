# F07 — Visual Diff & Contact Sheet Renderer (Job 1975 / Task 473)

**Role:** Visual Diff & Contact Sheet Renderer (Read-only on CVAT and `src/`)  
**Inputs:**
- [`F05_proposals.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/agents/F05_proposals.json)
- [`job_1975_live_pre_goal.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/snapshots/job_1975_live_pre_goal.json)
- [`F03_audit.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/agents/F03_audit.json)

**Contact Sheet:**
- [`00_FINAL_CONTACT_SHEET.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/final_proposals/00_FINAL_CONTACT_SHEET.jpg) (`1520×1950`, 2×5 grid: 6 eligible proposals + 3 review queue frames + summary legend)

---

## Rendering Specification

- **Zoom:** Exact `4.0x` bicubic (`INTER_CUBIC`) crop around Face50 bounding box (`pad = max(35px, 0.35 * max(fw, fh))`).
- **Dark IR Enhancement:** Gamma `0.50` + LAB CLAHE (`clipLimit=3.0`, `tileGridSize=8×8`) applied to dark IR frames (`luma < 45.0`: `f094, f095, f102, f106, f111, f112`).
- **Style (`face50_engine.render_face50_proposals` parity):**
  - Bold polylines (`thickness=2`) with dark `(15, 15, 15)` outer halo (`thickness=4`).
  - State-colored keypoints: `V` = green, `Q` = amber, `O` = red.
  - Diff highlights: `BEFORE` changed/flagged points in magenta/red; `PROPOSED` fixes in bright cyan; `REVIEW QUEUE` unresolved warnings in orange (`NOT SYNCED`).
- **Validation Check:** All 6 `ELIGIBLE` proposals passed `cvat_tools.pose.face50_engine.validate_face50_frame` with `0` findings after applying changes to `job_1975_live_pre_goal.json`.

---

## Rendered Files (`artifacts/face50_research/evidence/final_proposals/`)

### 1. Eligible Proposals (`6` frames — `AI_REVIEWED_ELIGIBLE`, `0` post-fix findings)

| Frame | Image | Action | Luma | IR CLAHE | 4x Crop | Output Size | Rendered Diff |
|---:|---|---|---:|:---:|---|---|---|
| `94` | `G06_095.jpg` | `update` (`4` kps: `42,43,46,49`) | `16.5` | Yes | `238×223` | `1916×962` | [`f094_G06_095.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/final_proposals/f094_G06_095.jpg) |
| `95` | `G06_096.jpg` | `update` (`5` kps: `42,43,45,46,49`) | `27.1` | Yes | `323×244` | `2596×1046` | [`f095_G06_096.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/final_proposals/f095_G06_096.jpg) |
| `102` | `G06_103.jpg` | `create` (`50` kps: `V=19, Q=31`) | `29.9` | Yes | `230×223` | `1852×962` | [`f102_G06_103.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/final_proposals/f102_G06_103.jpg) |
| `105` | `G06_106.jpg` | `update` (`7` kps: `42..45,47..49`) | `66.8` | No | `149×129` | `1204×586` | [`f105_G06_106.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/final_proposals/f105_G06_106.jpg) |
| `106` | `G06_107.jpg` | `create` (`50` kps: `V=50, Q=0`) | `15.1` | Yes | `235×258` | `1892×1102` | [`f106_G06_107.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/final_proposals/f106_G06_107.jpg) |
| `118` | `G06_119.jpg` | `update` (`33` kps: `5..9,22..49`) | `60.5` | No | `155×157` | `1252×698` | [`f118_G06_119.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/final_proposals/f118_G06_119.jpg) |

### 2. Review Queue (`3` frames — `NEEDS_HUMAN_REVIEW`, Held / Not Synced)

| Frame | Image | Reason | Luma | IR CLAHE | 4x Crop | Output Size | Rendered Diff |
|---:|---|---|---:|:---:|---|---|---|
| `100` | `G06_101.jpg` | Extreme `-35.8°` profile; surgical `moitrong` preview resolves inner lip, but foreshortened `longmayphai` (`5..9`) still triggers `BROW_NON_MONOTONIC_LOCAL`. | `98.5` | No | `161×142` | `1300×638` | [`f100_G06_101.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/final_proposals/f100_G06_101.jpg) |
| `111` | `G06_112.jpg` | Dark IR; surgical `moitrong` preview resolves `INNER_LIP_OUTSIDE_OUTER` + `LIP_SELF_INTERSECT`, but CVAT `kp 5` triggers `BROW_BELOW_EYE`. | `33.4` | Yes | `207×209` | `1668×906` | [`f111_G06_112.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/final_proposals/f111_G06_112.jpg) |
| `112` | `G06_113.jpg` | Very dark IR + compact `47×38px` face (`512×424`); `BROW_NON_MONOTONIC_LOCAL` (`5..9`) & sub-pixel lip compression (`kp 42`). | `15.7` | Yes | `117×108` | `948×502` | [`f112_G06_113.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/final_proposals/f112_G06_113.jpg) |
