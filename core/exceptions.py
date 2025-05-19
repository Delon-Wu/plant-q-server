from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .response import APIResponse

def custom_exception_handler(exc, context):
    if isinstance(exc, TokenError):
        return APIResponse.token_expired(msg=str(exc))
    elif isinstance(exc, InvalidToken):
        return APIResponse.auth_error(msg=str(exc))

    # 调用默认的异常处理器
    response = exception_handler(exc, context)
    
    if response is not None:
        if response.status_code == 401:
            return APIResponse.auth_error(msg=str(exc))
        return APIResponse.error(msg=str(exc), code=response.status_code)
    
    return None 