# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy import Selector
from urllib import urlencode
from zhihu.items import ZhihuItem
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class ZhihuSpiderSpider(scrapy.Spider):
    name = "zhihu_spider"
    allowed_domains = ["www.zhihu.com"]

    def start_requests(self): 
    	return[
    		FormRequest(
    			"http://www.zhihu.com/login/phone_num",
    			formdata={"phone_num":"18602701595","password":"cp89112587"},
    			callback=self.afterlogin)
    		]    	

    def afterlogin(self, response):
        print 'after login'
        requests = []
        yield Request(url='https://www.zhihu.com',callback=self.parse)

    def parse(self,response):
		item =	ZhihuItem()
		self.xsrf = response.xpath('.//input[@name="_xsrf"]/@value').extract()[0]
		self.i = 0
		pages = response.xpath('.//div[@class="feed-content"]')
		for page in pages:
			item['title'] = page.xpath('.//h2[@class="feed-title"]/a/text()').extract()
			item['content'] = page.xpath('.//div[@class="zh-summary summary clearfix"]/text()').extract()
		for j in range(50):
			yield self.next10()
			time.sleep(0.5)
    def next10(self):
		print 'next10'
		post_data =  {"params":{"offset":10+self.i*10,"start":str(9+self.i*10)},"method":"next"}
		headers ={
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Connection':'keep-alive',
			'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
			'Origin':'https://www.zhihu.com',
			'Referer':'https://www.zhihu.com/',
			'X-Requested-With':'XMLHttpRequest',
			'X-Xsrftoken':self.xsrf}
		self.i +=1						 
		return	Request(url = "https://www.zhihu.com/node/TopStory2FeedList",
						method = 'POST',
						headers = headers,
						# formdata = {"params":{"offset":10,"start":"9"},"method":"next"},
						body = urlencode(post_data).replace('%27','%22').replace('+',''),
						callback = self.parse_json)
			  	
    def parse_json(self,response):
		print 'got here'
		contents = json.loads(response.body)['msg']
		for content in contents:
			next_content = Selector(text = content,type = 'html')
			yield self.parse_next(next_content)

    def parse_next(self,next_content):
		pages = next_content.xpath('.//div[@class="feed-content"]')
		item =	ZhihuItem()
		for page in pages:
			item['title'] = page.xpath('.//h2[@class="feed-title"]/a/text()').extract()
			item['content'] = page.xpath('.//div[@class="zh-summary summary clearfix"]/text()').extract()
		return item
