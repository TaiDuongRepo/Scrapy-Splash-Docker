# # Define here the models for your spider middleware
# #
# # See documentation in:
# # https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# from scrapy import signals

# # useful for handling different item types with a single interface
# from itemadapter import is_item, ItemAdapter
# from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
# from w3lib.http import basic_auth_header

# from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
# from w3lib.http import basic_auth_header

# class ProxyMiddleware(HttpProxyMiddleware):
#     def __init__(self, auth_encoding='utf-8'):
#         self.proxy_user = 'sp08-16160'
#         self.proxy_password = 'CXCLJ'
#         self.proxy_url = 'sp08-20.proxy.mkvn.net'
#         self.proxy_port = '16160'
#         self.proxy_scheme = 'http'
#         self.proxy_auth = basic_auth_header(self.proxy_user, self.proxy_password)
#         self.proxy = f"{self.proxy_scheme}://{self.proxy_url}:{self.proxy_port}"
#         super().__init__(auth_encoding)

#     def process_request(self, request, spider):
#         request.meta['proxy'] = self.proxy
#         request.headers['Proxy-Authorization'] = self.proxy_auth
#         super().process_request(request, spider)

# class CrawlSpiderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.

#         # Should return None or raise an exception.
#         return None

#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.

#         # Must return an iterable of Request, or item objects.
#         for i in result:
#             yield i

#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.

#         # Should return either None or an iterable of Request or item objects.
#         pass

#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.

#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r

#     def spider_opened(self, spider):
#         spider.logger.info("Spider opened: %s" % spider.name)


# class CrawlDownloaderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.

#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None

#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.

#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response

#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.

#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass

#     def spider_opened(self, spider):
#         spider.logger.info("Spider opened: %s" % spider.name)


# middlewares.py

from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from w3lib.http import basic_auth_header

from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from w3lib.http import basic_auth_header

from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from w3lib.http import basic_auth_header

class ProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, auth_encoding='utf-8', proxy=None):
        """
        Constructor có tham số `proxy` để cấu hình proxy.

        - `auth_encoding`: Mã hóa xác thực (mặc định là utf-8).
        - `proxy`: Địa chỉ proxy, nếu không truyền vào sẽ sử dụng giá trị mặc định.
        """
        # Nếu không có proxy được truyền vào, dùng giá trị mặc định
        self.proxy = proxy or 'sp08-26.proxy.mkvn.net:17116:sp08-17116:FNPYO'

        # Phân tách proxy thành các thành phần
        proxy_parts = self.proxy.split(":")
        self.proxy_domain = proxy_parts[0]  # sp08-13.proxy.mkvn.net
        self.proxy_port = proxy_parts[1]    # 15051
        self.proxy_user = proxy_parts[2]    # sp08-15051
        self.proxy_pass = proxy_parts[3]    # GRNHS

        # Tạo proxy authentication
        self.proxy_auth = basic_auth_header(self.proxy_user, self.proxy_pass)

        # Tạo URL cho proxy
        self.proxy_url = f"http://{self.proxy_domain}:{self.proxy_port}"

        # Khởi tạo middleware, không cần truyền auth_encoding nếu không cần
        super().__init__(auth_encoding)

    def process_request(self, request, spider):
        # Đặt proxy vào meta và thêm header cho proxy authentication
        request.meta['proxy'] = self.proxy_url
        request.headers['Proxy-Authorization'] = self.proxy_auth
        super().process_request(request, spider)


class CrawlSpiderMiddleware:
    # Các phương thức cần thiết cho spider middleware

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class CrawlDownloaderMiddleware:
    # Các phương thức cần thiết cho downloader middleware

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
