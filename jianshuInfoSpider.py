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
            result_list = analysis_data(base_url, html)
            save_data(result_list)
    except Exception as e:
        print(e)


def analysis_data(base_url, html):
    '''
    解析网页数据 返回数据字典列表
    :param base_url: 基础url 用于拼接文章链接
    :param html: 网页html
    :return: 数据字典列表
    '''
    et = etree.HTML(html)
    # 标题
    titles = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/a[@class="title"]/text()')
    # 文章链接
    links = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/a[@class="title"]/@href')
    # 作者
    nicknames = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/div[@class="author"]'
                         '/div[@class="info"]/a[@class="nickname"]/text()')
    # 看的次数
    lookeds = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/div[@class="meta"]/a[1]/text()')
    # 评论数
    comments = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/div[@class="meta"]/a[2]/text()')
    # 喜欢数
    likes = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/div[@class="meta"]/span/text()')
    # 发布时间
    # report_times = et.xpath('//ul[@class="note-list"]/li/div[@class="content"]/div[@class="author"]'
    #                         '/div[@class="info"]/span[@class="time"]/text()')
    result_list = []
    for i in range(0, len(titles)):
        result_dict = {
            'title': '',
            'link': '',
            'nickname': '',
            'looked': '',
            'comment': '',
            'like': ''
        }
        result_dict['title'] = titles[i]
        result_dict['link'] = base_url + links[i]
        result_dict['nickname'] = nicknames[i]
        result_dict['looked'] = lookeds[i]
        result_dict['comment'] = comments[i]
        result_dict['like'] = likes[i]
        # result_dict['report_time'] = report_times[i]
        result_list.append(result_dict)
    return result_list


def save_data(result_list):
    '''
    保存数据
    :param result_list: 每页数据的字典列表
    :return:
    '''
    # 数据库信息
    db_config = {
        'host': 'xx.xx.xx.xx',
        'user': 'root',
        'password': 'xxxxxx',
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