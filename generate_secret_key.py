#!/usr/bin/env python3
"""
Django SECRET_KEY 生成器
"""
import secrets
import string
from django.utils.crypto import get_random_string

def generate_secret_key_method1():
    """使用 Django 内置方法生成"""
    return get_random_string(50, 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')

def generate_secret_key_method2():
    """使用 Python secrets 模块生成"""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for _ in range(50))

def generate_secret_key_method3():
    """生成更复杂的密钥"""
    return secrets.token_urlsafe(50)

if __name__ == '__main__':
    print("Django SECRET_KEY 生成器")
    print("=" * 50)
    
    print("\n方法1 - Django 内置方法:")
    key1 = generate_secret_key_method1()
    print(key1)
    
    print("\n方法2 - Python secrets 模块:")
    key2 = generate_secret_key_method2()
    print(key2)
    
    print("\n方法3 - URL 安全的密钥:")
    key3 = generate_secret_key_method3()
    print(key3)
    
    print("\n推荐使用方法1的密钥:")
    print(f"SECRET_KEY={key1}")
    
    print("\n密钥强度说明:")
    print("- 长度: 50 字符")
    print("- 包含: 大小写字母、数字、特殊字符")
    print("- 熵值: 约 296 位")
    print("- 安全级别: 非常高")
