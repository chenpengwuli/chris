# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #解决中文字符的问题
import pycurl
import StringIO
import urllib
from lxml.etree import HTML
from lxml import etree
phone_num = 'xxx' 
password = 'xxx'
url = 'http://www.zhihu.com/login/phone_num' #这个地址是zhihu手机号登录的post地址
data = {'phone_num':phone_num,'password':password} #这个是Post的form信息
after_login = 'http://www.zhihu.com/#signin' #登录后再次打开首页可获得信息
def login_zhihu(data,url):
	c = pycurl.Curl()
	str1 = StringIO.StringIO()
	c.setopt(pycurl.URL,url)
	c.setopt(c.WRITEFUNCTION,str1.write)
	# c.setopt(pycurl.VERBOSE,1)
	c.setopt(pycurl.POSTFIELDS,urllib.urlencode(data)) #Pycurl的post方法
	c.setopt(pycurl.FOLLOWLOCATION,1)
	c.setopt(pycurl.MAXREDIRS,5)
	c.setopt(pycurl.COOKIEFILE,'') #使用cookie?
	c.perform() 
	print str1.getvalue() #这里打印登录后的response，为一个Json，成功则为0

	c.setopt(pycurl.URL,after_login) #打开首面
	c.setopt(pycurl.HTTPGET,1) #使用get方法
	c.setopt(c.WRITEFUNCTION,str1.write) 
	c.perform()
	html = HTML(str1.getvalue()) #使用HTML将文本转为html类型
	pages = html.xpath('.//div[@class="feed-content"]') #对于title:content类型的结构，先取到它的Parent div部分，再依取得各文本
	for page in pages:
		page = HTML(etree.tostring(page))
		title = page.xpath('.//h2[@class="feed-title"]/a/text()')
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
