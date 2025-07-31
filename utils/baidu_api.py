# utils/baidu_api.py
import os
import httpx
import base64
import logging
from dotenv import load_dotenv
from django.core.cache import cache

load_dotenv()

logger = logging.getLogger(__name__)

class BaiduPlantAPI:
    @staticmethod
    async def get_access_token():
        """异步获取百度 API 访问令牌（使用缓存优化）"""
        # 先从缓存中获取token
        cache_key = "baidu_api_access_token"
        cached_token = cache.get(cache_key)
        
        if cached_token:
            logger.info("从缓存中获取百度API令牌")
            return cached_token
        
        # 缓存中没有token，重新获取
        api_key = os.getenv("BAIDU_API_KEY")
        secret_key = os.getenv("BAIDU_SECRET_KEY")
        token_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(token_url)
                response.raise_for_status()
                data = response.json()
                access_token = data.get("access_token")
                
                if access_token:
                    # 将token存储到缓存中，设置过期时间为25天（百度token有效期30天，提前5天刷新）
                    cache.set(cache_key, access_token, timeout=25 * 24 * 60 * 60)
                    logger.info("获取新的百度API令牌并存储到缓存")
                
                return access_token
        except Exception as e:
            logger.error(f"获取百度API令牌失败: {e}")
            return None

    @staticmethod
    def clear_access_token_cache():
        """清除缓存中的访问令牌"""
        cache_key = "baidu_api_access_token"
        cache.delete(cache_key)
        logger.info("已清除百度API令牌缓存")

    @staticmethod
    async def identify_plant(image_data: bytes):
        """异步识别植物"""
        access_token = await BaiduPlantAPI.get_access_token()
        if not access_token:
            return {"error": "无法获取API访问令牌"}
        
        api_url = f"https://aip.baidubce.com/rest/2.0/image-classify/v1/plant?access_token={access_token}"
        
        try:
            base64_data = base64.b64encode(image_data).decode("utf-8")
            payload = {"image": base64_data}
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(api_url, data=payload, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            logger.error(f"API请求错误: {e}")
            return {"error": f"API请求失败: {str(e)}"}
        except httpx.HTTPStatusError as e:
            logger.error(f"API返回错误状态码: {e.response.status_code}")
            return {"error": f"API返回错误: {e.response.status_code}"}
        except Exception as e:
            logger.error(f"未知错误: {e}")
            return {"error": f"识别失败: {str(e)}"}