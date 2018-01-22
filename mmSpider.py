import requests
from lxml import etree
import time
from multiprocessing import Pool
from utils.lazystore import LazyMysql


def get_page_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    try:
        response = requests.get(url=url)
        response.encoding == 'utf-8'
        if response.status_code == 200:
            response_text = response.content
            result_list = analysis_data(response_text)
            save_data(result_list)
    except Exception as e:
        print(e)


def save_data(result_list):
    '''
    保存数据
    :param result_list: 每页数据的字典列表
    :return: 
    '''
    db_config = {
        'host': 'xx.xxx.xxx.xxx',
        'user': 'root',
        'password': '123456',
        'db': 'db_test'
    }
    # 初始化数据库操作
    lazyStore = LazyMysql(db_config)
    lazyStore.save_data_list(result_list,'mm_image')


def analysis_data(response_text):
    '''
    解析每一页网页数据
    :param response_text: http响应的网页数据
    :return: 每页的数据字典列表
    '''
    et = etree.HTML(response_text)
    titles = et.xpath('//div[@class="pic"]/ul/li/a/img/@alt')
    urls = et.xpath('//div[@class="pic"]/ul/li/a/img/@src')
    report_times = et.xpath('//div[@class="pic"]/ul/li/span[2]/text()')
    lookeds = et.xpath('//div[@class="pic"]/ul/li/span[3]/text()')
    result_list = []
    for i in range(0, len(titles)):
        result_dict = {
            'title': '',
            'url': '',
            'report_time': '',
            'looked': ''
        }
        result_dict['title'] = titles[i]
        result_dict['url'] = urls[i]
        result_dict['report_time'] = report_times[i]
        result_dict['looked'] = lookeds[i]
        result_list.append(result_dict)
    return result_list


def main(start_page,end_page):
    '''
    爬虫程序最终运行入口
    :param start_page: 开始爬取页码
    :param end_page: 结束页码
    :return: 
    '''
    start = time.time()
    base_url = 'http://www.mmjpg.com'
    for page in range(start_page,end_page + 1):
        if start_page == 1:
            print('==开始抓取第{}页数据=='.format(page))
            get_page_info(url=base_url)
            print('===============华丽分割===============')
        else:
            url = base_url + '/home/' + str(page)
            print('==开始抓取第{}页数据=='.format(page))
            get_page_info(url=url)
            print('===============华丽分割===============')
            pass
        pass
    print('===============end===============')
    print('数据抓取完成，耗时{}s'.format(time.time() - start))
    pass


if __name__ == '__main__':
    pool = Pool(processes=8)
    pool.apply_async(main,args=(1,83))
    pool.close()
    pool.join()
    # main(1,83)




