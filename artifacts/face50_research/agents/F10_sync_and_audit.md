# F10 — Sync & Final Audit Report (Job 1975 / Task 473)

- **Agent:** F10 (Sole CVAT Writer)
- **Job / Task:** Job 1975 / Task 473 (Face50, frames `90..119`)
- **Sync Payload:** `artifacts/face50_research/proposed_face50_1975_round2.json`

## 1. Round 2 Sync Execution (`sync_face50_eligible`)
- **Dry-run (`yes=False`):**
  - `eligible_frames`: `[106, 102, 94, 95, 105, 118]`
  - `patch_shapes_count`: `7`
  - `create_shapes_count`: `14`
  - `total_kp_changes`: `149` (49 updates across 4 frames + 100 created keypoints across 2 frames)
  - `review_queue_frames`: `[100, 111, 112]`
- **Committed (`yes=True`):**
  - `written_to_cvat`: `True`
  - `readback_mismatches`: `0`
  - `created_shape_ids`: `[1453124..1453137]` (14 skeleton shapes on frames `102, 106` with `source="manual"`)
  - **Backup path:** `D:\06-Learning\AIA-VINGROUP\learning\cvat\week02\task473-face\job1975-face50\backups\before_face50_sync_20261118_141219.json`
  - **Run log path:** `D:\06-Learning\AIA-VINGROUP\learning\cvat\week02\task473-face\job1975-face50\backups\run_face50_sync_20261118_141219.json`

## 2. Live CVAT Post-Sync Verification (`Cvat.from_env('edufun', write_enabled=False)`)
- **Coverage:** `30 / 30` frames annotated (`210` shapes, `1,500` keypoints, `0` missing frames).
- **Per-frame `validate_face50_frame` results:**
  - **Round 2 synced frames (`94, 95, 102, 105, 106, 118`):** `0` errors, `0` warnings across all 6 frames.
  - **Review Queue frames (`100, 111, 112` — intentionally untouched):**
    - `f100`: `2` errors (`INNER_LIP_OUTSIDE_OUTER`, `LIP_SELF_INTERSECT`), `1` warning (`BROW_NON_MONOTONIC_LOCAL`)
    - `f111`: `3` errors (`INNER_LIP_OUTSIDE_OUTER`, `LIP_SELF_INTERSECT`, `BROW_BELOW_EYE`), `0` warnings
    - `f112`: `2` errors (`INNER_LIP_OUTSIDE_OUTER`, `LIP_SELF_INTERSECT`), `1` warning (`BROW_NON_MONOTONIC_LOCAL`)
  - **Other untouched baseline frames with findings:**
    - `f090`: `1` error (`LIP_SELF_INTERSECT`), `1` warning (`BROW_NON_MONOTONIC_LOCAL`)
    - `f096`: `1` error (`LIP_SELF_INTERSECT`), `0` warnings
    - `f101`: `1` error (`LIP_SELF_INTERSECT`), `0` warnings
    - `f107`: `1` error (`LIP_SELF_INTERSECT`), `1` warning (`BROW_NON_MONOTONIC_LOCAL`)
    - `f114`: `1` error (`LIP_SELF_INTERSECT`), `0` warnings
  - **All remaining 16 frames (`91, 92, 93, 97, 98, 99, 103, 104, 108, 109, 110, 113, 115, 116, 117, 119`):** `0` errors, `0` warnings.
  - **Total across 30 frames:** `12` errors (0 on Round 2 synced frames), `4` warnings.

## 3. Artifacts Updated & Visual Check
- Appended `149` Round 2 rows to `artifacts/face50_research/FACE50_CORRECTION_HISTORY.csv` (`221` total rows; `0` duplicates).
- Updated `artifacts/face50_research/FACE50_QC_REPORT.md` with Round 1 + Round 2 numbers (`30/30` frames on CVAT).
- Opened `artifacts/face50_research/evidence/final_proposals/00_FINAL_CONTACT_SHEET.jpg` in VS Code via `open_in_vscode` (`True`).

## 4. Test Verification
- Command: `python -m pytest tests/test_face50_engine.py tests/test_pose17_validate.py -v`
- Result: `14 passed in 3.78s` (all 5 tests in `test_face50_engine.py` and 9 tests in `test_pose17_validate.py` passed).
