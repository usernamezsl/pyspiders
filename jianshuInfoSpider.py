import requests
from utils.lazystore import LazyMysql
from lxml import etree


def getJianshuInfo(url):
    # targetUrl = 'https://www.jianshu.com/u/383970bef0a0'
    base_url = 'https://www.jianshu.com'
    # 模拟浏览器请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/59.0.3071.115 Safari/537.36'
    }
    try:
        response = requests.get(url=url, headers=headers)
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
            for i in range(0,9):
                result_dict = {}
                result_dict['title'] = titles[i]
                result_dict['link'] = base_url + links[i]
                result_dict['nickname'] = nicknames[i]
                result_list.append(result_dict)
            save_data(result_list)
    except Exception as e:
        print(e)


def save_data(result_list):
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
    print('数据抓取完成！')


if __name__ == '__main__':
    base_url = 'https://www.jianshu.com/u/'
    getJianshuInfo(base_url + '383970bef0a0')