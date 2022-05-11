from robot.items import RobotItem
import scrapy
import re
from datetime import datetime, timedelta
from robot.spider import RobotSpider

# 匹配日期
datePattern = re.compile(r'.*日')


class A81cnSpider(RobotSpider):
    title = '解放军报'
    name = '81cn'
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

        sectionUrls = response.xpath(
            '//*[@id="APP-SectionNav"]//li/a/@href').getall()
        base_url = self.get_base_url(response)
        for url in sectionUrls:
            yield scrapy.Request(base_url + url, self.resolve_page_urls)

    # 解析目录中的新闻
    def resolve_page_urls(self, response):
        areas = response.xpath('//map/area')
        base_url = self.get_base_url(response)
        for area in areas:
            areaUrl = area.xpath('./@href').extract_first()
            params = {}
            params['coords'] = area.xpath('./@coords').extract_first()
            yield scrapy.Request(url=base_url + areaUrl, callback=self.parse, cb_kwargs=params)

    # 整理数据
    def parse(self, response, coords):
        items = RobotItem()
        items['copyfrom'] = '解放军报'

        items['origin_url'] = response.url

        items['coords'] = coords

        items['pre_title'] = response.xpath(
            '//*[@id="APP-PreTitle"]/text()').extract_first()

        items['title'] = response.xpath(
            '//*[@id="APP-Title"]/text()').extract_first()

        items['sub_title'] = response.xpath(
            '//*[@id="APP-Subtitle"]/text()').extract_first()

        items['author'] = response.xpath(
            '//*[@id="APP-Author"]/text()').extract_first()

        items['section'] = response.xpath(
            'normalize-space(//span[@class="badge-info"])').extract_first()

        date = response.xpath(
            '//div[@class="nav-site"]/p[2]/text()').extract_first()
        items['date'] = datePattern.match(date).group().replace(
            '年', '/').replace('月', '/').replace('日', '')

        # 图片资源信息（包含介绍）
        attachment = response.xpath('//*[@class="attachment-image APP-Image"]')
        base_url = self.get_base_url(response)
        items['image_urls'] = []
        for item in attachment:
            image_url = item.xpath('.//img/@src').extract_first()
            image_info = item.xpath('.//td/text()').extract_first()
            if (image_url):
                items['image_urls'].append({
                    'url': base_url + image_url,
                    'info': image_info or '',
                })

        contents = response.xpath(
            '//*[@id="APP-Content"]/founder-content/*').extract()
        items['content'] = ''.join(contents)
        image_format = ''
        for image in items['image_urls']:
            image_format += "<img src='{0}' />".format(image['url'])
            if image['info']:
                image_format += "<p>{0}</p>".format(image['info'])

        items['content'] = image_format + items['content']

        items['upload_path'] = self.name + '/uploads/' + items['date']

        yield items

    # 返回 base url
    def get_base_url(self, response):
        return re.match('.*\/', response.url).group()
