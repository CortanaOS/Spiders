import json
import random
import requests
import time
from twisted.internet.error import TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.internet import defer
from twisted.web.client import ResponseFailed
from fake_useragent import UserAgent


class RandomUserAgentMiddleware(object):
    """随机更换 User-Agent"""

    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())


def random_proxy():
    """获取一个随机代理"""
    # 芝麻代理
    # proxy_url = "http://http.tiqu.alicdns.com/getip3?num=5&type=2&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions=&gm=4"
    # ip_key = "ip"
    # port_key = "port"

    # 黑洞代理
    proxy_url = "http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.hdtiqu_api_url&packid=0&fa=0&groupid=0&fetch_key=&time=100&qty=10&port=1&format=json&ss=5&css=&dt=0&pro=&city=&usertype=4"
    ip_key = "IP"
    port_key = "Port"
    try:
        # 芝麻代理 url
        response = requests.get(proxy_url)
        response = response.text
        result = json.loads(response)
        proxy_list = result.get('data')
        proxy_count = len(proxy_list)
        num = random.randint(0, proxy_count)
        ip = proxy_list[num].get(ip_key)
        port = proxy_list[num].get(port_key)
        proxy = 'https://{}:{}'.format(ip, port)

        return proxy
    except:
        raise ValueError("proxy is None")


class ProxiesMiddleware:
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)

    def __init__(self):
        try:
            self.proxy = random_proxy()  # 随机获取一个代理方法
        except:
            self.proxy = random_proxy()  # 随机获取一个代理方法

        self.count = 0

    def process_request(self, request, spider):
        if self.count % 500 == 0 and self.count != 0:
            self.proxy = random_proxy()
        self.count += 1
        spider.logger.info("[proxy]   {}".format(self.proxy))
        request.meta["proxy"] = self.proxy

    def process_response(self, request, response, spider):
        # 因为遇到过那种返回状态码是200但是是一个被反扒的界面，界面固定都是小于3000字符
        # if len(response.text) < 3000 or response.status in [403, 400, 405, 301, 302, 418]:
        if response.status in [403, 400, 405, 412, 301, 302, 402, 418, 414]:
            spider.logger.info("[此代理报错]   {}".format(self.proxy))
            new_proxy = random_proxy()
            self.proxy = new_proxy
            spider.logger.info("[更的的新代理为]   {}".format(self.proxy))
            # break
            new_request = request.copy()
            new_request_l = new_request.replace(url=request.url)
            return new_request_l
        return response

    def process_exception(self, request, exception, spider):
        # 捕获几乎所有的异常
        if isinstance(exception, self.ALL_EXCEPTIONS):
            # 在日志中打印异常类型
            spider.logger.info("[Got exception]   {}".format(exception))
            spider.logger.info("[需要更换代理重试]   {}".format(self.proxy))
            new_proxy = random_proxy()
            self.proxy = new_proxy
            spider.logger.info("[更换后的代理为]   {}".format(self.proxy))
            new_request = request.copy()
            new_request_l = new_request.replace(url=request.url)
            return new_request_l
        # 打印出未捕获到的异常
        spider.logger.info("[not contained exception]   {}".format(exception))
