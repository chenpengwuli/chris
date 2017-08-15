# -*- coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import requests
import time
import csv
from lxml import etree

headers ={'User-agent':'Mozilla/5.0'}

def get_page(url):
	r = requests.get(url,headers = headers)
	r.encoding = r.apparent_encoding
	html = etree.HTML(r.text)
	ip = html.xpath('//table[@id="ip_list"]//tr[@class="odd"]//td[2]/text()')
	port = html.xpath('//table[@id="ip_list"]//tr[@class="odd"]//td[3]/text()')
	port_type = html.xpath('//table[@id="ip_list"]//tr[@class="odd"]//td[6]/text()')
	data = []
	for i,j,k in zip(ip,port,port_type):
		data.append({'ip':i,'port':j,'port_type':k})
	f_csv.writeheader()
	f_csv.writerows(data)
	# print data
	# f_csv.writerows(data)
	# print etree.tostring(ip[0])
	# print port

host ="http://www.xicidaili.com/nn/"
csv_headers =['ip','port','port_type']

with open(r'C:\Users\Kevin\Desktop\xici.csv','wb') as f:
	f_csv = csv.DictWriter(f,csv_headers)
	# f_csv.writerow(csv_headers)
	for i in range(1,3,1):
		get_page(host + str(i))

		time.sleep(0.3)

# indent is 4
