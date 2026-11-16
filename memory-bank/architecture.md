# Architecture v2.0 (Pi-Inspired Modular Tool System)

- **Tool Kernel (`src/cvat_tools/core/`)**:
  - `permissions.py`: `Permission` (`READ_ONLY`, `LOCAL_WRITE`, `REMOTE_WRITE`) + `check_permissions()`.
  - `contracts.py`: `ToolSpec`, `ToolResult`, `ResourceRequirements`.
  - `registry.py`: `ToolRegistry` + `build_default_registry()`, đo `elapsed_ms` và `rss_mb`.
  - `model_registry.py`: `ModelRegistry` đọc `config/models.yaml`, quản lý lazy-load và `unload()` + `gc.collect()`.
- **Adapters & Persistence**:
  - `core/client.py`: CVAT REST client (read-only mặc định).
  - `core/shapestore.py`: SQLite (`data/store/shapes.sqlite`) tách `human_final` khỏi `rule_draft`/`ai_draft`.
  - `core/transactions.py` + `sync/push.py`: backup, run log (`data/runs/`), verify sau ghi, rollback giữ `human_final`.
- **CLI & Optional Pi Layer**:
  - `src/cvat_tools/cli.py`: `--json`, `--traceback`, `tools list|info`, `models list`, `store <capture|list|stats|push|rollback>`, `full-bbox`, `run`, `doctor`.
  - `.pi/extensions/cvat-tools.ts` + `.pi/skills/cvat-workflow/SKILL.md`: optional wrapper gọi CLI `--json`.
