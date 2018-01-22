import json
import requests
from utils.lazystore import LazyMysql
from multiprocessing import Pool
import os
import time

# 请求手机归属地信息，并存入数据库
def getMobileInfo(mobile):
    try:
        # 构造字符串请求参数
        payload = {
            'output': 'json',
            'callback': 'querycallback',
            'timestamp': '1516188073821'
        }
        payload['m'] = mobile
        # 模拟浏览器请求头
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/59.0.3071.115 Safari/537.36'
        }
        response = requests.get(url='http://v.showji.com/Locating/showji.com2016234999234.aspx',
                                params=payload,headers=headers)
        if response.status_code == 200:
            # 响应结果字符串
            response_text = response.text
            # 结果 json 字符串
            response_json = response_text.split('(')[1].split(')')[0]
            # json反序列化字典数据
            response_dict = json.loads(response_json)
            # 构造存入数据库的数据dict
            result_dict = {}
            result_dict['mobile_num'] = response_dict.get('Mobile')
            result_dict['province'] = response_dict.get('Province')
            result_dict['city'] = response_dict.get('City')
            result_dict['post_code'] = response_dict.get('PostCode')
            result_dict['area_code'] = response_dict.get('AreaCode')
            result_dict['corp'] = response_dict.get('Corp')
            result_dict['mobile_area'] = response_dict.get('Province') + response_dict.get('City')
            # 数据库信息
            db_config = {
                'host': '127.0.0.1',
                'user': 'root',
                'password': 'root',
                'db': 'db_test'
            }
            # 初始化数据库操作
            lazyStore = LazyMysql(db_config)
            # 入库一条数据
            result_save = lazyStore.save_one_data(result_dict, 'mobile')
            if result_save == 1:
                print(mobile + '数据入库成功！')
            else:
                print(mobile + '数据入库失败！')
    except Exception as e:
        print(e)
        getMobileInfo(mobile)

def requestAllSections(phoneSections):
    # last用于接上次异常退出前的号码
    last = 0
    # 自动生成手机号码，后四位补0
    start = time.time()
    for head in phoneSections:
        for i in range(0, 10000):
            # 线程休眠3s
            time.sleep(3)
            middle = str(i).zfill(4)
            phoneNum = head + middle
            getMobileInfo(phoneNum)
        last = 0
    end = time.time()
    print('数据抓取完成！耗时 {}s'.format(end-start))

if __name__ == '__main__':
    #要抓取的手机号段
    # yys = ['185','145']
    yys = ['176']
    # 开启进程池
    pool = Pool(processes=8)
    # 多进程调用
    pool.apply_async(requestAllSections, args=(yys,))
    pool.close()
    pool.join()
    # requestAllSections(yys)