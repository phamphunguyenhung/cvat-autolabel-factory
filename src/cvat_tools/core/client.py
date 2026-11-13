"""CVAT REST client dung chung (thay mtm.cvat / spm.cvat).

- Profile local/remote lay tu config/cvat.<profile>.yaml; PAT tu .env hoac bien moi truong (khong bao gio in).
- MAC DINH CHI DOC: moi lenh ghi/xoa raise WriteNotAuthorized tru khi write_enabled=True.
"""
from __future__ import annotations

import os
from pathlib import Path

import requests

from cvat_tools.core import paths

ENV_KEYS = ("CVAT_HOST", "CVAT_PAT", "CVAT_ORG", "MOT_MODEL", "POSE_MODEL")


class CvatError(RuntimeError):
    pass


class WriteNotAuthorized(CvatError):
    pass


def load_env(path: Path | None = None) -> dict:
    env: dict = {}
    for p in ([path] if path else paths.ENV_CANDIDATES):
        if p and p.exists():
            for line in p.read_text(encoding="utf8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env.setdefault(k.strip(), v.strip())
            break
    for k in ENV_KEYS:
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def load_profile(name: str = "local") -> dict:
    import yaml
    f = paths.CONFIG / f"cvat.{name}.yaml"
    return yaml.safe_load(f.read_text(encoding="utf8")) if f.exists() else {}


class Cvat:
    def __init__(self, host: str, pat: str, org: str = "", write_enabled: bool = False):
        if not pat:
            raise CvatError("Thieu CVAT_PAT (dat trong cvat/.env hoac bien moi truong).")
        self.host = host.rstrip("/")
        self.write_enabled = write_enabled
        self.h = {"Authorization": f"Bearer {pat}", "Accept": "application/vnd.cvat+json"}
        if org:
            self.h["X-Organization"] = org

    @classmethod
    def from_env(cls, profile: str = "local", write_enabled: bool = False) -> "Cvat":
        e, prof = load_env(), load_profile(profile)
        host = e.get("CVAT_HOST") or prof.get("host") or "http://localhost:8080"
        return cls(host, e.get("CVAT_PAT", ""), e.get("CVAT_ORG", prof.get("org", "") or ""), write_enabled)

    def _need_write(self):
        if not self.write_enabled:
            raise WriteNotAuthorized("Client dang o che do chi doc. Tao Cvat(..., write_enabled=True) khi da duoc phep ghi.")

    def _req(self, method: str, path: str, **kw):
        r = requests.request(method, self.host + path, headers=self.h, timeout=60, **kw)
        if r.status_code >= 400:
            raise CvatError(f"{method} {path} -> {r.status_code}: {r.text[:300]}")
        return r

    def get(self, path: str, **params):
        return self._req("GET", path, params=params).json()

    def all(self, path: str, **params) -> list:
        out, page = [], 1
        while True:
            body = self.get(path, page=page, page_size=100, **params)
            out += body.get("results", [])
            if not body.get("next"):
                return out
            page += 1

    # ---- doc
    def about(self) -> dict: return self.get("/api/server/about")
    def me(self) -> dict: return self.get("/api/users/self")
    def job(self, job_id: int) -> dict: return self.get(f"/api/jobs/{job_id}")
    def task(self, task_id: int) -> dict: return self.get(f"/api/tasks/{task_id}")
    def tasks(self) -> list: return self.all("/api/tasks")
    def jobs(self) -> list: return self.all("/api/jobs")
    def labels(self, job_id: int) -> list: return self.all("/api/labels", job_id=job_id)
    def meta(self, job_id: int) -> dict: return self.get(f"/api/jobs/{job_id}/data/meta")
    def annotations(self, job_id: int) -> dict: return self.get(f"/api/jobs/{job_id}/annotations")

    def frame(self, job_id: int, n: int) -> bytes:
        return self._req("GET", f"/api/jobs/{job_id}/data", params={"type": "frame", "number": n, "quality": "original"}).content

    # ---- ghi (chi them) -- can write_enabled
    def _patch(self, job_id: int, action: str, body: dict):
        self._need_write()
        return self._req("PATCH", f"/api/jobs/{job_id}/annotations", params={"action": action}, json=body)

    def create_tracks(self, job_id: int, tracks: list) -> dict:
        return self._patch(job_id, "create", {"shapes": [], "tracks": tracks, "tags": []}).json()

    def delete_tracks(self, job_id: int, tracks: list) -> None:
        """Chi cho rollback: track phai co id (lay tu run log)."""
        if any(t.get("id") is None for t in tracks):
            raise CvatError("delete_tracks chi nhan track co id.")
        self._patch(job_id, "delete", {"shapes": [], "tracks": tracks, "tags": []})

    def create_shapes(self, job_id: int, shapes: list) -> dict:
        return self._patch(job_id, "create", {"shapes": shapes, "tracks": [], "tags": []}).json()

    def delete_shapes(self, job_id: int, shapes: list) -> None:
        if any(s.get("id") is None for s in shapes):
            raise CvatError("delete_shapes chi nhan shape co id.")
        self._patch(job_id, "delete", {"shapes": shapes, "tracks": [], "tags": []})
