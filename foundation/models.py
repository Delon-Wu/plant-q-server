from django.db import models
from django.utils import timezone

class TrackEvent(models.Model):
    event = models.CharField(max_length=64)
    detail = models.TextField(null=True, blank=True)
    user_id = models.CharField(max_length=64, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.event} - {self.user_id} @ {self.timestamp}"
