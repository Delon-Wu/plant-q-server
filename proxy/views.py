import httpx
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.response import APIResponse

class ProxyView(APIView):
    permission_classes = (IsAuthenticated,)

    async def post(self, request):
        try:
            data = request.data
            url = data.get('url')
            method = data.get('method', 'GET').upper()
            headers = data.get('headers', {})
            payload = data.get('data', None)
            async with httpx.AsyncClient() as client:
                resp = await client.request(method, url, headers=headers, data=payload)
            return APIResponse.success(data=resp.content, msg="Request successful", status=resp.status_code, content_type=resp.headers.get('content-type', 'application/octet-stream'))
        except Exception as e:
            return APIResponse.error(msg=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
