import scrapy


class JjjcbSectionSpider(scrapy.Spider):
    name = 'jjjcb_section'
    allowed_domains = ['robot']
    start_urls = ['http://robot/']

    def parse(self, response):
        pass
