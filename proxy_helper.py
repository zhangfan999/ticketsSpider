# -*- coding:utf-8 -*-
from urllib import request
import requests
import time
import re
from queue import Queue
import threading

class Proxy_helper():
    def __init__(self, ip_que, validip_que,checkoutThreadMount,collectThreadMount):
        self.ip_que = ip_que
        self.validip_que = validip_que
        self.checkoutThreadMount=checkoutThreadMount
        self.collectThreadMount=collectThreadMount


    def run(self):
        self.collectUrl_start()
        time.sleep(1)
        self.checkout_start()

    def collectUrl_start(self):
        for i in range(self.collectThreadMount):
            worker = threading.Thread(target=self.collectUrl, args=(self.ip_que,), name="采集IP线程%d" % (i))
            worker.start()
            print("采集IP线程开启%d" % (i))

    def checkout_start(self):
        for i in range(self.checkoutThreadMount):
            worker = threading.Thread(target=self.checkout_proxy, args=(self.ip_que,self.validip_que), name="验证IP线程%d" % (i))
            worker.start()
            print("验证IP线程开启%d" % (i))

    def checkout_proxy(self,ip_que,validip_que):
        while not ip_que.empty():
            # print("开始检测")
            inip = ip_que.get()
            ip = {'http': inip}
            proxy = request.ProxyHandler(ip)
            opener = request.build_opener(proxy)
            # ua=FakeUserAgent()
            url = 'http://httpbin.org/ip'
            reqhd = request.Request(url)
            ip = inip.split(':')[0]
            try:
                req = opener.open(reqhd, timeout=2)
                if req.code == 200:
                    con = req.read().decode('utf-8')
                    if ip in con:
                        # print("有效IP%s" % inip)
                        validip_que.put(inip)
                        print("当前有效IP数量为%d"%(validip_que.qsize()))
                    else:
                        pass
                        # print("无效IP%s" % inip)
                else:
                    pass
                    # print("无效IP%s" % inip)
            except Exception as e:
                pass
                #print("无效IP%s" % ip)
            ip_que.task_done()

    # print("线程结束")

    def collectUrl(self,ip_que):
        print("代理IP采集线程开启")
        while True:
            if ip_que.qsize() < 300:
                print("开始采集代理IP")
                with open('headers.txt', 'r') as f:
                    headerStr=f.read()
                    headersArr=headerStr.split('\n')
                headers={}
                for headerItem in headersArr:
                    headersItemName=headerItem.split(': ')[0]
                    headerItemValue=headerItem.split(': ')[1]
                    headers[headersItemName]=headerItemValue
                response = requests.get("http://www.66ip.cn/mo.php?sxb=&tqsl=300&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=http%3A%2F%2Fwww.66ip.cn%2F%3Fsxb%3D%26tqsl%3D300%26ports%255B%255D2%3D%26ktip%3D%26sxa%3D%26radio%3Dradio%26submit%3D%25CC%25E1%2B%2B%25C8%25A1",headers=headers)
                html_code = response.content.decode("gbk")
                reg = re.compile(r"\r\n\t\t(.*?)<br />")
                ip_list = re.findall(reg, html_code)
                for ip in ip_list:
                    ip_que.put(ip)
                print("成功收集代理IP%d条" % (len(ip_list)))
                print("当前代理IP个数为%d" % (ip_que.qsize()))
            else:
                # print("代理IP数量已达上限，开始休眠")
                time.sleep(1)


def main():
    ip_que=Queue(1200)
    validip_que=Queue(900000)
    proxy_helper=Proxy_helper(ip_que,validip_que,4,6)
    proxy_helper.run()

if __name__=="__main__":
    main()
