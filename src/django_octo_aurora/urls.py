from django.urls import path
from .views import AuroraRuntimeShowcaseView

app_name = "django_octo_aurora"

urlpatterns = [
    path("", AuroraRuntimeShowcaseView.as_view(), name="showcase"),
]
