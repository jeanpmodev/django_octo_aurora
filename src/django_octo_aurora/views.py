import json
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import TemplateView
from .models import AuroraSnapshot
from .topology import build_aurora_topology


@method_decorator(xframe_options_sameorigin, name="dispatch")
class AuroraRuntimeShowcaseView(TemplateView):
    template_name = "django_octo_aurora/aurora_showcase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        snapshot = AuroraSnapshot.objects.first()

        if snapshot:
            data = snapshot.payload
        else:
            data = build_aurora_topology()
            try:
                AuroraSnapshot.objects.create(
                    project_name=data["project_name"],
                    total_files=sum(1 for n in data["nodes"] if n["type"] == "file"),
                    total_commits=len(data.get("timeline", [])),
                    payload=data,
                )
            except Exception:
                pass

        context["aurora_json"] = json.dumps(data)
        context["project_name"] = data.get("project_name", "Django Project")
        return context

