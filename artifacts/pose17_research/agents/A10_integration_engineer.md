# A10 — Integration Engineer Report (Pose17 5-Layer Validator & Guideline Engine)

## 1. Files Created / Edited
- Created `src/cvat_tools/pose/pose17_validate.py`:
  - **Rule & Case Registry Engine**: `lookup_rule`, `cases_for_rule`, `open_case` (verifies `evidence_path` on disk), `propose_rule` (idempotent append/update for `proposed` rules while strictly preserving `approved` rules).
  - **5-Layer Validation Engine** (`validate_frame`, `validate_job`, `load_job_snapshot`, `write_validation_outputs`):
    - **L1 (`L1_STRUCTURAL`)**: 17 keypoints `"1".."17"` for `person_vf17`, missing-skeleton detection (`MISSING_SKELETON`), frame bounds metadata, forbidden `hidden=True` (`P17-G10`).
    - **L2 (`L2_GEOMETRIC`)**: out-of-bounds non-outside coords (`P17-G23`), `< 3px` keypoint overlap (`P17-G22`), torso-normalized bone length outliers (`P17-G24`), upright vs horizontal/rotated torso-axis R/L projection (`P17-G06`, `P17-G08`), upright ankle-above-knee check (`P17-G25`), upper-limb chain crossings (`P17-G07`).
    - **L3 (`L3_SEMANTIC`)**: `occluded=True AND outside=True` conflict (`P17-G11`), skeleton bulk `occluded=True` (`P17-G12`), in-frame face/torso `{1..7,12,13}` marked `outside` (`P17-G15`), deep in-frame `outside` (`>= 8px`, `P17-G13`).
    - **L4 (`L4_CROSS_CASE`)**: detects mixed resolutions (`512x424`, `960x540`, `1280x1024`) as `independent_snapshots` (never assumes temporal continuity) and flags BTC `960x540` resolution mismatches (`P17-G26`).
    - **L5 (`L5_EVIDENCE_QA`)**: integrates `reports/w2_vlm/1623_*.json` and local image luminance/Laplacian metrics strictly as `advisory_only=True, is_ground_truth=False, auto_promoted=False` (`suspicious_qa` flags only).
  - **Idempotency & Structured Logging**: `snapshot_sha256`, `VALIDATOR_VERSION = "2.0.0"`, deduplicated CSV output, JSON-formatted `cvat_tools.pose17` logger, and `render_before_after_cases`.
- Created `src/cvat_tools/pose/pose17_cli.py`: CLI supporting `validate`, `audit`, `mine-cases`, `build-guideline`, `lookup-rule`, `open-case` with `--offline` and `--json`.
- Edited `src/cvat_tools/cli.py`: registered `pose17` subcommand group.
- Created `tools/__init__.py` and `tools/pose17.py`: thin repo-root shim (`python -m tools.pose17 ...`) delegating directly to `cvat_tools.pose.pose17_cli.main`.
- Created `tests/test_pose17_validate.py`: 8 unit & CLI smoke tests covering L1–L5, registry idempotency, and CLI commands.

## 2. Job 1623 Offline Verification Outputs
- `python -m tools.pose17 validate --job 1623 --offline --json`:
  - `snapshot_sha256`: `0fc88cfb9396cb022fb5f4572effb2d0ffc884153e02164b0bc4c6efccc38bbc`
  - `sequence_mode`: `independent_snapshots`, `resolutions`: `["512x424", "960x540", "1280x1024"]`
  - `frame_count`: `30`, `finding_count`: `157` (`L1_STRUCTURAL`: 2, `L2_GEOMETRIC`: 7, `L3_SEMANTIC`: 79, `L4_CROSS_CASE`: 19, `L5_EVIDENCE_QA`: 50)
  - Generated `artifacts/pose17_research/VALIDATION_RESULTS.csv` and `artifacts/pose17_research/FRAME_COVERAGE.csv`.
- `python -m tools.pose17 audit --job 1623 --offline --json`:
  - `frame_status`: `{"pass": 2, "fail": 17, "warn": 11}`
  - `l5_advisory_count`: `50`, `l5_auto_promoted_count`: `0`
- `python -m tools.pose17 mine-cases --job 1623 --offline --json`:
  - `total_existing_cases`: `30`, `mined_frames_count`: `30`
- `python -m tools.pose17 build-guideline --job 1623 --offline --render-before-after --json`:
  - `rules_count`: `30` (`approved`: 25, `needs_mentor`: 2, `proposed`: 3), `cases_count`: `30`, `missing_evidence_cases`: `[]`
  - Rendered 6 before/after comparison images into `artifacts/pose17_research/evidence/before_after/`:
    - `f093_G06_094.jpg`, `f101_G06_102.jpg`, `f113_G06_114.jpg`, `f114_G06_115.jpg`, `f116_G06_117.jpg`, `f117_G06_118.jpg`.
- `python -m cvat_tools pose17 lookup-rule --rule-id P17-G11 --json` & `python -m tools.pose17 open-case --case-id CASE-1623-F093 --json`: both exited `0` (`matching_cases_count: 13`, `evidence_exists: true`).

## 3. Pytest Results
- `python -m pytest tests/test_pose17_validate.py -v`: **8 passed in 5.58s**.
- `python -m pytest tests -q`: **283 passed in 141.85s (0:02:21)**.
