# Fit Synapse Backend

基于Django REST framework的后端API系统，使用JWT进行身份认证。

## 功能特性

- 用户认证系统（注册、登录、登出）
- JWT token认证
- 用户信息管理
- 密码修改
- CORS支持
- RESTful API设计

## 技术栈

- Python 3.8+
- Django 5.0.2
- Django REST framework 3.14.0
- Simple JWT 5.3.1
- Django CORS Headers 4.3.1
- Django Filter 23.5

## 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd fit-synapse-server
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

5. 创建超级用户（可选）
```bash
python manage.py createsuperuser
```

6. 运行开发服务器
```bash
python manage.py runserver
```

## API文档

### 认证相关接口

#### 注册新用户
- **URL**: `/api/accounts/register/`
- **Method**: `POST`
- **Data**:
  ```json
  {
    "email": "user@example.com",
    "username": "username",
    "password": "password123",
    "password2": "password123",
    "phone": "1234567890"
  }
  ```

#### 用户登录
- **URL**: `/api/accounts/login/`
- **Method**: `POST`
- **Data**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

#### 刷新Token
- **URL**: `/api/accounts/login/refresh/`
- **Method**: `POST`
- **Data**:
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

#### 用户登出
- **URL**: `/api/accounts/logout/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <access_token>`
- **Data**:
  ```json
  {
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

### 用户信息相关接口

#### 获取/更新用户信息
- **URL**: `/api/accounts/profile/`
- **Method**: 
  - `GET`: 获取用户信息
  - `PUT`: 更新用户信息
- **Headers**: `Authorization: Bearer <access_token>`
- **Data** (PUT):
  ```json
  {
    "username": "new_username",
    "phone": "9876543210"
  }
  ```

#### 修改密码
- **URL**: `/api/accounts/change-password/`
- **Method**: `PUT`
- **Headers**: `Authorization: Bearer <access_token>`
- **Data**:
  ```json
  {
    "old_password": "oldpassword123",
    "new_password": "newpassword123",
    "new_password2": "newpassword123"
  }
  ```

## 开发说明

### 项目结构
```
fit-synapse-server/
├── accounts/                 # 用户管理应用
│   ├── models.py            # 用户模型
│   ├── serializers.py       # 序列化器
│   ├── views.py            # 视图
│   └── urls.py             # URL配置
├── config/                  # 项目配置
│   ├── settings.py         # 项目设置
│   ├── urls.py             # 主URL配置
│   └── wsgi.py             # WSGI配置
├── media/                   # 媒体文件
├── static/                  # 静态文件
├── requirements.txt         # 项目依赖
└── manage.py               # Django管理脚本
```

### 环境变量
在开发环境中，你可以创建一个`.env`文件来存储环境变量：
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 安全说明

- 在生产环境中，请确保修改`SECRET_KEY`
- 设置适当的`ALLOWED_HOSTS`
- 关闭`DEBUG`模式
- 配置适当的CORS设置
- 使用HTTPS
- 定期更新依赖包

## 许可证

[MIT License](LICENSE) 