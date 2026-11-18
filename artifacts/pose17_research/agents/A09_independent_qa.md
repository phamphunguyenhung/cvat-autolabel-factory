# A09 — Independent QA Report (Pose17 Gold Reference & Guideline Engine)

**Role:** A09 — Independent QA  
**Scope:** Job 1623 (`Task 402`, `G06`, frames `90..119`) & Pose17 Guideline Engine (`P17-G01`–`P17-G30`)  
**Mode:** Read-only on CVAT and `src/` (only `A09_independent_qa.md` written)

---

## 1. PASS / FAIL Checklist

| Check | Status | Exact Verified Numbers & Evidence |
|---|---|---|
| **1. Snapshots (`artifacts/pose17_research/snapshots/`)** | **PASS** | All 5 required JSON files exist, non-empty, valid JSON: `job_1623.json` (`1,230 B`), `job_1623_meta.json` (`5,523 B`), `job_1623_labels.json` (`9,243 B`), `job_1623_annotations_raw.json` (`217,214 B`), `keypoint_mapping.json` (`167,249 B`). |
| **2. Frame Manifest (`frame_manifest.csv`)** | **PASS** | `30` rows (`frame_index = 90..119`), `28` skeletons total (`0` on `100, 118`; `1` on remaining 28 frames), `30/30` valid 64-hex-char SHA256 hashes. |
| **3. Version History & Change Logs** | **PASS** | `VERSION_HISTORY.md` (`4,431 B`), `version_comparison.csv` (`1,035 B`, `13` rows), `annotation_change_log.csv` (`159,284 B`, `1,605` rows). |
| **4. Guidelines & Rule CSVs (`docs/guidelines/pose17/`)** | **PASS** | `G06_POSE17_GUIDELINE.md` (`22,489 B`), `POSE17_GENERAL_GUIDELINE.md` (`11,213 B`), `GUIDELINE_CHANGELOG.md` (`4,599 B`), `pose17_rules.csv` (`11,329 B`, `30` rules), `difficult_cases.csv` (`22,026 B`, `30` cases). |
| **5. Evidence Images** | **PASS** | `evidence/overlays/`: `30` files (`f090_G06_091.jpg`..`f119_G06_120.jpg`); `evidence/before_after/`: `6` files (`f093_G06_094.jpg`, `f101_G06_102.jpg`, `f113_G06_114.jpg`, `f114_G06_115.jpg`, `f116_G06_117.jpg`, `f117_G06_118.jpg`). |
| **6. Agent Reports (`artifacts/pose17_research/agents/`)** | **PASS** | `A01`–`A08` and `A10` reports all present and non-empty (`A01` `4,241 B`, `A02` `16,943 B`, `A03` `17,811 B`, `A04` `13,341 B`, `A05` `15,263 B`, `A06` `23,074 B`, `A07` `3,463 B`, `A08` `2,401 B`, `A10` `4,136 B`), plus JSON outputs (`A02_deltas.json`, `A04_visibility_audit.json`, `A05_cases.json`, `A06_geometry_metrics.json`). |
| **7. `pose17_rules.csv` Schema & Enums** | **PASS** | `30` unique rules (`P17-G01`..`P17-G30`). `source_type`: `BTC_OFFICIAL=19`, `GEOMETRIC_INFERENCE=5`, `AI_RECOMMENDATION=5`, `USER_OBSERVED=1` (`0` invalid). `status`: `approved=25`, `proposed=3` (`P17-G17`, `P17-G24`, `P17-G25`), `needs_mentor=2` (`P17-G08`, `P17-G26`). |
| **8. `difficult_cases.csv` Referential Integrity** | **PASS** | `30` rows (`CASE-1623-F090`..`CASE-1623-F119`), `0` empty `rule_ids`, `0` unknown `rule_id` references, `0` missing `evidence_path` files on disk. |
| **9. `proposed_corrections.csv` Referential Integrity** | **PASS** | `39` rows (`CORR-1623-001`..`CORR-1623-039`), `0` empty `rule_id`, `0` unknown `rule_id` references, `0` missing `evidence_path` files on disk. |
| **10. Validation & Coverage Match vs A10** | **PASS** | `VALIDATION_RESULTS.csv`: `157` rows (`error=35`, `warning=53`, `info=69`; layers: `L1_STRUCTURAL=2`, `L2_GEOMETRIC=7`, `L3_SEMANTIC=79`, `L4_CROSS_CASE=19`, `L5_EVIDENCE_QA=50`); `FRAME_COVERAGE.csv`: `30` rows (`pass=2`, `fail=17`, `warn=11`; per-frame sums: `skeleton_count=28`, `error_count=35`, `warning_count=53`, `info_count=68` + `1` job-level `frame_index=-1` info row = `157`). `snapshot_sha256 = 0fc88cfb9396cb022fb5f4572effb2d0ffc884153e02164b0bc4c6efccc38bbc`. Exact match with `A10_integration_engineer.md`. |
| **11. CLI Idempotency & Unit Tests** | **PASS** | Ran `python -m tools.pose17 validate --job 1623 --offline --json` twice consecutively: `VALIDATION_RESULTS.csv` stayed `157` rows and `FRAME_COVERAGE.csv` stayed `30` rows (`0` duplicates). Ran `python -m pytest tests/test_pose17_validate.py -v`: `8 passed in 5.32s`. |
| **12. CVAT Read-Only Integrity (`src/`)** | **PASS** | Inspected `src/cvat_tools/pose/pose17_validate.py`, `src/cvat_tools/pose/pose17_cli.py`, and `tools/pose17.py`: zero write/PATCH/POST/DELETE calls. Only `Cvat.from_env(profile=profile, write_enabled=False)` at `pose17_validate.py:306`, invoking `cv.job`, `cv.meta`, `cv.labels`, `cv.annotations` only. |
| **13. Caveats & Unsubstantiated Claims Audit** | **PASS** | Zero unsubstantiated claims (e.g., "100% hoàn thiện"); all `100%` metrics in `A04`/`A05`/`A06` are narrowly scoped counts. Open `needs_mentor` items (`P17-G08`, `P17-G26`, label naming, `source=file` edit policy, `outside` scoring, `MIN_PERSON_PX`), Task `402` HTTP `403`, `/api/events` HTTP `500` (`history_unavailable`), `gold = 0`, and L5 `advisory_only=true, is_ground_truth=false, auto_promoted=false` are explicitly documented. |

---

## 2. Minor Documentation Observations (Non-Blocking)
1. `VERSION_HISTORY.md` line 30 refers to the v5 validator module with shorthand `cvat_tools.pose.validate`; the actual module path is `cvat_tools.pose.pose17_validate` (exposed via `python -m cvat_tools pose17` and `python -m tools.pose17`).
2. `GUIDELINE_CHANGELOG.md` line 44 mentions `scripts/w2_qc_rules.py` / `scripts/eval_pose17.py` as sync targets; the new 5-layer engine is implemented in `src/cvat_tools/pose/pose17_validate.py`.
3. `src/` and CVAT remain untouched by QA; only this report was written.
