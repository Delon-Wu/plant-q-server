from django.db import models
from django.utils import timezone

def plant_image_upload_to(instance, filename):
    # 按用户和植物分目录存储
    if hasattr(instance, 'user'):
        # 对于 Plant 模型
        user_id = instance.user
        plant_id = instance.id or 'new'
    else:
        # 对于 GrowthRecord 模型
        user_id = instance.plant.user
        plant_id = instance.plant.id
    return f"plant/{user_id}/{plant_id}/{filename}"

class Plant(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True, verbose_name='描述')
    cover = models.ImageField(upload_to=plant_image_upload_to)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return f"{self.name} ({self.user})"

class GrowthRecord(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='records')
    image = models.ImageField(upload_to=plant_image_upload_to)
    record_time = models.DateTimeField(default=timezone.now)
    remark = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'plant_growthrecord'

    def __str__(self):
        return f"{self.plant.name} @ {self.record_time}"
