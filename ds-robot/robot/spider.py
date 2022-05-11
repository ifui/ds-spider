
from datetime import datetime, timedelta
import scrapy
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class RobotSpider(scrapy.Spider):
    """
    封装的基础类
    """
    to_email = None
    start_time = None
    end_time = None
    title = ''

    def __init__(self, start_time=None, end_time=None, to_email=None, *args, **kwargs):
        super(RobotSpider, self).__init__(*args, **kwargs)
        self.to_email = to_email

        # 转换时间格式
        nowTime = datetime.strftime(datetime.now(), "%Y%m%d")
        self.start_time = datetime.strptime(start_time or nowTime, "%Y%m%d")
        self.end_time = datetime.strptime(end_time or nowTime, "%Y%m%d")
        self.resolve_filter_date(start_time=start_time, end_time=end_time)

    # 分析起止时间，生成链接池
    def resolve_filter_date(self, start_time=None, end_time=None):
        if not start_time:
            return

        self.start_urls = []
        temp_start_time = self.start_time

        while temp_start_time <= self.end_time:
            url = self.resolve_date_url(temp_start_time)

            self.start_urls.append(url)

            temp_start_time += timedelta(days=1)

    # 返回格式化后的时间（一般需要重写该方法）
    def resolve_date_url(self, time):
        return time
