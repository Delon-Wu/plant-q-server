#!/bin/bash

# 系统监控脚本

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}植物识别系统状态监控${NC}"
echo "================================"

# 1. 系统资源监控
echo -e "${YELLOW}系统资源使用情况：${NC}"
echo "CPU 使用率："
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1

echo "内存使用情况："
free -h

echo "磁盘使用情况："
df -h | grep -E "(/$|/var)"

echo ""

# 2. 服务状态检查
echo -e "${YELLOW}服务状态：${NC}"
echo "Nginx 状态："
sudo systemctl is-active nginx

echo "PostgreSQL 状态："
sudo systemctl is-active postgresql

echo "Redis 状态："
sudo systemctl is-active redis-server

echo "Supervisor 服务："
sudo supervisorctl status

echo ""

# 3. 应用健康检查
echo -e "${YELLOW}应用健康检查：${NC}"
echo "Django 应用响应："
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/admin/ || echo "连接失败"

echo ""

# 4. 日志检查
echo -e "${YELLOW}最近的错误日志：${NC}"
echo "Django 错误日志（最近 10 行）："
tail -10 /var/log/plant-q-server/supervisor_django.log | grep -i error || echo "无错误"

echo "Nginx 错误日志（最近 5 行）："
sudo tail -5 /var/log/nginx/plant-q-server.error.log || echo "无错误"

echo ""

# 5. 进程监控
echo -e "${YELLOW}相关进程：${NC}"
ps aux | grep -E "(gunicorn|celery|nginx)" | grep -v grep

echo ""

# 6. 网络连接
echo -e "${YELLOW}网络连接：${NC}"
netstat -tlnp | grep -E "(80|443|8000|6379|5432)"

echo ""
echo -e "${GREEN}监控完成${NC}"
