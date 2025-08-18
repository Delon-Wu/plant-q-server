# 植物识别系统云服务器部署指南

本指南将帮助您将植物识别系统部署到云服务器上。

## 系统要求

- Ubuntu 20.04+ 或 Debian 10+
- 至少 2GB RAM
- 至少 20GB 存储空间
- Python 3.8+

## 快速部署步骤

### 1. 准备服务器

首先连接到您的云服务器：

```bash
ssh your-username@your-server-ip
```

### 2. 上传项目文件

将项目文件上传到服务器：

```bash
# 方法一：使用 scp
scp -r /path/to/plant-q-server your-username@your-server-ip:/home/your-username/

# 方法二：使用 rsync
rsync -avz /path/to/plant-q-server your-username@your-server-ip:/home/your-username/

# 方法三：从 Git 仓库克隆
git clone your-repository-url /home/your-username/plant-q-server
```

### 3. 运行部署脚本

```bash
cd /home/your-username/plant-q-server
chmod +x *.sh
sudo ./deploy.sh
```

### 4. 配置环境变量

编辑环境变量文件：

```bash
cd /var/www/plant-q-server
cp .env.production .env
nano .env
```

请填入正确的配置信息：

- `SECRET_KEY`: Django 密钥（生成一个长随机字符串）
- `DB_PASSWORD`: 数据库密码
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥
- `BAIDU_API_KEY` 和 `BAIDU_SECRET_KEY`: 百度 API 密钥
- `DOMAIN_NAME`: 您的域名
- `SERVER_IP`: 服务器 IP 地址

### 5. 配置服务

```bash
sudo ./configure_services.sh
```

### 6. 配置 SSL（可选但推荐）

```bash
sudo ./setup_ssl.sh your-domain.com
```

## 手动部署步骤

如果自动脚本遇到问题，可以按照以下步骤手动部署：

### 1. 安装系统依赖

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib \
    redis-server nginx supervisor git curl build-essential libpq-dev python3-dev \
    libssl-dev libffi-dev libjpeg-dev libpng-dev zlib1g-dev
```

### 2. 创建目录结构

```bash
sudo mkdir -p /var/www/plant-q-server
sudo mkdir -p /var/log/plant-q-server
sudo chown $USER:$USER /var/www/plant-q-server
sudo chown $USER:$USER /var/log/plant-q-server
```

### 3. 复制项目文件

```bash
cp -r /home/your-username/plant-q-server/* /var/www/plant-q-server/
cd /var/www/plant-q-server
```

### 4. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary django-redis
```

### 5. 配置 PostgreSQL

```bash
sudo -u postgres psql
```

在 PostgreSQL 控制台中：

```sql
CREATE DATABASE plant_q_db;
CREATE USER plant_q_user WITH PASSWORD 'your-secure-password';
ALTER ROLE plant_q_user SET client_encoding TO 'utf8';
ALTER ROLE plant_q_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE plant_q_user SET timezone TO 'Asia/Shanghai';
GRANT ALL PRIVILEGES ON DATABASE plant_q_db TO plant_q_user;
\q
```

### 6. 配置 Django

```bash
export DJANGO_SETTINGS_MODULE=config.production_settings
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
```

### 7. 配置 Nginx

```bash
sudo cp nginx.conf /etc/nginx/sites-available/plant-q-server
sudo ln -sf /etc/nginx/sites-available/plant-q-server /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 8. 配置 Supervisor

```bash
sudo cp supervisor.conf /etc/supervisor/conf.d/plant-q-server.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start plant-q-server:*
```

## 维护和监控

### 1. 监控系统状态

```bash
./monitor.sh
```

### 2. 备份数据

```bash
# 手动备份
./backup.sh

# 设置定时备份（每天凌晨 2 点）
echo "0 2 * * * /var/www/plant-q-server/backup.sh" | crontab -
```

### 3. 查看日志

```bash
# Django 应用日志
tail -f /var/log/plant-q-server/supervisor_django.log

# Celery 工作进程日志
tail -f /var/log/plant-q-server/supervisor_celery_worker.log

# Nginx 访问日志
sudo tail -f /var/log/nginx/plant-q-server.access.log

# Nginx 错误日志
sudo tail -f /var/log/nginx/plant-q-server.error.log
```

### 4. 重启服务

```bash
# 重启所有服务
sudo supervisorctl restart plant-q-server:*

# 重启特定服务
sudo supervisorctl restart plant-q-server:plant-q-django
sudo supervisorctl restart plant-q-server:plant-q-celery-worker

# 重启 Nginx
sudo systemctl restart nginx
```

## 故障排除

### 1. 常见问题

**问题：502 Bad Gateway**
- 检查 Gunicorn 进程是否运行：`sudo supervisorctl status`
- 检查日志：`tail -f /var/log/plant-q-server/supervisor_django.log`

**问题：静态文件无法加载**
- 运行：`python manage.py collectstatic --noinput`
- 检查 Nginx 配置中的静态文件路径

**问题：图片上传失败**
- 检查媒体文件目录权限：`sudo chown -R www-data:www-data /var/www/plant-q-server/media/`
- 检查 Nginx 配置中的 `client_max_body_size`

### 2. 性能优化

**数据库优化**
```bash
# 分析数据库性能
sudo -u postgres psql plant_q_db -c "EXPLAIN ANALYZE SELECT * FROM your_table;"
```

**Redis 缓存监控**
```bash
redis-cli info stats
```

## 安全建议

1. **防火墙配置**
   ```bash
   sudo ufw enable
   sudo ufw allow 'Nginx Full'
   sudo ufw allow OpenSSH
   ```

2. **定期更新系统**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **监控登录日志**
   ```bash
   sudo tail -f /var/log/auth.log
   ```

4. **使用强密码和密钥认证**

## 扩展部署

### 1. 负载均衡

如果需要处理更多流量，可以配置多个应用服务器：

```nginx
upstream plant_q_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    location / {
        proxy_pass http://plant_q_backend;
        # ... 其他配置
    }
}
```

### 2. 分离数据库

将数据库部署到单独的服务器，修改 `.env` 文件中的数据库配置。

### 3. CDN 配置

配置 CDN 来加速静态文件和媒体文件的传输。

## 支持

如果部署过程中遇到问题，请：

1. 检查日志文件
2. 确认所有配置文件中的参数正确
3. 验证防火墙和安全组设置
4. 确保服务器资源充足

## 更新应用

当需要更新应用时：

```bash
cd /var/www/plant-q-server
git pull origin main  # 或者重新上传文件
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart plant-q-server:*
```
