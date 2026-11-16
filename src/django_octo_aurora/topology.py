import ast
import subprocess
from pathlib import Path
from django.apps import apps
from django.conf import settings

IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".rye",
    ".pytest_cache",
    "staticfiles",
}

BOILERPLATE_NAMES = {"__init__.py", "migrations", "manage.py", "asgi.py", "wsgi.py"}
INFRA_DIRS = {"tests", "features", "performance", ".github", "audits", "config"}


def _classify_node(rel_path: str, name: str, is_dir: bool) -> str:
    top = rel_path.split("/")[0]
    if top in INFRA_DIRS or name in BOILERPLATE_NAMES or "/migrations" in rel_path:
        return "infra"


def _inspect_py(file_path: Path) -> dict:
    try:
        src = file_path.read_text(encoding="utf-8")
        tree = ast.parse(src)
        return {
            "lines": len(src.splitlines()),
            "classes": sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree)),
            "functions": sum(
                isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                for n in ast.walk(tree)
            ),
        }
    except Exception:
        return {}


def _read_git_timeline(root: Path, limit: int = 150) -> list[dict]:
    if not (root / ".git").exists():
        return []
    cmd = [
        "git",
        "-C",
        str(root),
        "log",
        f"-n{limit}",
        "--reverse",
        "--name-status",
        "--pretty=format:COMMIT|%h|%an|%ad|%s",
        "--date=short",
    ]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return []

    commits, current = [], None
    for line in out.splitlines():
        if line.startswith("COMMIT|"):
            if current:
                commits.append(current)
            _, sha, author, date, msg = line.split("|", 4)
            current = {
                "sha": sha,
                "author": author,
                "date": date,
                "message": msg,
                "changes": [],
            }
        elif current and "\t" in line:
            parts = line.split("\t")
            status, filepath = parts, parts[-1]
            if not any(part in IGNORED_DIRS for part in Path(filepath).parts):
                current["changes"].append({"status": status, "path": filepath})
    if current:
        commits.append(current)
    return commits


def _append_installed_apps(nodes: list[dict], root: Path) -> None:
    if not apps.ready:
        return

    django_core_apps = []
    external_modules = []

    for app_config in apps.get_app_configs():
        app_path = Path(app_config.path).resolve()
        if app_config.name.startswith("django.contrib."):
            django_core_apps.append(app_config.label)
        elif not app_path.is_relative_to(root):
            external_modules.append((app_config.label, app_config.name))

    if external_modules:
        nodes.append(
            {
                "id": "installed-modules",
                "name": "installed_modules",
                "type": "dir",
                "parent": ".",
                "ext": "dir",
                "role": "satellite",
                "meta": {},
            }
        )
        for label, full_name in sorted(external_modules):
            nodes.append(
                {
                    "id": f"installed-modules/{label}",
                    "name": full_name,
                    "type": "file",
                    "parent": "installed-modules",
                    "ext": ".py",
                    "role": "satellite",
                    "meta": {},
                }
            )

    if django_core_apps:
        nodes.append(
            {
                "id": "django-contrib",
                "name": f"django.contrib ({len(django_core_apps)})",
                "type": "file",
                "parent": ".",
                "ext": ".toml",
                "role": "satellite",
                "meta": {},
            }
        )


def build_aurora_topology(base_dir: Path | None = None) -> dict:
    target_dir = base_dir or getattr(settings, "BASE_DIR", None) or Path.cwd()
    root = Path(target_dir).resolve()
    nodes = [
        {
            "id": ".",
            "name": root.name,
            "type": "dir",
            "parent": None,
            "ext": "root",
            "role": "root",
            "meta": {},
        }
    ]

    all_paths = sorted(
        [p for p in root.rglob("*") if not any(part in IGNORED_DIRS for part in p.parts)],
        key=lambda p: (not p.is_dir(), p.suffix != ".py", p.as_posix()),
    )

    for path in all_paths:
        rel = path.relative_to(root).as_posix()
        parent = path.parent.relative_to(root).as_posix()
        is_dir = path.is_dir()
        nodes.append(
            {
                "id": rel,
                "name": path.name,
                "type": "dir" if is_dir else "file",
                "parent": parent,
                "ext": "dir" if is_dir else (path.suffix.lower() or ".file"),
                "role": _classify_node(rel, path.name, is_dir),
                "meta": _inspect_py(path) if path.suffix == ".py" else {},
            }
        )

    _append_installed_apps(nodes, root)

    return {
        "project_name": root.name,
        "nodes": nodes,
        "timeline": _read_git_timeline(root),
    }

