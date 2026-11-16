from behave import given, then, when
from django.contrib.auth import get_user_model
from django.db import connection
from django.test import Client
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django_octo_aurora.models import AuroraSnapshot


@given("a clean Django runtime environment")
def step_clean_environment(context):
    AuroraSnapshot.objects.all().delete()
    context.client = Client()


@when("a user requests the Aurora showcase endpoint")
def step_request_showcase(context):
    context.url = reverse("django_octo_aurora:showcase")
    context.response = context.client.get(context.url)


@then("the response status code should be 200")
def step_check_status_200(context):
    assert context.response.status_code == 200


@then("the rendered canvas should contain the project topology payload")
def step_check_payload(context):
    html = context.response.content.decode("utf-8")
    assert "AURORA" in html
    assert 'id="c"' in html


@then("subsequent requests should execute in a single database query")
def step_check_single_query(context):
    with CaptureQueriesContext(connection) as queries:
        res = context.client.get(context.url)
    assert res.status_code == 200
    assert len(queries) == 1


@given("an authenticated Django superuser")
def step_authenticated_superuser(context):
    User = get_user_model()
    user, _ = User.objects.get_or_create(
        username="aurora_admin",
        defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True},
    )
    user.set_password("secret123")
    user.save()
    context.client = Client()
    context.client.force_login(user)


@when("the admin triggers the Aurora snapshot refresh action")
def step_trigger_refresh(context):
    refresh_url = reverse("admin:django_octo_aurora_refresh")
    context.admin_response = context.client.get(refresh_url)


@then("a new AuroraSnapshot record should be persisted")
def step_check_snapshot_persisted(context):
    assert context.admin_response.status_code == 302
    assert AuroraSnapshot.objects.count() >= 1

