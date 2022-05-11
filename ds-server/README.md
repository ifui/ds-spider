# DS Server

基于 `Django` + `Scrapyd` 开发的爬虫后台管理服务系统

## 特性

- 爬虫服务器分布式管理
- 爬虫项目启动、暂停、删除等功能
- 定时任务
- 日志功能
- 附件打包下载

## 快速上手

### 1. 配置文件

`cp .env-example .env`

请注意如果部署在线上请修改 `.env` 文件中的 `SECRET_KEY`

## 部署方式

推荐使用 `uwsgi` 部署，本项目提供了 `uwsgi.ini` 配置文件

有两种部署方式：
1. `Django` 项目部署，请参考[Django官网部署方式](https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/uwsgi/)
2. `Docker` 一键部署，请参考[DS Spider](https://github.com/ds-spider)

