from django.db import models


class AuroraSnapshot(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    project_name = models.CharField(max_length=255)
    total_files = models.PositiveIntegerField(default=0)
    total_commits = models.PositiveIntegerField(default=0)
    payload = models.JSONField(default=dict)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Aurora Snapshot"
        verbose_name_plural = "Aurora Snapshots"

    def __str__(self):
        return f"{self.project_name} ({self.total_files} files) - {self.created_at:%Y-%m-%d %H:%M}"


