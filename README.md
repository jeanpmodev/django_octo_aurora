<p align="center">
  <img src="https://raw.githubusercontent.com/jeanpmodev/jeanpmodev/main/assets/django-octo-aurora.jpg" alt="Django-Octo-SEO" width="100%" />
</p>

# django-octo-aurora pypi library package

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![Framework: Django](https://img.shields.io/badge/Framework-Django-darkgreen)](https://djangoproject.com)
[![Package Manager: Rye](https://img.shields.io/badge/Package_Manager-Rye-orange)](https://astral.sh)
![PyPI Version](https://img.shields.io/pypi/v/django-octo-aurora)
[![Latest on Django Packages](https://img.shields.io/badge/Django_Packages-django__octo__aurora-8c3c26.svg)](https://djangopackages.org/packages/p/django_octo_aurora/)
[![Tests: pytest](https://img.shields.io/badge/Tests-pytest%20passed-2ea44f.svg)](https://github.com/jeanpmodev/django_octo_aurora/blob/main/TESTING.md)
[![BDD: Behave](https://img.shields.io/badge/BDD-Behave%20verified-009688.svg)](https://github.com/jeanpmodev/django_octo_aurora/blob/main/TESTING.md)
[![Load Test: Locust](https://img.shields.io/badge/Load_Test-11ms_median_%7C_0%25_fails-blueviolet.svg)](https://github.com/jeanpmodev/django_octo_aurora/blob/main/performance/locust_load_report.pdf)
[![CI](https://img.shields.io/github/actions/workflow/status/jeanpmodev/django_octo_aurora/ci.yml?branch=main&label=CI)](https://github.com/jeanpmodev/django_octo_aurora/actions/workflows/ci.yml)
[![Code Style: PEP 8](https://img.shields.io/badge/code%20style-PEP%208-blue)](https://peps.python.org/pep-0008/)
[![PyPI Provenance](https://img.shields.io/badge/PyPI-With%20Provenance-blue?logo=pypi&logoColor=white)](https://pypi.org/project/django-octo-aurora/#provenance)
[![Snyk Vulnerabilities](https://img.shields.io/badge/Snyk%20Vulnerabilities-0%20known-brightgreen?logo=snyk&logoColor=white)](https://security.snyk.io/package/pip/django-octo-aurora)
[![Security Audit](https://github.com/jeanpmodev/django_octo_aurora/actions/workflows/security.yml/badge.svg)](https://github.com/jeanpmodev/django_octo_aurora/actions/workflows/security.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/jeanpmodev/django_octo_aurora/badge)](https://scorecard.dev/viewer/?uri=github.com/jeanpmodev/django_octo_aurora)
[![Socket Badge](https://badge.socket.dev/pypi/package/django-octo-aurora/0.1.6?artifact_id=tar-gz)](https://badge.socket.dev/pypi/package/django-octo-aurora/0.1.6?artifact_id=tar-gz)
[![codecov](https://codecov.io/gh/jeanpmodev/django_octo_aurora/graph/badge.svg?token=FO3B4DS2RH)](https://codecov.io/gh/jeanpmodev/django_octo_aurora)

**django_octo_aurora** is a decoupled runtime software topology visualizer and interactive architecture showcase module under the **Django-Octo** ecosystem.

It inspects the host Django project structure, installed apps, AST metrics, and local Git commit history in real time, persisting lightweight snapshots for single-query rendering across both a public showcase endpoint and the Django Admin interface.

---

## Core Architecture

- **Dual-Channel Access:** Exposes an interactive HTML5 Canvas topology view on a dedicated route (`/aurora/`) and embeds the same preview directly inside the Django Admin (`Aurora Snapshots`).
- **Runtime Introspection:** Scans active project directories (`pathlib`), extracts Python class/function counts (`ast`), detects coupled `INSTALLED_APPS`, and parses local Git history (`git log`) using only the Python standard library.
- **Single-Query Persistence:** Stores serialized topology payloads in `AuroraSnapshot`, ensuring subsequent page loads execute in a single ORM query.
- **Interactive Canvas Controls:** Supports directional navigation (keyboard arrows / `WASD` and on-screen D-Pad), module filtering checklists, file-type counters, commit timeline playback, presentation mode (`H`), and clean PNG export.

---

## Installation & Quick Start

### 1. Install Package
```bash
pip install django-octo-aurora
```
Or using **Rye**:
```bash
rye add django-octo-aurora
```

### 2. Register App & Migrate
Add `"django_octo_aurora"` to `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    "django_octo_aurora",
]
```
Run migrations:
```bash
python3 manage.py migrate
```

### 3. Mount Routes
Include the module URLs in your project's `urls.py`:
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("aurora/", include("django_octo_aurora.urls")),
]
```
Start the server (`python3 manage.py runserver`) and open `http://127.0.0.1:8000` or `http://127.0.0.1:8000/admin/django_octo_aurora/aurorasnapshot/`.

---

## Local Development (Rye)

```bash
git clone https://github.com/jeanpmodev/django_octo_aurora.git
cd django_octo_aurora
rye sync
rye run pytest
rye run behave
```

See [TESTING.md](TESTING.md) for full QA and load testing instructions.

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

