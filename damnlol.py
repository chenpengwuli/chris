# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import time
from damnlol2.items import Damnlol2Item
class DamnlolSpider(scrapy.Spider):
    count = 0
    name = "damnlol"
    allowed_domains = ["damnlol.com"]
    start_urls = [
                'http://www.damnlol.com/', 
                ]
    def parse(self, response):
        item =  Damnlol2Item()
        self.count = self.count + 1
        url_link = response.xpath('//div[starts-with(@class,"right navigation")]/a/@href')[1].extract()
        item['link'] = response.xpath('//*[@id="post-image"]/@src')[0].extract()
        item['title'] = response.xpath('//*[@id="post-title"]/text()')[0].extract()
        item['image_urls'] = [item['link'],] # here the [,] is very important that the image_urls have to be lists.
        print item['title'],item['link'] 
        if self.count < 100:
            yield Request(url = url_link, dont_filter=True)

        yield item
        ‘’‘ 这里需要注意的是 item link必须得是list形式
            但是item title 必须是string形式
        ’‘’
        # print response.xpath('//div[starts-with(@class,"right navigation")]/a/@href')
# '//div[starts-with(@class,"right navigation")/a[@class="nav right previous"]/]'

# '//div[starts-with(@class,"right navigation")/a and (@class="nav right previous")]'
