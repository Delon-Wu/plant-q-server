import os
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import json
from django.utils import timezone
from .models import TrackEvent

class TrackEventView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            # 支持 application/json
            if request.content_type.startswith('application/json'):
                data = json.loads(request.body.decode())
            else:
                data = request.POST.dict()
            event = data.get('event')
            detail = data.get('detail')
            user_id = data.get('userId')
            timestamp = data.get('timestamp')
            import datetime
            if timestamp:
                try:
                    # 支持时间戳或ISO格式
                    if isinstance(timestamp, (int, float)):
                        dt = datetime.datetime.fromtimestamp(float(timestamp))
                    else:
                        dt = datetime.datetime.fromisoformat(str(timestamp))
                except Exception:
                    dt = timezone.now()
            else:
                dt = timezone.now()
            TrackEvent.objects.create(
                event=event,
                detail=detail,
                user_id=user_id,
                timestamp=dt
            )
            return JsonResponse({'code': 0, 'msg': '埋点成功'})
        except Exception as e:
            return JsonResponse({'code': 1, 'msg': f'埋点失败: {str(e)}'}, status=500)
