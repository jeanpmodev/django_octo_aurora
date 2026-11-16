import os
import django
from django.conf import settings
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

if "testserver" not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS = [*settings.ALLOWED_HOSTS, "testserver"]


def before_all(context):
    call_command("migrate", verbosity=0)

