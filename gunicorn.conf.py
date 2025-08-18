# Gunicorn 配置文件

# 服务器套接字
bind = "127.0.0.1:8000"
backlog = 2048

# 工作进程
workers = 4  # 建议设置为 CPU 核心数的 2-4 倍
worker_class = "sync"
worker_connections = 1000
timeout = 300  # 增加超时时间，适应图片处理
keepalive = 30

# 安全
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# 日志
accesslog = "/var/log/plant-q-server/gunicorn_access.log"
errorlog = "/var/log/plant-q-server/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 进程命名
proc_name = "plant-q-server"

# 用户和组
user = "www-data"
group = "www-data"

# 临时目录
tmp_upload_dir = None

# 启用在操作系统中重用 TCP 连接
reuse_port = True
