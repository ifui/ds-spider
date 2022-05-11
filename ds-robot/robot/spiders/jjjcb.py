from datetime import timedelta
import datetime
import json
import scrapy
from robot.items import RobotItem

from robot.spider import RobotSpider


class JjjcbSpider(RobotSpider):
    title = '中国纪检监察报'

    name = 'jjjcb'

    allowed_domains = ['jjjcb.ccdi.gov.cn']

    # 获取版面列表信息链接地址
    bm_menu = 'https://jjjcb.ccdi.gov.cn/reader/layout/findBmMenu.do'
    # 获取版面内容链接地址
    bm_detail = 'https://jjjcb.ccdi.gov.cn/reader/layout/getBmDetail.do'
    # 获取文章内容链接地址
    bm_detail_data = 'https://jjjcb.ccdi.gov.cn/reader/layout/detailData.do'

    start_urls = []

    def start_requests(self):

        if self.start_urls.__len__ == 0:
            nowTime = datetime.strftime(datetime.now(), "%Y%m%d")
            self.start_urls.append(nowTime)

        for time in self.start_urls:
            params = {
                'time': time
            }
            docPubTime = datetime.datetime.strftime(time, "%Y%m%d")

            yield scrapy.FormRequest(
                url=self.bm_menu,
                callback=self.resolve_section_urls,
                formdata={
                    'docPubTime': docPubTime
                },
                cb_kwargs=params
            )

    # 分析起止时间，生成链接池
    def resolve_filter_date(self, start_time=None, end_time=None):
        if not start_time:
            return

        self.start_urls = []
        temp_start_time = self.start_time

        while temp_start_time <= self.end_time:
            self.start_urls.append(temp_start_time)
            temp_start_time += timedelta(days=1)

    # 分析版面数据
    def resolve_section_urls(self, response, time):
        results = json.loads(response.body)

        for res in results:
            bc = res['IRCATELOG']
            docpubtime = datetime.datetime.strftime(time, "%Y/%m/%d")

            yield scrapy.FormRequest(
                url=self.bm_detail,
                callback=self.resolve_data_urls,
                formdata={
                    'bc': bc,
                    'docpubtime': docpubtime
                },
            )

    # 分析版面内容链接
    def resolve_data_urls(self, response):
        results = json.loads(response.body)

        for res in results:
            guid = res['ZB_GUID']
            url = "%s?guid=%s" % (self.bm_detail_data, guid)
            yield scrapy.Request(url, self.parse)

    # 解析内容
    def parse(self, response):
        data = json.loads(response.body)

        items = RobotItem()
        base_url = 'https://jjjcb.ccdi.gov.cn/epaper/'

        date = datetime.datetime.strptime(
            data['docPubTime'], '%Y/%m/%d %H:%M:%S')

        items['copyfrom'] = '中国纪检监察报'

        items['origin_url'] = response.url

        items['coords'] = data['zb']

        items['pre_title'] = data['yt']

        items['title'] = data['docTitle']

        items['sub_title'] = data['fb']

        items['author'] = data['docAuthor']

        items['section'] = "第%s版：%s" % (data['bc'], data['bm'])

        items['date'] = date.strftime("%Y/%m/%d")

        # 图片资源信息
        items['image_urls'] = []
        ctpath = data['ctpath'].split(';')
        ts = data['ctpath'].split(';')

        for index in range(len(ctpath)):
            if ctpath[index]:
                items['image_urls'].append({
                    'url': base_url + ctpath[index],
                    'info': ts[index] or '',
                })

        items['content'] = data['content'].replace('&nbsp;', '')

        items['upload_path'] = self.name + '/uploads/' + items['date']

        yield items
