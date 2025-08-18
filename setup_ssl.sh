#!/bin/bash

# SSL 证书配置脚本（使用 Let's Encrypt）

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 检查参数
if [ $# -eq 0 ]; then
    echo -e "${RED}用法: $0 <domain-name>${NC}"
    echo -e "例如: $0 example.com"
    exit 1
fi

DOMAIN=$1

echo -e "${GREEN}为域名 $DOMAIN 配置 SSL 证书...${NC}"

# 1. 安装 Certbot
echo -e "${YELLOW}安装 Certbot...${NC}"
sudo apt update
sudo apt install -y certbot python3-certbot-nginx

# 2. 获取 SSL 证书
echo -e "${YELLOW}获取 SSL 证书...${NC}"
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN

# 3. 设置自动续期
echo -e "${YELLOW}设置证书自动续期...${NC}"
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -

# 4. 测试续期功能
echo -e "${YELLOW}测试证书续期...${NC}"
sudo certbot renew --dry-run

# 5. 更新 Django 设置以使用 HTTPS
echo -e "${YELLOW}更新 Django HTTPS 设置...${NC}"
cat >> /var/www/plant-q-server/.env << EOF

# HTTPS 设置
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
EOF

# 重启服务
sudo supervisorctl restart plant-q-server:plant-q-django

echo -e "${GREEN}SSL 证书配置完成！${NC}"
echo -e "${YELLOW}现在可以通过 https://$DOMAIN 访问您的应用${NC}"
