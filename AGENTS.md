# AGENTS.md — CVAT Tools Architecture v2.0

## Workspace & Core Rules
- Root: `D:\06-Learning\AIA-VINGROUP\learning\cvat` (Python >= 3.11, CPU-first, Windows 16 GB RAM).
- **Rules & Memory Bank**: Always follow [rules.md](rules.md) and consult [memory-bank/](memory-bank/architecture.md) (`architecture.md`, `lessons-learned.md`, `workflows.md`) before modifying pipelines or onboarding a new CVAT job.
- **Agent-agnostic**: Every `python -m cvat_tools ...` / `cvat-tools ...` command MUST work without Pi, DeepSeek, or any LLM.
- **Read-only by default**: Never write to remote CVAT (`--yes` + `write_enabled=True` required). All AI predictions stay `ai_draft` / `rule_draft` in local SQLite (`data/store/shapes.sqlite`) and are separated from `human_final`.
- **Lazy model loading**: Never import torch/ultralytics/onnxruntime or load weights at CLI startup; `ModelRegistry` enforces at most one heavyweight model in RAM by default (`unload()` + `gc.collect()`).

## Entrypoints
- `cvat-tools --help` / `python -m cvat_tools --help`
- `cvat-tools tools list` / `cvat-tools --json tools info <tool_id>`
- `cvat-tools models list`
- `cvat-tools doctor`
- `cvat-tools store <capture|list|stats|push|rollback> --job <id>`
- `cvat-tools full-bbox --job 285 --open`
- Optional Pi extension: `.pi/extensions/cvat-tools.ts` + `.pi/skills/cvat-workflow/SKILL.md`.
