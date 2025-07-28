from django.db import models

class Task(models.Model):
    plant = models.CharField(max_length=255, blank=True)
    is_completed = models.BooleanField(default=False)
    task_type = models.CharField(max_length=20)
    duration_type = models.CharField(max_length=20)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    time_at_once = models.DateTimeField(null=True, blank=True)
    remark = models.TextField(blank=True)
    interval_days = models.IntegerField(default=0)  # Interval in days for recurring tasks
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_type
