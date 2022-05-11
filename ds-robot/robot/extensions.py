import shutil

from htmlmin import minify
from jinja2 import Environment, FileSystemLoader
from scrapy import signals
from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

jinja = Environment(loader=FileSystemLoader(settings['BASE_PATH']))
template = jinja.get_template('./email.html')


class SendEmail:
    """
    发送通知邮件
    """

    def __init__(self, crawler):
        self.crawler = crawler
        self.mailer = MailSender().from_settings(settings)
        # 注册信号
        crawler.signals.connect(self.engine_stopped,
                                signal=signals.engine_stopped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    # 爬虫结束时回调
    def engine_stopped(self):
        if self.crawler.stats.get_value('log_count/ERROR'):
            subject = self.crawler.spider.title + '采集失败通知'
        else:
            subject = self.crawler.spider.title + '采集成功通知'

        body = minify(template.render(data=self.crawler))

        return self.mailer.send(to=settings['TO_EMAIL'],
                                subject=subject,
                                body=body,
                                mimetype='text/html')


class ArchiveJob:
    """
    打包文件夹
    """

    def __init__(self, crawler):
        self.crawler = crawler
        # 注册信号
        crawler.signals.connect(self.engine_stopped,
                                signal=signals.engine_stopped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    # 爬虫结束时回调 打包文件函数
    def engine_stopped(self):
        spider_name = self.crawler.spider.name
        # 文件名 eg: spider_name_jobid
        filename = spider_name + '_' + settings['JOB_ID']
        # 资源路径 eg: /public/2022/02/14/spider_name
        public_path = settings['PUBLIC_PATH'] + '/' + spider_name
        # 打包路径
        archive_path = settings['ARCHIVE_PATH']
        # 当天时间路径
        datetime_path = settings['DATETIME_PATH']
        # 打包的文件名 eg: /archives/2022/02/14/jobid
        archive_file = archive_path + '/' + datetime_path + '/' + filename
        # 打包资源下的所有附件
        shutil.make_archive(archive_file, 'zip', public_path)
