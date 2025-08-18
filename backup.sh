#!/bin/bash

# 数据库和媒体文件备份脚本

set -e

# 配置
BACKUP_DIR="/var/backups/plant-q-server"
DB_NAME="plant_q_db"
DB_USER="plant_q_user"
MEDIA_DIR="/var/www/plant-q-server/media"
RETENTION_DAYS=30

# 创建备份目录
mkdir -p $BACKUP_DIR

# 时间戳
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "开始备份植物识别系统数据..."

# 1. 备份数据库
echo "备份数据库..."
pg_dump -U $DB_USER -h localhost $DB_NAME | gzip > $BACKUP_DIR/database_$TIMESTAMP.sql.gz

# 2. 备份媒体文件
echo "备份媒体文件..."
tar -czf $BACKUP_DIR/media_$TIMESTAMP.tar.gz -C $MEDIA_DIR .

# 3. 删除过期备份
echo "清理过期备份..."
find $BACKUP_DIR -name "database_*.sql.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "media_*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "备份完成！"
echo "数据库备份: $BACKUP_DIR/database_$TIMESTAMP.sql.gz"
echo "媒体文件备份: $BACKUP_DIR/media_$TIMESTAMP.tar.gz"

# 显示备份文件大小
ls -lh $BACKUP_DIR/*$TIMESTAMP*
