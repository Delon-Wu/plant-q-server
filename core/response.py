from rest_framework.response import Response
from rest_framework import status

class APIResponse(Response):
    def __init__(self, data=None, code=200, msg="success", status=None, **kwargs):
        response_data = {
            "code": code,
            "data": data,
            "msg": msg
        }
        response_data.update(kwargs)
        super().__init__(data=response_data, status=status)

    @classmethod
    def success(cls, data=None, msg="success", status=status.HTTP_200_OK, **kwargs):
        return cls(data=data, code=200, msg=msg, status=status, **kwargs)

    @classmethod
    def error(cls, msg="error", code=400, data=None, status=status.HTTP_400_BAD_REQUEST, **kwargs):
        return cls(data=data, code=code, msg=msg, status=status, **kwargs) 