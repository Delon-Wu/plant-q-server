#!/bin/bash

# 植物识别系统部署脚本
# 适用于 Ubuntu/Debian 系统

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}开始部署植物识别系统...${NC}"

# 1. 更新系统
echo -e "${YELLOW}更新系统包...${NC}"
sudo apt update && sudo apt upgrade -y

# 2. 安装必要的系统包
echo -e "${YELLOW}安装系统依赖...${NC}"
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    postgresql \
    postgresql-contrib \
    redis-server \
    nginx \
    supervisor \
    git \
    curl \
    build-essential \
    libpq-dev \
    python3-dev \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    libpng-dev \
    zlib1g-dev

# 3. 创建项目目录
echo -e "${YELLOW}创建项目目录...${NC}"
sudo mkdir -p /var/www/plant-q-server
sudo mkdir -p /var/log/plant-q-server
sudo chown $USER:$USER /var/www/plant-q-server
sudo chown $USER:$USER /var/log/plant-q-server

# 4. 克隆项目（如果从 Git 仓库部署）
echo -e "${YELLOW}克隆项目代码...${NC}"
cd /var/www/
# git clone your-repository-url plant-q-server
# 或者您可以直接上传代码到服务器

# 5. 创建虚拟环境
echo -e "${YELLOW}创建 Python 虚拟环境...${NC}"
cd /var/www/plant-q-server
python3 -m venv venv
source venv/bin/activate

# 6. 安装 Python 依赖
echo -e "${YELLOW}安装 Python 依赖包...${NC}"
pip install --upgrade pip
pip install -r /home/delon/plant-q-server/requirements.txt
pip install gunicorn psycopg2-binary django-redis

# 7. 设置 PostgreSQL 数据库
echo -e "${YELLOW}配置 PostgreSQL 数据库...${NC}"
sudo -u postgres psql << EOF
CREATE DATABASE plant_q_db;
CREATE USER plant_q_user WITH PASSWORD 'your-secure-password';
ALTER ROLE plant_q_user SET client_encoding TO 'utf8';
ALTER ROLE plant_q_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE plant_q_user SET timezone TO 'Asia/Shanghai';
GRANT ALL PRIVILEGES ON DATABASE plant_q_db TO plant_q_user;
\q
EOF

# 8. 配置 Redis
echo -e "${YELLOW}配置 Redis...${NC}"
# sudo systemctl enable redis-server
# sudo systemctl start redis-server

# 9. 创建环境变量文件
echo -e "${YELLOW}配置环境变量...${NC}"
cd /home/delon/plant-q-server
cp .env.production .env
echo -e "${RED}请编辑 .env 文件，填入正确的配置信息${NC}"

# 10. Django 设置
echo -e "${YELLOW}运行 Django 迁移...${NC}"
export DJANGO_SETTINGS_MODULE=config.production_settings
python manage.py collectstatic --noinput
python manage.py migrate

# 11. 创建超级用户（可选）
echo -e "${YELLOW}创建 Django 超级用户...${NC}"
echo "请按提示创建管理员账户："
python manage.py createsuperuser

echo -e "${GREEN}基础部署完成！${NC}"
echo -e "${YELLOW}接下来需要配置 Nginx 和 Supervisor...${NC}"
