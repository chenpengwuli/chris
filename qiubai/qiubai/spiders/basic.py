# -*- coding: utf-8 -*-
import scrapy
from qiubai.items import QiuBaiItem
class QiuBaiSpider(scrapy.Spider):
    name = "qiubai"
    start_urls = (
        'http://www.qiushibaike.com/',
    )

    def parse(self, response):
        item = QiuBaiItem()
        item['content'] = response.xpath('//div[@class="content"]/text()').extract()
        yield item
