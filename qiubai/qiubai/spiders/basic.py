# -*- coding: utf-8 -*-
import scrapy
from qiubai.items import QiuBaiItem
import time
class QiuBaiSpider(scrapy.Spider):
    name = "qiubai"
    start_urls = (
        'http://www.qiushibaike.com/',
    )

    def parse(self, response):
        item = QiuBaiItem()
        item['content'] = response.xpath('//div[@class="content"]/text()').extract()
        url = 'http://www.qiushibaike.com' + response.xpath('//span[@class="next"]/parent::*/@href').extract_first()
        time.sleep(1)
        yield item
        yield scrapy.Request(url,callback=self.parse)
