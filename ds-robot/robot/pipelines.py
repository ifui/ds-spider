# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.utils.python import to_bytes
import hashlib
from contextlib import suppress
from .settings import MONGO_HOST, MONGO_DBNAME, MONGO_PORT, MONGO_USERNAME, MONGO_PASSWORD
import pymongo


class MongoPipeline(object):
    """
    数据存储中间件
    """
    db = None
    collection = None

    def __init__(self):
        host = MONGO_HOST
        port = MONGO_PORT
        dbname = MONGO_DBNAME

        client = pymongo.MongoClient(
            host=host, port=port, username=MONGO_USERNAME, password=MONGO_PASSWORD)

        self.db = client[dbname]

    # 不同的 spider 存入不同的数据表
    def db_collection(self, spider):
        self.collection = self.db[spider.name]

    def process_item(self, item, spider):
        self.db_collection(spider=spider)
        # 去重插入
        self.collection.update_one(
            {'origin_url': item['origin_url']}, {"$set": dict(item)}, upsert=True)
        return item


class ImagespiderPipeline(ImagesPipeline):
    """
    图片资源下载中间件
    """

    # 重写下载方法
    def get_media_requests(self, item, info):
        # 下载文章内资源
        if 'image_urls' in item:
            for image_url in item['image_urls']:
                yield Request(image_url['url'])

    # 重写保存路径
    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()

        return f'{item["upload_path"]}/{image_guid}.jpg'

    # 图片下载完成操作：替换 content 图片路径
    def item_completed(self, results, item, info):
        with suppress(KeyError):
            ItemAdapter(item)[self.images_result_field] = [
                x for ok, x in results if ok]
            for res in ItemAdapter(item)[self.images_result_field]:
                ItemAdapter(item)['content'] = ItemAdapter(item)[
                    'content'].replace(res['url'], res['path'])
        return item


class ThumbspiderPipeline(ImagesPipeline):
    """
    版面图片下载中间件
    """

    # 重写下载方法
    def get_media_requests(self, item, info):
        if 'thumb_url' in item:
            yield Request(item['thumb_url'])

    # 重写保存路径
    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = item['sort']

        return f'{item["upload_path"]}/{image_guid}.jpg'

    # # 图片下载完成操作：替换 content 图片路径
    def item_completed(self, results, item, info):
        for ok, x in results:
            if ok:
                ItemAdapter(item)['thumb_url'] = x['path']

        return item


class PDFspiderPipeline(FilesPipeline):
    """ 
    PDF下载中间件
    """

    # 重写下载方法
    def get_media_requests(self, item, info):
        if 'pdf_url' in item:
            yield Request(item['pdf_url'])

    # 重写保存路径
    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = item['sort']

        return f'{item["upload_path"]}/{image_guid}.pdf'

    # 图片下载完成操作：替换 content 图片路径
    def item_completed(self, results, item, info):
        for ok, x in results:
            if ok:
                ItemAdapter(item)['pdf_url'] = x['path']

        return item
