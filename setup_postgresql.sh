#!/bin/bash

# PostgreSQL 数据库配置脚本

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}配置 PostgreSQL 数据库连接...${NC}"

# 检查是否已安装 psycopg2
echo -e "${YELLOW}检查 PostgreSQL 驱动...${NC}"
source venv/bin/activate
pip install psycopg2-binary

# 创建 .env 文件
echo -e "${YELLOW}创建环境配置文件...${NC}"
if [ ! -f .env ]; then
    cp .env.production .env
    echo -e "${GREEN}.env 文件已创建${NC}"
else
    echo -e "${YELLOW}.env 文件已存在，请手动检查配置${NC}"
fi

# 提示用户输入数据库信息
echo -e "${YELLOW}请输入 PostgreSQL 数据库信息：${NC}"

read -p "数据库名称 (默认: plant_q_db): " db_name
db_name=${db_name:-plant_q_db}

read -p "数据库用户 (默认: plant_q_user): " db_user
db_user=${db_user:-plant_q_user}

read -s -p "数据库密码: " db_password
echo

read -p "数据库主机 (默认: localhost): " db_host
db_host=${db_host:-localhost}

read -p "数据库端口 (默认: 5432): " db_port
db_port=${db_port:-5432}

# 更新 .env 文件
echo -e "${YELLOW}更新环境变量文件...${NC}"
sed -i "s/DB_NAME=.*/DB_NAME=$db_name/" .env
sed -i "s/DB_USER=.*/DB_USER=$db_user/" .env
sed -i "s/DB_PASSWORD=.*/DB_PASSWORD=$db_password/" .env
sed -i "s/DB_HOST=.*/DB_HOST=$db_host/" .env
sed -i "s/DB_PORT=.*/DB_PORT=$db_port/" .env
sed -i "s/USE_POSTGRESQL=.*/USE_POSTGRESQL=True/" .env

# 测试数据库连接
echo -e "${YELLOW}测试数据库连接...${NC}"
export $(cat .env | xargs)
python manage.py check --database default

if [ $? -eq 0 ]; then
    echo -e "${GREEN}数据库连接测试成功！${NC}"
    
    # 运行迁移
    echo -e "${YELLOW}运行数据库迁移...${NC}"
    python manage.py migrate
    
    echo -e "${GREEN}PostgreSQL 配置完成！${NC}"
    echo -e "${YELLOW}现在可以运行服务器：python manage.py runserver${NC}"
else
    echo -e "${RED}数据库连接失败，请检查配置${NC}"
    exit 1
fi
