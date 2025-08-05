from django.contrib import admin
from .models import Plant, GrowthRecord

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'name', 'cover', 'created_at')
    search_fields = ('name', 'user_id')

@admin.register(GrowthRecord)
class GrowthRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'plant', 'image', 'record_time', 'created_at')
    search_fields = ('plant__name',)
