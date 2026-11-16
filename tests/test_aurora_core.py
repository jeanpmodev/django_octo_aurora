import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import Client, RequestFactory
from django.urls import reverse
from django_octo_aurora.admin import AuroraSnapshotAdmin
from django_octo_aurora.models import AuroraSnapshot
from django_octo_aurora.topology import build_aurora_topology


def test_build_aurora_topology_extracts_structure(tmp_path):
    sample_file = tmp_path / "models.py"
    sample_file.write_text("class Item:\n    pass\n\ndef run():\n    return True\n", encoding="utf-8")

    result = build_aurora_topology(base_dir=tmp_path)

    assert result["project_name"] == tmp_path.name
    assert len(result["nodes"]) >= 2

    py_node = next(n for n in result["nodes"] if n["name"] == "models.py")
    assert py_node["ext"] == ".py"
    assert py_node["meta"]["classes"] == 1
    assert py_node["meta"]["functions"] == 1


@pytest.mark.django_db
def test_showcase_view_renders_and_caches_snapshot(django_assert_num_queries):
    client = Client()
    url = reverse("django_octo_aurora:showcase")

    response = client.get(url)
    assert response.status_code == 200
    assert AuroraSnapshot.objects.count() == 1
    assert "AURORA" in response.content.decode("utf-8")

    with django_assert_num_queries(1):
        cached_response = client.get(url)
    assert cached_response.status_code == 200


@pytest.mark.django_db
def test_admin_refresh_view_creates_snapshot(monkeypatch):
    site = AdminSite()
    model_admin = AuroraSnapshotAdmin(AuroraSnapshot, site)

    request = RequestFactory().get("/admin/django_octo_aurora/aurorasnapshot/refresh/")
    setattr(request, "session", "session")
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)

    monkeypatch.setattr(
        "django_octo_aurora.admin.reverse",
        lambda viewname, *args, **kwargs: "/admin/django_octo_aurora/aurorasnapshot/",
    )

    response = model_admin.refresh_view(request)
    assert response.status_code == 302
    assert AuroraSnapshot.objects.count() == 1

