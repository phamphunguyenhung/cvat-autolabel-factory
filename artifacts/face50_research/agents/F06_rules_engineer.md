# F06 — Face50 Rules & Quality Gate Engineer Summary

## 1. Files Modified
- [`src/cvat_tools/pose/face50_engine.py`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/src/cvat_tools/pose/face50_engine.py)
  - Closed F03 validator blind spots in `validate_face50_frame` (and `build_face50_proposals` inner-lip containment check):
    - `INNER_LIP_OUTSIDE_OUTER`: tightened threshold from `-0.3` px to `-0.05` px (catches sub-pixel escapes such as `f105` and `f112`).
    - `LIP_SELF_INTERSECT`: added `_segments_intersect` and `_polygon_self_intersects` to check non-adjacent polygon edges of `moingoai` (`30..41`) and `moitrong` (`42..49`).
    - `BROW_BELOW_EYE`: checked in face-local `(u, v)` coordinates that brow points (`0..4`, `5..9`) are not below the upper eyelid (`15..17`, `23..25`).
    - `BROW_NON_MONOTONIC_LOCAL`: checked monotonic `u` order across `0..4` and `5..9` in face-local coordinates.
  - Added reusable `align_face50_clahe_fan(img_bgr, try_rotations=True, landmarker=None)` implementing:
    - Adaptive Gamma (`0.55` when mean luma `< 90`) + LAB CLAHE (`clipLimit=2.5`, `tileGridSize=(8, 8)`)
    - `FaceLandmarker.landmarks68(..., try_rotations=try_rotations)` + `map68_to_50`
    - `BrowEdgeSnap` (Sobel gradient snap within `±4` px along face-down `v`, bounded above upper eyelid)
    - `InnerLipClamp` (clamps `42..49` strictly inside `moingoai` via `_nudge_inner_lip_point`)
  - Extended `sync_face50_eligible` to support `action="create"` alongside `action="update"`:
    - Splits `eligible_proposals` into `update_proposals` and `create_proposals`.
    - Enforces `source="manual"` on all synced shapes and elements.
    - Adds create-mode staleness guard (aborts if `(frame, label_id)` already exists on live CVAT).
    - Calls `cv.create_shapes(job_id, create_shapes)` and performs read-back verification for both updated and created shapes.
- [`rules.md`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/rules.md)
  - Added Section 7: `Quy chuẩn Face50 Verification & Alignment (face50_engine.py)`.
- [`docs/guidelines/face50/FACE50_RULES.csv`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/docs/guidelines/face50/FACE50_RULES.csv)
  - Added `F50-R09` (`BrowEdgeSnap`), `F50-R10` (`LipSelfIntersect`), and `F50-R11` (`TightInnerLipContainment`).
- [`tests/test_face50_engine.py`](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/tests/test_face50_engine.py)
  - Added `test_face50_validator_blind_spots`, `test_align_face50_clahe_fan_with_mock_landmarker`, and `test_face50_sync_action_create_and_readback`.

## 2. Verification
- Ran `python -m pytest tests/test_face50_engine.py -v` at repo root: **5 passed in 6.27s** (`test_face50_rotation_aware_and_surgical_proposals`, `test_face50_sync_dry_run_and_staleness_guard`, `test_face50_validator_blind_spots`, `test_align_face50_clahe_fan_with_mock_landmarker`, `test_face50_sync_action_create_and_readback`).
- Read-only on CVAT (`write_enabled=False` / mocked `Cvat` in tests); `pose17_*.py` untouched.
