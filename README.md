# Django 投票系统

一个基于 Django 的在线投票系统，支持用户注册、登录、创建投票、参与投票等功能。

## 项目简介

你好，世界！

这是一个我的第一个Django项目，我通过完成DjangoVote来学习Django框架的基本原理的实践，该项目同样适合Django初学者，可以帮助快速认识Django框架。在此系统中，用户可以注册账号、创建投票、参与其他用户的投票，并查看投票结果和统计信息。

## 主要功能

### 用户管理
- ✅ 用户注册（账号、姓名、邮箱、密码）
- ✅ 用户登录/登出
- ✅ 用户中心（显示用户统计信息）

### 投票功能
- ✅ 创建投票（支持问题标题、描述、多个选项）
- ✅ 查看所有投票列表
- ✅ 查看投票详情
- ✅ 参与投票（每个用户对每个投票只能投一次）
- ✅ 查看投票结果（实时统计票数）
- ✅ 查看我创建的投票
- ✅ 查看我参与的投票

### 数据统计
- ✅ 用户发布的投票数
- ✅ 参与用户投票的总人数
- ✅ 用户参与的投票数量
- ✅ 最近投票展示

## 技术栈

- **后端框架**: Django 5.2.7
- **数据库**: MySQL
- **前端**: HTML + CSS + JavaScript
- **认证方式**: Session 认证

## 项目结构

```
DjangoProject/
├── app/                    # 应用目录
│   ├── dashboard/         # 仪表板应用
│   │   ├── models.py      # 数据模型
│   │   ├── views.py       # 视图函数
│   │   ├── urls.py        # URL路由
│   │   └── templates/     # 模板文件
│   ├── login/             # 登录注册应用
│   │   ├── models.py      # 用户模型
│   │   ├── views.py       # 登录注册视图
│   │   ├── urls.py        # URL路由
│   │   └── templates/     # 模板文件
│   └── polls/             # 投票应用
│       ├── models.py      # 投票、选项、投票记录模型
│       ├── views.py       # 投票相关视图
│       ├── urls.py        # URL路由
│       └── templates/     # 模板文件
├── mysite/                # 项目配置文件
│   ├── settings.py        # 项目设置
│   ├── urls.py            # 主URL配置
│   └── wsgi.py            # WSGI配置
├── static/                # 静态文件（CSS、JS）
├── media/                 # 媒体文件
├── manage.py              # Django管理脚本
└── requirements.txt       # 项目依赖

```

## 数据模型

### 用户模型 (userInfo)
- `account`: 账号（唯一）
- `name`: 姓名
- `email`: 邮箱（唯一）
- `password`: 密码
- `register_time`: 注册时间

### 投票模型 (poll)
- `poll_id`: 投票ID（主键）
- `question`: 问题标题
- `question_description`: 问题描述
- `pub_date`: 发布时间
- `created_by`: 创建人（外键关联用户）

### 选项模型 (choice)
- `poll`: 所属投票（外键）
- `choice_text`: 选项文本
- `votes`: 票数

### 投票记录模型 (vote)
- `poll`: 投票（外键）
- `choice`: 选项（外键）
- `voter`: 投票人（外键关联用户）
- `voted_at`: 投票时间
- 唯一约束：每个用户对每个投票只能投一次

## 安装与运行

### 环境要求

- Python 3.8+
- MySQL 5.7+
- Django 5.2.7

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/Li-xiaotong-cauc/DjangoVote.git
cd DjangoProject
```

2. **创建虚拟环境（推荐）**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置数据库**

在 MySQL 中创建数据库：
```sql
create database DjangoProject_DB DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

5. **配置数据库连接**

编辑 `mysite/settings.py`，修改数据库配置：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DjangoProject_DB',
        'USER': 'root',
        'PASSWORD': 'YourPassword',
        'HOST': '127.0.0.1',
        'PORT': 3306
    }
}
```

6. **运行数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **创建超级用户（可选）**
```bash
python manage.py createsuperuser
```

8. **运行开发服务器**
```bash
python manage.py runserver
```

9. **访问应用**

打开浏览器访问：
- 主页: http://127.0.0.1:8000/
- 登录页: http://127.0.0.1:8000/login/
- 投票列表: http://127.0.0.1:8000/polls/
- 管理后台: http://127.0.0.1:8000/admin/

## 主要路由

### 登录注册
- `/login/` - 登录页面
- `/login/register` - 注册页面
- `/login/logout/` - 登出

### 仪表板
- `/` - 主页（需要登录）
- `/welcome/` - 欢迎页
- `/userCenter/` - 用户中心（需要登录）

### 投票功能
- `/polls/` - 投票列表
- `/polls/poll_id=<int:poll_id>/` - 投票详情
- `/polls/create/` - 创建投票
- `/polls/my_polls/` - 我创建的投票
- `/polls/voted_polls/` - 我参与的投票

## 项目特性

- 🔐 用户认证系统（基于Session）
- 📊 投票统计功能
- 🔒 防止重复投票（每个用户对每个投票只能投一次）
- 📱 响应式设计
- 🎨 友好的用户界面
- 📈 实时投票结果展示

## 开发说明

### 代码规范
- 使用 Django 标准项目结构
- 视图函数命名采用下划线命名法
- 模型类使用驼峰命名法

### 注意事项
1. 生产环境部署前，请修改 `SECRET_KEY`
2. 将 `DEBUG` 设置为 `False`
3. 配置合适的 `ALLOWED_HOSTS`
4. 建议使用 HTTPS
5. 密码应进行加密存储（当前为明文存储，仅用于开发）

## 后续优化建议

- [ ] 密码加密存储（使用 Django 的密码哈希）
- [ ] 添加邮箱验证功能
- [ ] 添加投票截止时间功能
- [ ] 添加投票分类/标签功能
- [ ] 添加评论功能
- [ ] 添加投票搜索功能
- [ ] 添加数据导出功能
- [ ] 优化前端UI/UX
- [ ] 添加API接口
- [ ] 添加单元测试

## 许可证

本项目采用 MIT 许可证。

## 作者

📞 联系方式

GitHub: @Li-xiaotong-cauc

email:L17785363505@163.com

QQ：3110893251

如果有部署或其他问题欢迎联系本人！

项目链接: https://github.com/Li-xiaotong-cauc/DjangoVote

## 🙏 致谢

感谢Django社区提供的优秀文档

感谢所有测试和提供反馈的用户