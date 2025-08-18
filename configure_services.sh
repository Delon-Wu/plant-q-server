#!/bin/bash

# 植物识别系统服务配置脚本

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}配置服务...${NC}"

# 1. 配置 Nginx
echo -e "${YELLOW}配置 Nginx...${NC}"
sudo cp nginx.conf /etc/nginx/sites-available/plant-q-server
sudo ln -sf /etc/nginx/sites-available/plant-q-server /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 测试 Nginx 配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx

# 2. 配置 Supervisor
echo -e "${YELLOW}配置 Supervisor...${NC}"
sudo cp supervisor.conf /etc/supervisor/conf.d/plant-q-server.conf

# 重新加载 Supervisor 配置
sudo supervisorctl reread
sudo supervisorctl update

# 启动服务
sudo supervisorctl start plant-q-server:*

# 3. 设置日志轮转
echo -e "${YELLOW}设置日志轮转...${NC}"
sudo tee /etc/logrotate.d/plant-q-server > /dev/null << EOF
/var/log/plant-q-server/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        sudo supervisorctl restart plant-q-server:*
    endscript
}
EOF

# 4. 配置防火墙（如果使用 UFW）
echo -e "${YELLOW}配置防火墙...${NC}"
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH

# 5. 显示服务状态
echo -e "${GREEN}服务配置完成！${NC}"
echo -e "${YELLOW}服务状态：${NC}"
sudo systemctl status nginx
sudo supervisorctl status

echo -e "${GREEN}部署完成！${NC}"
echo -e "${YELLOW}请访问您的域名或服务器IP查看应用${NC}"
echo -e "${YELLOW}管理后台：http://your-domain.com/admin/${NC}"
echo -e "${YELLOW}API 文档：http://your-domain.com/swagger/${NC}"

echo -e "${RED}重要提醒：${NC}"
echo -e "1. 请确保已正确配置 .env 文件中的所有变量"
echo -e "2. 建议为网站配置 SSL 证书（可使用 Let's Encrypt）"
echo -e "3. 定期备份数据库和媒体文件"
echo -e "4. 监控日志文件，确保应用正常运行"
