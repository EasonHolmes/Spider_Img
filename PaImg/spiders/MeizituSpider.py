# coding:utf-8
import scrapy
from scrapy.spiders import CrawlSpider
from PaImg.items import PaimgItem


class MeizituSpider(CrawlSpider):
    name = "meizitu"
    host = 'http://www.meizitu.com/'
    start_urls = ['http://www.meizitu.com/a/sexy.html']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    }

    def parse(self, response):
        nextPage = response.xpath(u'//div[@id="wp_page_numbers"]//a[text()="下一页"]/@href').extract_first()
        nextPage = self.host + nextPage

        for p in response.xpath('//li[@class="wp-item"]//a/@href').extract():
            # scrapy.Request再次请求获取详情html由parse_item解析
            yield scrapy.Request(p, callback=self.parse_item)

        yield scrapy.Request(nextPage, callback=self.parse)

    def parse_item(self, response):
        item = PaimgItem()
        # 详情中的图片列表
        item['image_urls'] = response.xpath("//div[@id='picture']//img/@src").extract()
        item['name'] = response.xpath("//div[@id='picture']//img/@alt").extract()[0].split(u'，')[0]
        return item
