"""Duong dan workspace (khong hardcode task/job/credential)."""
from __future__ import annotations

from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]          # .../learning/cvat
REPO = WORKSPACE.parent                                   # .../learning
CONFIG = WORKSPACE / "config"
DATA = WORKSPACE / "data"
CACHE = DATA / "cache"
MODELS = WORKSPACE / "models"
CHECKPOINTS = MODELS / "checkpoints"
PROJECTS = WORKSPACE / "projects"
LEGACY_MTM = REPO / "tools" / "mot-track-manager"

# noi tim .env, theo thu tu (chi doc, khong in gia tri)
ENV_CANDIDATES = [WORKSPACE / ".env", LEGACY_MTM / ".env"]
