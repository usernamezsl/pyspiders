import requests
from utils.lazystore import LazyMysql
from lxml import etree
from multiprocessing import Pool
import time

def getJianshuInfo(user_id,page):
    '''
    抓取指定用户一页的文章数据，并存入数据库
    :param user_id: 用户id 网页中获取
    :param page: 当前抓取的页码
    :return:
    '''
    base_url = 'https://www.jianshu.com'
    target_url = 'https://www.jianshu.com/u/' + user_id
    # 模拟浏览器请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/59.0.3071.115 Safari/537.36'
    }
    # 构造查询字符串
    payload = {
        'order_by':'shared_at',
        'page':''
    }
    payload['page'] = page
    try:
        response = requests.get(url=target_url, headers=headers,params=payload)
        if response.status_code == 200:
            html = response.text
            et = etree.HTML(html)
            titles = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/a[@class="title"]/text()')
            links = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/a[@class="title"]/@href')
            nicknames = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/div[@class="author"]'
                                '/div[@class="info"]/a[@class="nickname"]/text()')
            # report_time = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/div[@class="author"]'
            #                        '/div[@class="info"]/span[@class="time"]/text()')
            # print(report_time)
            result_list = []
            for i in range(0,len(titles)):
                result_dict = {}
                result_dict['title'] = titles[i]
                result_dict['link'] = base_url + links[i]
                result_dict['nickname'] = nicknames[i]
                result_list.append(result_dict)
            save_data(result_list)
    except Exception as e:
        print(e)

def save_data(result_list):
    '''
    保存数据
    :param result_list: 每页数据的字典列表
    :return:
    '''
    # 数据库信息
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'db': 'db_test'
    }
    # 初始化数据库操作
    lazyStore = LazyMysql(db_config)
    for result in result_list:
        result_save = lazyStore.save_one_data(result, 'jianshu_info')
        if result_save == 1:
            print('一条数据入库成功！')



def main(user_id,page_num):
    '''
    封装抓取指定用户，指定页数数量的文章数据
    :param user_id: 用户id,网页中获取
    :param page_num: 要抓取的页数
    :return:
    '''
    # 开启进程池
    pool = Pool(processes=8)
    # 开始时间
    start = time.time()
    for page in range(0, page_num):
        print('开始抓取第{}页数据'.format(page))
        # 多进程调用
        pool.apply_async(getJianshuInfo, args=(user_id, page))
        # getJianshuInfo(user_id=user_id,page=page)
    pool.close()
    pool.join()
    print('数据抓取完成！！耗时{}s'.format(time.time() - start))


if __name__ == '__main__':
    # https://www.jianshu.com/u/383970bef0a0?order_by=shared_at&page=0
    user_id = '383970bef0a0'
    page_num = 15
    main(user_id=user_id,page_num=page_num)