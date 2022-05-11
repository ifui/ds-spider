# DS Spider

基于 `Scrapy` + `Scrapyd` + `Django` + `Next.js` 构建的分布式爬虫服务管理系统

![图片](https://github.com/ifui/resources/blob/main/ds-spider/WX20220510-155840.png)

## 特性

- 爬虫服务器分布式管理
- 爬虫项目启动、暂停、删除等功能
- 定时任务
- 日志功能
- 附件打包下载
- 界面可视化控制
- 支持容器化部署
- 支持邮件推送提醒功能

## 快速上手

本项目是将3个子项目整合到一块通过 `Docker` 进行部署，你完全可以将之拆分

运行本项目只需要拥有 `Docker` 环境即可

### 1. 配置文件

请参考

[ds-robot README.md](https://github.com/ds-spider/ds-robot/README.md)

[ds-admin README.md](https://github.com/ds-spider/ds-admin/README.md)

[ds-server README.md](https://github.com/ds-spider/ds-server/README.md)

### 1. 构建容器

在项目根目录下

> 容器配置文件在 `.env` 中，都有详细说明

执行命令： `docker-compose up -d`

该命令会将以下四个容器编组到一块，到时候请注意相互之间的关系

1. mongodb
2. ds-robot
3. ds-server
4. ds-admin

### 2. 创建管理员账号密码

根据提示操作即可

`docker-compose exec server python manage.py createsuperuser`

### 3. 打开后台管理界面

然后使用浏览器访问 `http://127.0.0.1:3000`



