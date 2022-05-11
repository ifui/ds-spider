# DS Admin

基于 [Next.js](https://nextjs.org/) + [DS Server](https://github.com/ifui/ds-spider/ds-server) 开发的可视化爬虫服务管理后台页面

## 快速上手(本地测试开发)

### 1. 配置后端服务器地址
   
更改`app/.env`中的`NEXT_PUBLIC_BASE_URL`设置

### 2. 安装依赖并启动开发服务
  
`yarn && yarn dev`

## 快捷部署

具体部署方式请参考[Next.js官网的部署方式](https://nextjs.org/docs/deployment)

本项目还提供了 `Dockerfile` 文件

你也可以参考 [DS Spider](https://github.com/ds-spider) 的 `docker-compose.yml` 文件部署属于你自己的容器服务

## 配置文件

具体配置请参考[Next.js官网](https://nextjs.org/docs/api-reference/next.config.js/introduction)