from django.core.management.base import BaseCommand
from tasks import clean_old_track_events

class Command(BaseCommand):
    help = '清理30天前的埋点数据'

    def handle(self, *args, **options):
        deleted = clean_old_track_events(days=30)
        self.stdout.write(self.style.SUCCESS(f'已清理 {deleted} 条埋点数据'))
