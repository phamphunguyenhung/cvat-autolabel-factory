---
name: cvat-workflow
description: Consolidated CVAT Autolabel Factory V3 & V2 CLI workflow for zero-friction auth, job discovery, model-driven prelabeling, VS Code visual review, and conflict-safe CVAT sync.
---

# CVAT Autolabel Factory Workflow

Always operate **read-only and local-first by default**. Never print or commit `CVAT_PAT`, never bypass staleness/permission checks, and never write to CVAT without explicit `--yes`.

## 1. Environment, Auth & Discovery (Read-Only)
- `cvat-factory doctor` — verify Python, RAM/CPU, lazy model loading, auth status, and cached models.
- `cvat-factory setup` — discover/verify CVAT credentials (env / Windows Credential Manager) and detect real API role/permissions.
- `cvat-factory discover` / `cvat-factory jobs --mine` — list accessible tasks/jobs, frame counts, annotation types, and local run state.
- `cvat-factory models list` (or `--scan`) — inspect registered/cached models without loading weights into RAM.
- `cvat-factory inspect --job <id>` — inspect CVAT label schema, geometry types (`rectangle`, `polygon`, `skeleton`), and matched adapter/model.

## 2. Local-First Pipeline & Evidence Review
- `cvat-factory run --job <id> --mode auto` — run adaptive preprocessing (separating display-enhanced vs inference-input images), model/rule proposal, and quality gates into local SQLite storage.
- `cvat-factory review --job <id>` — render `BEFORE / AFTER / OVERLAY` + error crop zooms (max 5 priority cases) and interactive HTML dashboard, auto-opening in VS Code via `code.cmd --reuse-window`.
- `cvat-factory resume --job <id>` — resume the latest interrupted run or sync.
- `cvat-factory benchmark --job <id> --compare-v2` — measure real latency, RAM, cache hits, and geometry failures.

## 3. Safe Synchronization (Dry-Run Default)
- `cvat-factory sync --job <id>` — compute minimal PATCH/create diff, verify staleness & permissions, and preview without writing.
- `cvat-factory sync --job <id> --yes` — backup live CVAT state, apply minimal writes preserving human edits, and run read-back verification.
- `cvat-factory sync --job <id> --rollback --latest` — conflict-aware rollback (dry-run by default; `--yes` to execute).

## 4. V2 Compatibility (`python -m cvat_tools`)
- `python -m cvat_tools doctor`, `store capture --job <id>`, `store push --job <id>`, `full-bbox --job <id> --open`.
