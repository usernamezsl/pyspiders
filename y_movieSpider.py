from multiprocessing import Pool
import time
import os
import requests
from lxml import etree
from utils.lazystore import LazyMysql

def get_page_url(url):
    '''
    抓取每个影片入口url 以及影片信息
    :return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            response_text = response.content
            page_url_list = analysis_page_url(response_text)
            result_list = []
            for page_url_dict in page_url_list:
                page_url = page_url_dict['page_url']
                movie_title = page_url_dict['title']
                movie_info_dict = get_page_info(page_url=page_url)
                result_list.append(movie_info_dict)
                pass
            save_data(result_list)
    except Exception as e:
        print(e)
        pass


def analysis_page_url(response_text):
    '''
    解析每页影片入口url
    :param response_text:
    :return:
    '''
    # 用于组装跳转详情页面url
    base_url = 'https://www.1124s.com'
    et = etree.HTML(response_text)
    titles = et.xpath('//div[@class="box movie_list"]/ul/li/a/h3/text()')
    page_urls = et.xpath('//div[@class="box movie_list"]/ul/li/a/@href')
    img_urls = et.xpath('//div[@class="box movie_list"]/ul/li/a/img/@src')
    movie_dates = et.xpath('//div[@class="box movie_list"]/ul/li/a/span/text()')
    page_url_list = []
    for i in range(0, len(titles)):
        page_url_dict = {
            'title': '',
            'page_url': '',
            'img_url': '',
            'movie_date': ''
        }
        page_url_dict['title'] = titles[i]
        page_url_dict['page_url'] = base_url + page_urls[i]
        page_url_dict['img_url'] = img_urls[i]
        page_url_dict['movie_date'] = movie_dates[i]
        page_url_list.append(page_url_dict)
        pass
    return page_url_list


def get_page_info(page_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    try:
        response = requests.get(url=page_url, headers=headers)
        if response.status_code == 200:
            response_text = response.content
            movie_info_dict = analysis_movie_info(response_text)
            return movie_info_dict
    except Exception as e:
        print(e)
        pass


def analysis_movie_info(response_text):
    '''
    解析影片详情数据
    :param response_text: 页面数据
    :return:
    '''
    et = etree.HTML(response_text)
    downurls = et.xpath('//ul[@class="downurl"]/a/@href')
    img_urls = et.xpath('//div[@class="movie_info"]/dl/dt/img/@src')
    film_titles = et.xpath('//div[@class="movie_info"]/dl/dd[@class="film_title"]/h1/text()')
    film_types = et.xpath('//div[@class="movie_info"]/dl/dd[4]/span/text()')
    update_times = et.xpath('//div[@class="movie_info"]/dl/dd[5]/text()')
    movie_info_dict = {
        'movie_title':'',
        'downurl':'',
        'img_url':'',
        'film_type':'',
        'update_time':''
    }
    movie_info_dict['movie_title'] = film_titles[0]
    movie_info_dict['downurl'] = downurls[0]
    movie_info_dict['img_url'] = img_urls[0]
    movie_info_dict['film_type'] = film_types[0]
    movie_info_dict['update_time'] = update_times[0].split('：')[1].strip()
    return movie_info_dict

def save_data(result_list):
    '''
    保存数据
    :param result_list: 每页数据的字典列表
    :return:
    '''
    db_config = {
        'host': 'xx.xx.xx.xx',
        'user': 'root',
        'password': '123456',
        'db': 'db_test'
    }
    # 初始化数据库操作
    lazyStore = LazyMysql(db_config)
    lazyStore.save_data_list(result_list,'movie_info')

def main(start_page,end_page):
    start = time.time()
    base_url = 'https://www.1124s.com/Html/110/'
    for page in range(start_page,end_page):
        if page == 1:
            print('===============开始抓取第{}页数据==============='.format(page))
            get_page_url(url=base_url)
            print('===============华丽分割===============')
        else:
            url = base_url + 'index-' + str(page) + '.html'
            print('===============开始抓取第{}页数据==============='.format(page))
            get_page_url(url=url)
            print('===============华丽分割===============')
            pass
    print('===============end===============')
    print('数据抓取完成，耗时{}s'.format(time.time() - start))
    pass
if __name__ == '__main__':
    main(start_page=4,end_page=215)
    pass