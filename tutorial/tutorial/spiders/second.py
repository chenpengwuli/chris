# -*- coding: utf-8 -*-
import scrapy


class SecondSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["domz.org"]
    start_urls = [
            'http://www.dmoz.org/Computers/Programming/Languages/Python/Books/',
            'http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/'
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
