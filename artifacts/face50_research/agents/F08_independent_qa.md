# F08 — Independent QA Report (Job 1975 `F05_proposals.json`)

**Verdict:** **PASS** (with 2 minor non-blocking notes on proposal JSON schema normalization and F05 markdown count typo)  
**Target:** [`F05_proposals.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/agents/F05_proposals.json) (`eligible_count=6`, `review_queue_count=3`)  
**Baselines Checked:** [`job_1975_live_pre_goal.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/snapshots/job_1975_live_pre_goal.json), [`job_1975_labels.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/snapshots/job_1975_labels.json), [`job_1975_meta.json`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/snapshots/job_1975_meta.json)  
**Validator:** [`validate_face50_frame`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/src/cvat_tools/pose/face50_engine.py#L150-L292)

---

## 1. Automated Validation (`validate_face50_frame`) & Preservation Summary

All `6` eligible frames (`94, 95, 102, 105, 106, 118`) passed `validate_face50_frame` with **`0` errors** and **`0` warnings** (`findings=[]`), and matched `job_1975_meta.json` frame dimensions.

| Frame | Image | Action | Size | Angle (°) | Pre-Fix Findings | Post-Fix Errors / Warnings | Preservation / Structure Check | Verdict |
|---:|---|---|---|---:|---|---:|---|---|
| `94` | `G06_095.jpg` | `update` | `1280×1024` | `-4.0` | `INNER_LIP_OUTSIDE_OUTER` (`46`), `LIP_SELF_INTERSECT` (`42;43;48;49`) | `0` / `0` | `0..41` 100% identical to `live_pre_goal`; changed `[42, 43, 46, 49]`; `old_xy`/`old_state` 0 mismatches | **PASS** |
| `95` | `G06_096.jpg` | `update` | `1280×1024` | `-5.3` | `INNER_LIP_OUTSIDE_OUTER` (`42;46`) | `0` / `0` | `0..41` 100% identical to `live_pre_goal`; changed `[42, 43, 45, 46, 49]`; `old_xy`/`old_state` 0 mismatches | **PASS** |
| `102` | `G06_103.jpg` | `create` | `1280×1024` | `8.6` | *(missing in live)* | `0` / `0` | `50` kps (`19 V / 31 Q / 0 O / 0 Q+O`), maps cleanly to `7` `FACE50_GROUPS` skeletons | **PASS** |
| `105` | `G06_106.jpg` | `update` | `960×540` | `-4.1` | `INNER_LIP_OUTSIDE_OUTER` (`42`), `LIP_SELF_INTERSECT` (`44;45;46;47`) | `0` / `0` | `0..41` 100% identical to `live_pre_goal`; changed `[42, 43, 44, 45, 47, 48, 49]`; `old_xy`/`old_state` 0 mismatches | **PASS** |
| `106` | `G06_107.jpg` | `create` | `1280×1024` | `86.5` | *(missing in live)* | `0` / `0` | `50` kps (`50 V / 0 Q / 0 O / 0 Q+O`), maps cleanly to `7` `FACE50_GROUPS` skeletons | **PASS** |
| `118` | `G06_119.jpg` | `update` | `960×540` | `-29.2` | `INNER_LIP_OUTSIDE_OUTER` (`42;46`), `LIP_SELF_INTERSECT` (`44;46`), `BROW_BELOW_EYE` (`9`) | `0` / `0` | `0..4`, `10..13`, `14..21` 100% identical to `live_pre_goal`; changed 33 kps (`5..9, 22..49`); `old_xy`/`old_state` 0 mismatches | **PASS** |

### Notes on `f102` & `f106` Schema (`7` skeletons, `source="manual"`)
- `F05_proposals.json` stores `f102` and `f106` as a flat `"keypoints": {"0".."49"}` map rather than pre-serialized CVAT `"shapes"` arrays, so `"shapes"` (`7` skeletons) and `"source": "manual"` are not literal fields inside `F05_proposals.json`.
- When materialized against `job_1975_labels.json` using [`FACE50_GROUPS`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/src/cvat_tools/pose/face50_engine.py#L30-L38), both frames produce exactly `7` skeletons and `50` keypoints with `0` `Q+O` or `O` flags, and [`face50_engine.py`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/src/cvat_tools/pose/face50_engine.py#L760-L764) enforces `source="manual"` on every synced shape and element at CVAT write time. The downstream payload builder for `create` frames must ensure `shapes` are emitted with `source="manual"`.
- Minor doc typo in [`F05_missing_and_profiles.md`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/agents/F05_missing_and_profiles.md#L14): the summary table states `16 / 34 / 0` for `f102`, whereas the actual counts in `F05_proposals.json` (and the sum of F05's own listed `V` ranges `0..4` [5] + `5..9` [5] + `10` [1] + `22..29` [8]) are **`19 V / 31 Q / 0 O`**.

---

## 2. Visual Inspection of `f102` (`G06_103.jpg`) on CLAHE-Brightened Image

- **Path note:** `artifacts/face50_research/evidence/final_proposals/f102_G06_103.jpg` does not exist yet (`evidence/final_proposals/` has not been generated). Visual QA was performed directly against [`evidence/crops/f102_G06_103.jpg`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/crops/f102_G06_103.jpg), [`evidence/candidates/f102_G06_103.jpg_compare.png`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/face50_research/evidence/candidates/f102_G06_103.jpg_compare.png), and an independently rendered 2× zoomed side-by-side CLAHE (`clipLimit=4.0`) + Gamma (`0.45`) overlay crop.
- **Landmark placement findings (`PASS`):**
  - **Eyebrows (`0..4`, `5..9`, `V`):** `longmaytrai` (`838,198` → `908,210`) tracks the left brow ridge cleanly below the diagonal glasses temple; `longmayphai` (`928,214` → `974,222`) tracks the unobstructed right brow ridge.
  - **Eyes (`14..21` `Q`, `22..29` `V`):** `mattrai` aligns over the shadowed left eye socket right above the raised hand/knuckle (`Q` appropriate); `matphai` (`934.31,226.09`..`961.69,231.91`) sits cleanly on the visible right eye (`V`).
  - **Nose (`10` `V`, `11..13` `Q`):** Nasion `10` (`918,220`) sits between inner brow/eye corners; `11..13` descend vertically along the nose bridge to tip `13` (`918,282`), immediately adjacent to the nose-tip IR specular highlight (`~915, 278`).
  - **Mouth (`30..49`, `Q`):** Centered at `(915.9, 316.9)` beneath nose tip `13` and behind the horizontal glasses frame and hand shadow, with `moitrong` (`42..49`) strictly contained inside `moingoai` (`30..41`) and no crossing edges.

---

## 3. Conclusion

`F05_proposals.json` (`6` eligible proposals: `94, 95, 102, 105, 106, 118`; `3` deferred to review queue: `100, 111, 112`) is **APPROVED (`PASS`)** for downstream CVAT payload assembly/sync, provided the `create` builder materializes `f102` and `f106` into `7` skeletons with `source="manual"`.
