#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
from threading import Thread
from queue import Queue
import json


class XiaomiSpider:
    def __init__(self):
        self.url = 'http://app.mi.com/categotyAllListApi?page={}&categoryId=2&pageSize=30'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.url_queue = Queue()
        self.n = 0
        pass

    # URL 入队列
    def url_in(self):
        for i in range(67):
            url = self.url.format(i)
            #  放到队列
            self.url_queue.put(url)
        pass

    # 线程事件函数
    def get_data(self):
        while True:
            # 判断队列是否为空
            if self.url_queue.empty():
                break

            # get地址 请求+解析+保存
            url = self.url_queue.get()
            # 字符串
            html = requests.get(url=url, headers=self.headers).content.decode('utf-8')
            # json 格式
            html = json.loads(html)
            with open('xiaomi.json', 'a')as f:
                app_dict = {}
                for app in html['data']:
                    app_dict['app_name'] = app['displayName']
                    app_dict['app_link '] = 'http://app.mi.com/details?id=' + app['packageName']
                    json.dump(app_dict, f, ensure_ascii=False)
                    # print(app_name, app_link)
                    self.n += 1

    def main(self):
        # url 入队列
        self.url_in()
        # 创建多线程
        t_list = []
        for i in range(5):
            t = Thread(target=self.get_data)
            t_list.append(t)
            t.start()
        # 阻塞线程
        for i in t_list:
            i.join()

        print('应用数量:', self.n)
        pass


if __name__ == '__main__':
    start = time.time()
    spider = XiaomiSpider()
    spider.main()
    end = time.time()
    print('执行时间: %.2f' % (end-start))
