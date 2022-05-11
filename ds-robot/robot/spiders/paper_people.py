from datetime import datetime, timedelta
import scrapy
import re
from robot.items import RobotItem
from robot.spider import RobotSpider

# 匹配日期
datePattern = re.compile(r'\d{4,}年.*日')

# 匹配空白符
blankPattern = re.compile(r'\s')

# 匹配数字
numberPattern = re.compile(r'\d+')


class PaperPeople(RobotSpider):
    title = '人民日报'
    name = 'people'
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
            yield scrapy.Request(base_url + url, self.resolve_page_urls)

    # 解析新闻链接
    def resolve_page_urls(self, response):
        areas = response.xpath('//map//area')
        base_url = self.get_base_url(response)
        for area in areas:
            areaUrl = area.xpath('./@href').extract_first()
            params = {}
            params['coords'] = area.xpath('./@coords').extract_first()
            yield scrapy.Request(url=base_url + areaUrl, callback=self.parse_robot_item, cb_kwargs=params)

     # 整理新闻数据
    def parse_robot_item(self, response, coords):
        items = RobotItem()
        items['copyfrom'] = '人民日报'

        items['origin_url'] = response.url

        items['coords'] = coords

        items['pre_title'] = response.xpath(
            '//div[@class="article"]/h3/text()').extract_first()

        items['title'] = response.xpath(
            '//div[@class="article"]/h1/text()').extract_first()

        items['sub_title'] = response.xpath(
            '//div[@class="article"]/h2/text()').extract_first()

        author = response.xpath(
            '//div[@class="article"]/p[@class="sec"]/text()').extract()
        items['author'] = blankPattern.sub('', ''.join(author))

        # 图片资源信息（包含介绍）
        attachment = response.xpath('//table[@class="pci_c"]//tbody')
        base_url = self.get_base_url(response)
        items['image_urls'] = []
        for item in attachment:
            image_url = item.xpath('.//img/@src').extract_first()
            image_info = item.xpath('.//p/text()').extract()
            if (image_url):
                items['image_urls'].append({
                    'url': base_url + image_url,
                    'info': ''.join(image_info) or '',
                })

        contents = response.xpath('//div[@id="ozoom"]//p').extract()
        items['content'] = ''.join(contents)
        image_format = ''
        for image in items['image_urls']:
            image_format += "<img src='{0}' />".format(image['url'])
            if image['info']:
                image_format += "<p>{0}</p>".format(image['info'])

        items['content'] = re.sub(
            '\u3000', '', image_format + items['content'])

        date = response.xpath(
            '//div[@class="date-box"]/p[@class="date left"]/text()').extract_first()
        items['date'] = datePattern.search(date).group().replace(
            '年', '/').replace('月', '/').replace('日', '')

        items['section'] = response.xpath(
            '//div[@class="paper-bot"]/p[@class="left ban"]/text()').extract_first()

        items['upload_path'] = self.name + '/uploads/' + items['date']

        yield items

    # 返回 base url
    def get_base_url(self, response):
        return re.match('.*\/', response.url).group()
