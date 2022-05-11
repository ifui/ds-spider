# Scrapy settings for robot project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
from datetime import datetime

from environs import Env

BOT_NAME = 'robot'

# 项目路径
BASE_PATH = os.path.dirname(__file__)

# 加载 env
env = Env()
Env.read_env()

SPIDER_MODULES = ['robot.spiders']
NEWSPIDER_MODULE = 'robot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'robot (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-cn',
}
# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'robot.middlewares.RobotSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'robot.middlewares.RandomUserAgentMiddleware': 542,
    # 'robot.middlewares.RobotDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    #    'scrapy.extensions.telnet.TelnetConsole': None,
    'robot.extensions.SendEmail': 400,  # 发送通知邮件
    'robot.extensions.ArchiveJob': 500,  # 打包文件
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #    'robot.pipelines.RobotPipeline': 300,
    'robot.pipelines.MongoPipeline': 500,  # 数据存储中间件
    'robot.pipelines.ImagespiderPipeline': 200,  # 图片资源下载中间件
    'robot.pipelines.ThumbspiderPipeline': 300,  # 版面图片下载中间件
    'robot.pipelines.PDFspiderPipeline': 400,  # PDF下载中间件
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# Job Id 表示使用 scrapyd 执行任务时所生成的 job id
JOB_ID = os.getenv("SCRAPY_JOB") or datetime.strftime(
    datetime.now(), '%Y-%m-%d')

# 时间路径 eg: 2022/02/14
DATETIME_PATH = datetime.strftime(datetime.now(), '%Y/%m/%d')

# 附件路径 eg: /public/2022/02/14
PUBLIC_PATH = os.path.join(env('PUBLIC_PATH'), DATETIME_PATH)

# 打包路径 eg: /archives
ARCHIVE_PATH = env('ARCHIVE_PATH')

# 图片和文件保存路径 eg: /public/2022/02/14
IMAGES_STORE = PUBLIC_PATH
FILES_STORE = PUBLIC_PATH

# 当前时间，eg：2021-09-01 01:02:03
DATETIME_NOW = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

# JSON 文件名
FEED_JSON_PATH = PUBLIC_PATH + '/%(name)s/%(name)s_' + JOB_ID + '.json'

FEEDS = {
    FEED_JSON_PATH: {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'item_classes': ['mullet.items.MulletItem'],
        'fields': None,
        'indent': 2,
        'item_export_kwargs': {
            'export_empty_fields': True,
        },
    },
}

# mongodb 设置
MONGO_HOST = env('MONGO_HOST')
MONGO_PORT = env.int('MONGO_PORT')
MONGO_DBNAME = env('MONGO_NAME')
MONGO_USERNAME = env('MONGO_USERNAME')
MONGO_PASSWORD = env('MONGO_PASSWORD')

# 邮件通知设置
MAIL_HOST = env('MAIL_HOST')
MAIL_PORT = env.int('MAIL_PORT')

MAIL_FROM = env('MAIL_FROM')
MAIL_USER = env('MAIL_USER')
MAIL_PASS = env('MAIL_PASS')
MAIL_SSL = env.bool('MAIL_SSL')
MAIL_TLS = env.bool('MAIL_TLS')

# TO_EMAIL = ['ifui@foxmail.com']
TO_EMAIL = env.list('TO_EMAIL')
