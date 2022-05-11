from robot.items import SectionItem
import scrapy
import re
from datetime import datetime, timedelta
from robot.spider import RobotSpider

# 匹配日期
datePattern = re.compile(r'.*日')

# 匹配数字
numberPattern = re.compile(r'\d+')


class A81cnSpider(RobotSpider):
    title = '解放军报-版面'
    name = '81cn_section'
    allowed_domains = ['81.cn']

    start_urls = ['http://www.81.cn/jfjbmap/paperindex.htm']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.resolve_section_urls)

    # 解析按时间筛选的链接
    def resolve_date_url(self, time):
        return "https://www.81.cn/jfjbmap/content/%s/node_2.htm" % time.strftime("%Y-%m/%d")

    # 解析版面URL
    def resolve_section_urls(self, response):

        sections = response.xpath(
            '//*[@id="APP-SectionNav"]//li/a')
        base_url = self.get_base_url(response)
        for section in sections:
            url = section.xpath('./@href').extract_first()
            params = {}
            params['name'] = section.xpath('./text()').extract_first()
            yield scrapy.Request(url=base_url + url, callback=self.parse, cb_kwargs=params)

    # 整理数据
    def parse(self, response, name):
        items = SectionItem()
        base_url = self.get_base_url(response)

        items['copyfrom'] = '解放军报'

        items['origin_url'] = response.url

        items['name'] = name

        date = response.xpath(
            '//div[@class="nav-site"]/p[2]/text()').extract_first()
        items['date'] = datePattern.match(date).group().replace(
            '年', '/').replace('月', '/').replace('日', '')

        items['sort'] = numberPattern.search(name).group()

        items['thumb_url'] = base_url + \
            response.xpath('//img[@id="APP-Brief"]/@src').extract_first()

        items['pdf_url'] = base_url + \
            response.xpath('//a[@id="APP-Pdf"]/@href').extract_first()

        items['upload_path'] = self.name + '/uploads/' + items['date']
        yield items

    # 返回 base url
    def get_base_url(self, response):
        return re.match('.*\/', response.url).group()
