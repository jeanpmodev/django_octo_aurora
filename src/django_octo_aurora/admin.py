from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from .models import AuroraSnapshot
from .topology import build_aurora_topology


@admin.register(AuroraSnapshot)
class AuroraSnapshotAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "project_name", "total_files", "total_commits")
    readonly_fields = ("created_at", "project_name", "total_files", "total_commits", "live_preview")
    exclude = ("payload",)
    change_list_template = "admin/django_octo_aurora/aurorasnapshot/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("refresh/", self.admin_site.admin_view(self.refresh_view), name="django_octo_aurora_refresh"),
        ]
        return custom + urls

    def refresh_view(self, request):
        data = build_aurora_topology()
        snap = AuroraSnapshot.objects.create(
            project_name=data["project_name"],
            total_files=sum(1 for n in data["nodes"] if n["type"] == "file"),
            total_commits=len(data.get("timeline", [])),
            payload=data,
        )
        self.message_user(request, f"Snapshot #{snap.id} refreshed ({snap.total_files} files).", messages.SUCCESS)
        return HttpResponseRedirect(reverse("admin:django_octo_aurora_aurorasnapshot_changelist"))

    @admin.display(description="Aurora Showcase")
    def live_preview(self, obj):
        url = reverse("django_octo_aurora:showcase")
        return format_html(
            '<iframe src="{}?embed=1" style="width:100%;height:520px;border:1px solid #1e293b;border-radius:8px;background:#05070d;"></iframe>',
            url,
        )

    def has_add_permission(self, request):
        return False

