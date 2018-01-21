from multiprocessing import Pool
import time
import os
import requests
from lxml import etree


def get_page_url():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    # index-2.html
    # 用于组装跳转详情页面url
    base_url = 'https://www.1124s.com'
    response = requests.get(url='https://www.1124s.com/Html/110/', headers=headers)
    if response.status_code == 200:
        response_text = response.content
        et = etree.HTML(response_text)
        titles = et.xpath('//div[@class="box movie_list"]/ul/li/a/h3/text()')
        page_url = et.xpath('//div[@class="box movie_list"]/ul/li/a/@href')
        img_urls = et.xpath('//div[@class="box movie_list"]/ul/li/a/img/@src')
        movie_dates = et.xpath('//div[@class="box movie_list"]/ul/li/a/span/text()')
        print(response_text)


def get_page_info():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    response = requests.get(url='https://www.1124s.com/Html/131/23932.html', headers=headers)
    if response.status_code == 200:
        response_text = response.content
        et = etree.HTML(response_text)
        downurls = et.xpath('//ul[@class="downurl"]/a/@href')
        img_urls = et.xpath('//div[@class="movie_info"]/dl/dt/img/@src')
        film_titles = et.xpath('//div[@class="movie_info"]/dl/dd[@class="film_title"]/h1/text()')
        film_type = et.xpath('//div[@class="movie_info"]/dl/dd[4]/span/text()')
        update_times = et.xpath('//div[@class="movie_info"]/dl/dd[5]/text()')
        print(downurls)

if __name__ == '__main__':
    pass