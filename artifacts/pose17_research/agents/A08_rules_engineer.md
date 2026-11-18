# A08 — Rules Engineer Summary

**Role:** Pose17 Gold Reference & Guideline Engine — Rules Engineer (`A08`)  
**Scope:** Job 1623 (Task 402, `G06`, frames `90..119`) & Reusable Pose17 Guideline (`P17-G01`–`P17-G30`)  
**Mode:** Read-only on CVAT and `src/`

---

## 1. Created Artifacts

| Artifact | Rows (excluding header) | Encoding | Purpose |
|---|---:|---|---|
| [pose17_rules.csv](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/docs/guidelines/pose17/pose17_rules.csv) | `30` | UTF-8 (no BOM) | Canonical rule table `P17-G01`..`P17-G30` with exact `source_type`, `source_ref`, `confidence`, `status` from `POSE17_GENERAL_GUIDELINE.md` |
| [difficult_cases.csv](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/docs/guidelines/pose17/difficult_cases.csv) | `30` | UTF-8 (no BOM) | Per-frame difficult case registry (`90..119`) integrating `A05_cases.json`, `A04_visibility_audit.json`, and `A06_geometry_metrics.json`, linked to `rule_ids` and overlay evidence |
| [proposed_corrections.csv](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/proposed_corrections.csv) | `39` | UTF-8 (no BOM) | Actionable read-only correction proposals (`status = proposed_for_human_review`) covering missing skeletons (`f100`, `f118`), `f093` bulk-occluded + `7Q`, `22` `occluded+outside` conflicts, `9` in-frame eye/ear `outside`, `f101` `2=4` overlap (`0.27 px`), `f117` `kpt 6`, `f116` `kpt 10/8/6`, `f113` wrist swap, `f114` `forearm_R` (`48.8 px` / `0.139x` torso), and leg/ankle misplacements (`f094`, `f095`, `f115`, `f119`, `f110`, `f112`) |
| [A08_rules_engineer.md](file:///D:/06-Learning/AIA-VINGROUP/learning/cvat/artifacts/pose17_research/agents/A08_rules_engineer.md) | — | UTF-8 (no BOM) | This summary report |

---

## 2. Programmatic Cross-Reference & File Validation

- **`pose17_rules.csv`:** `30` rules (`P17-G01`..`P17-G30`), `0` missing columns or malformed rows.
- **`difficult_cases.csv`:** `30` cases (`CASE-1623-F090`..`CASE-1623-F119`), **`0` missing `rule_id` references** against `pose17_rules.csv`, **`0` missing `evidence_path` overlay files**.
- **`proposed_corrections.csv`:** `39` proposals (`CORR-1623-001`..`CORR-1623-039`, all `status = proposed_for_human_review`), **`0` missing `rule_id` references** against `pose17_rules.csv`, **`0` missing `evidence_path` overlay files**.
- **Read-only compliance:** No writes to CVAT or `src/`.
