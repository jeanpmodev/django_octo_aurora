from django.urls import include, path

urlpatterns = [
    path("aurora-demo/", include("django_octo_aurora.urls")),
]
