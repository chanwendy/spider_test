# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy
from scrapy import signals
import time
from selenium import webdriver
import random
from pactencent.user_agent import agents


class PactencentSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PactencentDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        # 创建中间件对象， signal。connect 使中间件对象能过访问scrapy的一些核心主件
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 该方法会在请求到达的时候进行自动调用
        # Called for each request that goes through the downloader
        # middleware.
        # 在这里设置的请求，将会是最后请求，会将settings设置的headers进行覆盖

        # Must either:
        # 1.return None ：表示request请求在这里已经处理完毕，下一步丢给其他的process_request方法来进行下一步的处理，如果没有方法对request进行处理了，则直接扔给downloader进行下载
        # - return None: continue processing this request
        # 2. return scrapy.http.HtmlResponse ：表示数据已经从下载器中下载回来了，下一步会丢给process_response进行下一步的处理，若果没有则直接返回给引擎
        # - or return a Response object
        # return request：返回请求对象时，会停止调用其他的process_request方法对该请求的处理，直接将该请求扔给downloader进行下载
        # - or return a Request object
        # raise InoreRequest：若引发异常，会将改请求丢给process_exception进行处理，如果process_exception无法处理，则会丢给request中的errback，如果errback也无法处理则凉凉。
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # 在响应到达时进行自动调用
        # Called with the response returned from the downloader.

        # Must either;
        # 1.return response：可以丢给其他process_response进行处理，处理完成后返回引擎
        # - return a Response object
        # 2. return request: 则将改request丢给process_request进行进一步处理
        # - return a Request object
        # 3. 若引发错误处理方法同process_request中引发错误的方法一致
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # 1.return none：则表示可以进行下一步
        # - return None: continue processing this exception
        # 2.return response：可以交给process_response进行下一步处理，处理完成后即返回引擎
        # - return a Response object: stops process_exception() chain
        # 3.return request: 返回request对象会交给process_request进行进一步的处理，处理完成后交给下载器
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 实现用户代理
# 1. 在中间件中创建代理类
# 2. 代理的一些用户名
# 3. 在类中random。choice（）进行抽选
# 4. 去setting文件中对类进行注册，同时修改scrapy自己默认的为'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers['User-Agent'] = agent
        return None


class ChromeDynamicMiddleware(object):
    def process_request(self, request, spider):
        """
        request对象可能是
        1. 爬虫文件跟进的请求
        2. 爬虫文件start_urls的请求
        3. 中间件类中返回的请求.

        反正请求流到中间件的时候, process_request就会去处理这些请求, 怎么处理看你中间件代码怎么写.
        在这里, 请求流到了这里, 先进行if条件判断, 若当前请求的url是小说书库的第一页(http://www.xs4.cc/shuku/)的话.
        我就用selenium来访问这个url, 然后获取动态加载的数据, 然后构造response返回给引擎.
        若流过来的请求的url不是(http://www.xs4.cc/shuku/), 那就直接return None, 交给其他中间件处理, 我反正是不管了.

        selenium访问请求的headers是什么?我用的chrome, chrome该携带什么headers, selenium自己就携带什么.
        selenium发送的请求 到 获取到数据, 都是在一个方法中就完成,  跟其他中间件有什么关系?

        :param request:
        :param spider:
        :return:
        """
        # 创建浏览器设置对象, 可设置相关参数如以无界面方式运行driver.
        # opts = webdriver.ChromeOptions()
        # opts.add_argument("--headless")

        # 1. 判断请求是否是目标请求
        if request.url == "https://hr.tencent.com/position.php":
            # 2. 创建对应的浏览器driver对象
            driver = webdriver.Chrome()
            # 3. 通过driver对象访问页面, 获取渲染后的动态数据.
            driver.get("https://hr.tencent.com/position.php")
            # 4. 由于访问可能存在不确定因素, 如网络延迟, 所以等待浏览器加载页面数据需要一定时间.
            time.sleep(1.5)
            # 5. 通过driver对象获取加载后的页面数据
            html_data = driver.page_source
            # 6. 使用完driver对象需进行退出.
            driver.quit()
            # 7. 构造响应对象并返回.
            return scrapy.http.HtmlResponse(headers={"name": "hello world"}, url=request.url,
                                            body=html_data, encoding="UTF-8", request=request)
        else:
            # 若不是目标请求就返回None.
            return None


