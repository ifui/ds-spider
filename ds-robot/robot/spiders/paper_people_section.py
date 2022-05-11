from datetime import datetime, timedelta
import scrapy
import re
from robot.items import SectionItem
from robot.spider import RobotSpider

# 匹配日期
datePattern = re.compile(r'\d{4,}年.*日')

# 匹配空白符
blankPattern = re.compile(r'\s')

# 匹配数字
numberPattern = re.compile(r'\d+')


class PaperPeople(RobotSpider):
    title = '人民日报-版面'
    name = 'people_section'
    allowed_domains = ['paper.people.com.cn']

    start_urls = ['http://paper.people.com.cn/rmrb/index.html']

    # 解析按时间筛选的链接
    def resolve_date_url(self, time):
        return "http://paper.people.com.cn/rmrb/html/%s/nbs.D110000renmrb_01.htm" % time.strftime("%Y-%m/%d")

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.resolve_section_urls)

    # 解析版面URL
    def resolve_section_urls(self, response):
        sectionUrls = response.xpath('//*[@id="pageLink"]/@href').getall()
        base_url = self.get_base_url(response)
        for url in sectionUrls:
            yield scrapy.Request(base_url + url, self.parse_section_item)

    # 整理版面数据
    def parse_section_item(self, response):
        items = SectionItem()
        base_url = self.get_base_url(response)

        items['copyfrom'] = '人民日报'

        items['origin_url'] = response.url

        items['name'] = response.xpath(
            '//div[@class="paper-bot"]/p[@class="left ban"]/text()').extract_first()

        date = response.xpath(
            '//div[@class="date-box"]/p[@class="date left"]/text()').extract_first()
        items['date'] = datePattern.search(date).group().replace(
            '年', '/').replace('月', '/').replace('日', '')

        items['sort'] = numberPattern.search(items['name']).group()

        items['thumb_url'] = base_url + response.xpath(
            '//div[@class="paper"]/img[@usemap="#PagePicMap"]/@src').extract_first()

        items['pdf_url'] = base_url + response.xpath(
            '//div[@class="paper-bot"]/p[@class="right btn"]/a/@href').extract_first()

        items['upload_path'] = self.name + '/uploads/' + items['date']

        yield items

    # 返回 base url
    def get_base_url(self, response):
        return re.match('.*\/', response.url).group()
