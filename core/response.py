from rest_framework.response import Response
from rest_framework import status

class APIResponse(Response):
    """
    统一的API响应类
    支持同步和异步视图的响应格式标准化
    """
    def __init__(self, data=None, code=200, msg="success", status=None, **kwargs):
        response_data = {
            "code": code,
            "data": data,
            "msg": msg
        }
        # 合并额外的字段
        response_data.update(kwargs)
        super().__init__(data=response_data, status=status)

    @classmethod
    def success(cls, data=None, msg="success", status=status.HTTP_200_OK, **kwargs):
        """成功响应"""
        return cls(data=data, code=200, msg=msg, status=status, **kwargs)

    @classmethod
    def error(cls, msg="error", code=400, data=None, status=status.HTTP_400_BAD_REQUEST, **kwargs):
        """错误响应"""
        return cls(data=data, code=code, msg=msg, status=status, **kwargs)

    @classmethod
    def auth_error(cls, msg="Authentication error", code=401, data=None, status=status.HTTP_401_UNAUTHORIZED, **kwargs):
        """认证错误响应"""
        return cls(data=data, code=code, msg=msg, status=status, **kwargs)

    @classmethod
    def token_expired(cls, msg="Token has expired", code=40101, data=None, status=status.HTTP_401_UNAUTHORIZED, **kwargs):
        """Token过期响应"""
        return cls(data=data, code=code, msg=msg, status=status, **kwargs)
    
    @classmethod
    def permission_denied(cls, msg="Permission denied", code=403, data=None, status=status.HTTP_403_FORBIDDEN, **kwargs):
        """权限拒绝响应"""
        return cls(data=data, code=code, msg=msg, status=status, **kwargs)
    
    @classmethod
    def not_found(cls, msg="Resource not found", code=404, data=None, status=status.HTTP_404_NOT_FOUND, **kwargs):
        """资源未找到响应"""
        return cls(data=data, code=code, msg=msg, status=status, **kwargs)
    
    @classmethod
    def validation_error(cls, msg="Validation error", code=422, data=None, status=status.HTTP_400_BAD_REQUEST, **kwargs):
        """验证错误响应"""
        return cls(data=data, code=code, msg=msg, status=status, **kwargs)
    
    @classmethod
    def server_error(cls, msg="Internal server error", code=500, data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR, **kwargs):
        """服务器错误响应"""
        return cls(data=data, code=code, msg=msg, status=status, **kwargs)
    
    @classmethod
    def from_drf_response(cls, drf_response, default_msg="操作完成"):
        """
        从Django REST Framework的Response对象转换为APIResponse
        保持原有数据结构的同时统一响应格式
        """
        if not drf_response:
            return cls.error(msg="Unknown error", code=500)
        
        # 提取原始数据
        original_data = drf_response.data if hasattr(drf_response, 'data') else None
        status_code = drf_response.status_code if hasattr(drf_response, 'status_code') else 200
        
        # 提取消息
        if isinstance(original_data, dict):
            msg = original_data.get('detail', 
                  original_data.get('message', 
                  original_data.get('msg', default_msg)))
            # 如果original_data只包含detail/message/msg字段之一，则不重复显示
            if len(original_data) == 1 and any(key in original_data for key in ['detail', 'message', 'msg']):
                data = None
            else:
                data = original_data
        else:
            msg = str(original_data) if original_data else default_msg
            data = original_data
        
        # 根据状态码选择合适的响应类型
        if status_code == 401:
            return cls.auth_error(msg=msg, data=data, status=status_code)
        elif status_code == 403:
            return cls.permission_denied(msg=msg, data=data, status=status_code)
        elif status_code == 404:
            return cls.not_found(msg=msg, data=data, status=status_code)
        elif status_code >= 500:
            return cls.server_error(msg=msg, data=data, status=status_code)
        elif status_code >= 400:
            return cls.error(msg=msg, code=status_code, data=data, status=status_code)
        else:
            return cls.success(msg=msg, data=data, status=status_code) 