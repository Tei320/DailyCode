from crawler import Crawler
from db import RedisClient
from setting import POOL_UPPER_THRESHOLD

class Getter():
    def __init__(self):
        self.crawler = Crawler()
        self.redis = RedisClient()

    def is_over_threshold(self):
        '''
        判断是否达到了代理池限制
        '''
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)

