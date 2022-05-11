# DS Robot

基于 `Scrapy` + `Scrapyd`  开发的爬虫服务

## 快速上手

### 1. 生成配置文件

#### 1.1 将 `robot/.env-example` 重命名为 `.env`

参考配置说明填写相应配置，更详细的配置请参考 `robot/settings.py`

#### 1.2 将 `scrapy-example.cfg` 重命名为 `scrapy.cfg`

主要是 `scrapyd` 和 `scrapy-client` 的相关配置

建议使用 `scrapy-deploy` 命令向服务器推送爬虫项目

> 注意： 默认需要的数据库是 `Mongodb`

### 2. 测试

在 `robot` 目录下

`python manage.py`

### 3. 发布

#### 3.1 配置 `scrapy.cfg`

在 `scrapy.cfg` 文件中加入以下内容（默认已添加）

```bash
#  参考配置，deploy-name 可自命名
[deploy:deploy-name]
# 远程服务器地址
url = http://localhost:6800/
# 项目名
project = robot
# 用户名
username = robot
# 密码
password = robot
# 版本可选（发布命令时可以指定）
# version = 202x-xx-xx
```

#### 3.2 发布：

`scrapyd-deploy deploy-name -p robot --version 202x-xx-xx`