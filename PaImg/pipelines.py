# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

# get_media_requests(item, info)
# 在工作流程中可以看到，管道会得到图片的URL并从项目中下载。
# 为了这么做，你需要重写 get_media_requests() 方法，并对各个图片URL返回一个Request:
#
# def get_media_requests(self, item, info):
#     for image_url in item['image_urls']:
#         yield scrapy.Request(image_url)
# 这些请求将被管道处理，当它们完成下载后，结果将以2-元素的元组列表形式传送到 item_completed()
#
#
# item_completed() 方法
# success 是一个布尔值，当图片成功下载时为 True ，因为某个原因下载失败为``False``
# image_info_or_error 是一个包含下列关键字的字典（如果成功为 True ）或者出问题时为 Twisted Failure 。
# url - 图片下载的url。这是从 get_media_requests() 方法返回请求的url。
# path - 图片存储的路径（类似 IMAGES_STORE）
# checksum - 图片内容的 MD5 hash

# item_completed(results, items, info)
# 当一个单独项目中的所有图片请求完成时（要么完成下载，要么因为某种原因下载失败）， ImagesPipeline.item_completed() 方法将被调用。
#
# item_completed() 方法需要返回一个输出，其将被送到随后的项目管道阶段，因此你需要返回（或者丢弃）项目，如你在任意管道里所做的一样。
# 这里是一个 item_completed() 方法的例子，其中我们将下载的图片路径（传入到results中）存储到 image_paths 项目组中，如果其中没有图片，我们将丢弃项目:
#

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    "Referer": "https://www.meizitu.com/",  # 加入referer 为下载的域名网站
}


class PaimgPipeline(ImagesPipeline):
    # 在工作流程中可以看到，管道会得到图片的URL并从项目中下载。
    # # 为了这么做，你需要重写 get_media_requests() 方法，并对各个图片URL返回一个Request:
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            # 这里把item传过去，因为后面需要用item里面的name作为文件名
            yield Request(image_url, meta={'item': item}, headers=headers)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = request.url.split('/')[-1]  # 倒数第一个元素
        filenames = "full/%s/%s" % (item['name'], image_guid)
        # print(filename)
        return filenames

    def thumb_path(self, request, thumb_id, response=None, info=None):
        item = request.meta['item']
        image_guid = request.url.split('/')[-1]  # 倒数第一个元素
        # thumb_id就是setting文件中定义的big small
        filenames = "thumbil/%s/%s/%s" % (thumb_id, item['name'], image_guid)
        return filenames
