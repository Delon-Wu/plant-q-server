"""
生产环境设置
"""
from .settings import *
import os
from dotenv import load_dotenv
try:
    load_dotenv()
except ImportError:
    pass

# 安全设置
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-super-secret-production-key-here')

# 从环境变量获取域名和IP
domain_name = os.environ.get('DOMAIN_NAME')
server_ip = os.environ.get('SERVER_IP')

if domain_name:
    ALLOWED_HOSTS.extend([
        domain_name,
        f"www.{domain_name}",
        f"api.{domain_name}",  # 如果有 API 子域名
    ])

if server_ip:
    ALLOWED_HOSTS.append(server_ip)

# 始终允许本地开发
ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])


# 数据库设置 - 生产环境建议使用 PostgreSQL 或 MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'plant_q_db'),
        'USER': os.environ.get('DB_USER', 'plant_q_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your-db-password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Redis 缓存设置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', '6379')}/1",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'plant_q',
        'TIMEOUT': 7200,
    }
}

# Celery 配置
CELERY_BROKER_URL = f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', '6379')}/0"
CELERY_RESULT_BACKEND = f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', '6379')}/0"

# 安全设置
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# HTTPS 设置（如果使用 HTTPS）
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS 设置 - 生产环境应该限制域名
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    f"https://{os.environ.get('DOMAIN_NAME')}",
    f"https://www.{os.environ.get('DOMAIN_NAME')}",
    'https://localhost',
    'https://127.0.0.1',
    'https://your-ip-address',  # 硬编码的IP
]

# 静态文件和媒体文件设置
STATIC_ROOT = '/var/www/plant-q-server/static/'
MEDIA_ROOT = '/var/www/plant-q-server/media/'

# 日志设置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/plant-q-server/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
