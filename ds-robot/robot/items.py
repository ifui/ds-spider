# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RobotItem(scrapy.Item):
    pre_title = scrapy.Field()  # 肩标题
    title = scrapy.Field()  # 标题
    sub_title = scrapy.Field()  # 副标题
    author = scrapy.Field()  # 作者信息
    content = scrapy.Field()  # 内容
    date = scrapy.Field()  # 日期
    origin_url = scrapy.Field()  # 来源网址
    section = scrapy.Field()  # 版面
    section_image = scrapy.Field()  # 版面图片
    copyfrom = scrapy.Field()  # 来源
    coords = scrapy.Field()  # 锚点
    image_urls = scrapy.Field()  # 图片链接
    images = scrapy.Field()  # 图片信息
    upload_path = scrapy.Field()  # 资源保存路径


class SectionItem(scrapy.Item):
    copyfrom = scrapy.Field()  # 来源
    name = scrapy.Field()  # 版名
    date = scrapy.Field()  # 日期
    sort = scrapy.Field()  # 排序
    thumb_url = scrapy.Field()  # 版面图片
    pdf_url = scrapy.Field()  # PDF路径
    images = scrapy.Field()  # 图片信息
    origin_url = scrapy.Field()  # 来源网址
    upload_path = scrapy.Field()  # 资源保存路径
