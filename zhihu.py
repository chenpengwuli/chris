# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pycurl
import StringIO
import urllib
from lxml.etree import HTML
from lxml import etree
import json
class zhihu(object):
	c = None
	def __init__(self):
		self.c = pycurl.Curl()
		self.login_url ='http://www.zhihu.com/login/phone_num'
		self.after_login_url ='http://www.zhihu.com/#signin'
		self.feedlist_url = 'https://www.zhihu.com/node/TopStory2FeedList'
		self.phone_num = 'xx'
		self.password = 'xx'
		self.data = {'phone_num':self.phone_num,'password':self.password}
		
	def login(self): #login the zhihu 
		buff = StringIO.StringIO()
		self.c.setopt(pycurl.URL,self.login_url)
		self.c.setopt(pycurl.FOLLOWLOCATION,1)		
		self.c.setopt(pycurl.MAXREDIRS,5)
		self.c.setopt(pycurl.COOKIEFILE,'temp')
		# self.c.setopt(pycurl.VERBOSE,1)
		self.c.setopt(pycurl.POSTFIELDS,urllib.urlencode(self.data))
		self.c.setopt(self.c.WRITEFUNCTION,buff.write)
		self.c.perform()
		print buff.getvalue()
		# print self.data
	def homepage(self): # after login,retrieve the homepage contents of zhihu
		buff = StringIO.StringIO()
		self.c.setopt(pycurl.URL,self.after_login_url)
		self.c.setopt(pycurl.FOLLOWLOCATION,1)			
		self.c.setopt(pycurl.MAXREDIRS,5)	
		self.c.setopt(pycurl.COOKIEFILE,'temp')
		self.c.setopt(pycurl.HTTPGET,1)
		self.c.setopt(self.c.WRITEFUNCTION,buff.write)
		self.c.perform()
		self.parse_xsrftoken(buff.getvalue())
		self.parse_content(buff.getvalue()) #call the function parse_content to parse the zhihu contents
		# print 'here2'
	def parse_xsrftoken(self,contents):
		html=HTML(contents)
		self.xsrftoken = html.xpath('.//input[@name="_xsrf"]/@value')[0]
	def nextcontents(self,page='2'): # then retrieve the next 10 contents of zhihu
		buff = StringIO.StringIO()
		params = {"offset":10,"start":'9'}
		method = "next"
		data_feed ={'params':params,'method':method}
		header =['Accept:*/*',
				'Accept-Language:zh-CN,zh;q=0.8',
				'Connection:keep-alive',
				'Content-Type:application/x-www-form-urlencoded; charset=UTF-8',
				'Origin:https://www.zhihu.com',
				'Referer:https://www.zhihu.com/',
				'X-Requested-With:XMLHttpRequest',
				'X-Xsrftoken:'+self.xsrftoken]
		self.c.setopt(pycurl.URL,self.feedlist_url)		
		self.c.setopt(pycurl.FOLLOWLOCATION,1)		
		self.c.setopt(pycurl.MAXREDIRS,5)
		self.c.setopt(pycurl.HTTPHEADER,header)
		self.c.setopt(pycurl.POSTFIELDS,urllib.urlencode(data_feed).replace('%27','%22').replace('+',''))
		self.c.setopt(self.c.WRITEFUNCTION,buff.write)
		self.c.perform()
		contents = json.loads(buff.getvalue())['msg']
		for content in contents:
			self.parse_content(content)
		
	def save_to_file(self,filename):# save the retrieved contents and save them to file
		pass

	def parse_content(self,contents):
		html=HTML(contents)
	# print xsrftoken
		pages = html.xpath('.//div[@class="feed-content"]')
		for page in pages:
			page = HTML(etree.tostring(page))
			title = page.xpath('.//h2[@class="feed-title"]/a/text()')
			content = page.xpath('.//div[@class="zh-summary summary clearfix"]/text()')

			if title:
				for tit in title:
					print tit.strip()

			if content:
				for con in content:
					print con.strip()
	def run(self):
		self.login()
		self.homepage()
		self.nextcontents()
		self.c.close()

if __name__=='__main__':
	zhspider = zhihu()
	zhspider.run()
