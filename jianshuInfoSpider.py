import requests
from lxml import etree
from bs4 import BeautifulSoup

targetUrl = 'https://www.jianshu.com/u/383970bef0a0'
response = requests.get(url=targetUrl)
html = response.text
et = etree.HTML(html)
titles = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/a[@class="title"]/text()')
print(titles)

links = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/a[@class="title"]/@href')
print(links)

nickname = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/div[@class="author"]'
                    '/div[@class="info"]/a[@class="nickname"]/text()')

print(nickname)

report_time = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/div[@class="author"]'
                       '/div[@class="info"]/span[@class="time"]/text()')
print(report_time)