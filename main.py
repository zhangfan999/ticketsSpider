# -*- coding:utf-8 -*-
import requests
import threading
from queue import Queue
import re
import time
from proxy_helper import Proxy_helper
from bs4 import BeautifulSoup
import pymysql
import os
import sys
import pyttsx3

class Spider(threading.Thread):
    #def __init__(self, threadName, url_queue, validip_que):
    def __init__(self, threadName,validip_que,stationItem):
        threading.Thread.__init__(self)
        self.validip_que = validip_que
        self.requestUrl=stationItem[1]
        self.stationName=stationItem[0]
        self.starttime = time.time()
        self.endtime = time.time()
        self.daemon = True
        self.count = 0
        # self.url_queue = url_queue
        #self.mysqlClient = pymysql.connect("localhost", "root", "k6i7986t", "spider", use_unicode=True)
        self.userAgents = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11"
        ]
        self.productPageRequestCount=0

    def run(self):
        print("%s开始启动" % (self.name))
        while True:
            #url = self.url_queue.get()
            with open('headers2.txt', 'r') as f:
                headerStr = f.read()
                headersArr = headerStr.split('\n')
            headers = {}
            for headerItem in headersArr:
                headersItemName = headerItem.split(': ')[0]
                headerItemValue = headerItem.split(': ')[1] if headersItemName !='User-Agent' else "%s" % (self.userAgents[self.count % 17])
                headers[headersItemName] = headerItemValue
            self.count += 1
            self.refreshPage(headers)
            time.sleep(1)

    def refreshPage(self,headers):
        validip = self.validip_que.get()
        proxy = {'http': validip}
        try:
            response = requests.get(self.requestUrl, proxies=proxy, headers=headers, timeout=6)
            if response.status_code == 200:
                self.validip_que.put(validip)
                response.encoding = "utf-8"
                a=response.text.count("有",0,len(response.text))
                print(response.text)
                if a>0:
                    # engine = pyttsx3.init()
                    # engine.say("发现%d张%s的车票"%(a,self.stationName))
                    # engine.runAndWait()
                    print("发现%s"%(self.stationName))
                    os.system("demo.mp3")
                else:
                    print("%s暂无车票可购买，%s正在进行第%d次重新购买"%(self.stationName,self.stationName,self.count))
            else:
                print("请求错误")
        except BaseException as e:
            print(e)
            self.validip_que.get(validip)
        time.sleep(1)

    def getListHtml(self,url,headers,repeat_count=0):
        validip = self.validip_que.get()
        proxy = {'http': validip}
        try:
            response = requests.get(url, proxies=proxy, headers=headers, timeout=5)
            if response.status_code == 200:
                self.validip_que.put(validip)
                response.encoding = "euc-kr"
                soup = BeautifulSoup(response.text, "lxml")
                a_list = list(set(soup.select("td b a")))
                for a in a_list:
                    arc_url = "http://cellbank.snu.ac.kr/" + a.get("href")
                    self.getArticleHtml(arc_url,url)
            else:
                repeat_count += 1
                if repeat_count < 4:
                    print("%s列表页下载失败，正在进行第%d次重新下载!" % (url, repeat_count))
                    self.getListHtml(url,headers,repeat_count)
                else:
                    print("%s列表页下载失败" % (url))
                    self.sqlInsertFailedListUrl(url)
        except BaseException as e:
            print("代理IP连接超时")
            self.validip_que.get(validip)

def main():
    # 开启多线程采集代理IP，并放置于代理IP的队列ipproxy_que里
    ip_que = Queue(1200)
    validip_que = Queue(900000)
    ipCheckoutThreadMount = 5
    ipCollectThreadMount = 2
    dataCollectThreadMount = 1
    proxy_helper = Proxy_helper(ip_que, validip_que, ipCheckoutThreadMount, ipCollectThreadMount)
    proxy_helper.run()
    time.sleep(4)
    item_list = [
    ["麻城到合肥","https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-10&leftTicketDTO.from_station=MCN&leftTicketDTO.to_station=HFH&purpose_codes=ADULT"],
    ["麻城到杭州","https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-10&leftTicketDTO.from_station=MCN&leftTicketDTO.to_station=HZH&purpose_codes=ADULT"],
    ["麻城到南京","https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-10&leftTicketDTO.from_station=MCN&leftTicketDTO.to_station=NJH&purpose_codes=ADULT"]
    ]
    # url_que = Queue(2)
    # for arc_url in url_list:
    #     url_que.put(arc_url)
    for i in range(len(item_list)):
        worker = Spider("数据采集线程%d" % (i),validip_que,item_list[i])
        worker.start()
        print("数据采集线程%d开启" % (i))

    validip_que.join()


if __name__ == "__main__":
    main()
