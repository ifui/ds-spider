# -*- coding: utf-8 -*-
from scrapy import cmdline

cmdline.execute(
    'scrapy crawl jjjcb -a start_time=20220218 -a end_time=20220218'.split())
# cmdline.execute(
#     'scrapy crawl 81cn -a startTime=20220111 -a endTime=20220112'.split())
