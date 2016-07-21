# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pycurl
import StringIO
import urllib
from lxml.etree import HTML
from lxml import etree
phone_num = 'xxx'
password = 'xxx'
url = 'http://www.zhihu.com/login/phone_num'
data = {'phone_num':phone_num,'password':password}
after_login = 'http://www.zhihu.com/#signin'
def login_zhihu(data,url):
	c = pycurl.Curl()
	str1 = StringIO.StringIO()
	c.setopt(pycurl.URL,url)
	c.setopt(c.WRITEFUNCTION,str1.write)
	# c.setopt(pycurl.VERBOSE,1)
	c.setopt(pycurl.POSTFIELDS,urllib.urlencode(data))
	c.setopt(pycurl.FOLLOWLOCATION,1)
	c.setopt(pycurl.MAXREDIRS,5)
	c.setopt(pycurl.COOKIEFILE,'')
	c.perform()
	print str1.getvalue()

	c.setopt(pycurl.URL,after_login)
	c.setopt(pycurl.HTTPGET,1)
	c.setopt(c.WRITEFUNCTION,str1.write)
	c.perform()
	html = HTML(str1.getvalue())
	pages = html.xpath('.//div[@class="feed-content"]')
	for page in pages:
		page = HTML(etree.tostring(page))
		title = page.xpath('.//a[@class="question_link"]/text()')
		content = page.xpath('.//div[@class="zh-summary summary clearfix"]/text()')

		if title:
			for tit in title:
				print tit.strip()
		# print len(tit)
		if content:
			for con in content:
				print con.strip()
		# print len(content)
		# print etree.tostring(page)
		# contents = dict(zip(titles,pages))
	# for page in pages:
	# 	print page.strip()
	# for title in titles:
	# 	print title
	# for (key,value) in content.items():
	# 	print '[',key,':',value,']'
	c.close()

if __name__=='__main__':
	login_zhihu(data,url)
