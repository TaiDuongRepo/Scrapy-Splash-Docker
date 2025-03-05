
import scrapy
from urllib.parse import quote
from datetime import datetime
from urllib.parse import urlparse
'''

# Giờ qua
https://www.google.com/search?q={quote(self.query)}&source=lnt&tbs=qdr:h&sa=X&ved=2ahUKEwiXy7SJze-LAxVjsVYBHae2ABcQpwV6BAgEEAw&biw=1536&bih=730&dpr=1.25
# 24h qua
https://www.google.com/search?q={quote(self.query)}&source=lnt&tbs=qdr:d&sa=X&ved=2ahUKEwi13_Sdze-LAxXqsFYBHRamNi0QpwV6BAgGEA0&biw=1536&bih=730&dpr=1.25
# 1 tuần qua
https://www.google.com/search?q={quote(self.query)}&source=lnt&tbs=qdr:w&sa=X&ved=2ahUKEwjiipnYze-LAxWwrVYBHQ_VHOgQpwV6BAgCEA4&biw=1536&bih=730&dpr=1.25
# 1 tháng qua
https://www.google.com/search?q={quote(self.query)}&source=lnt&tbs=qdr:m&sa=X&ved=2ahUKEwjGs_nxze-LAxWIglYBHT0AHG0QpwV6BAgFEA8&biw=1536&bih=730&dpr=1.25
# 1 năm qua
https://www.google.com/search?q={quote(self.query)}&source=lnt&tbs=qdr:y&sa=X&ved=2ahUKEwjpmKSEzu-LAxW0r1YBHTtPNb4QpwV6BAgFEBA&biw=1536&bih=730&dpr=1.25
'''
class GoogleSpider(scrapy.Spider):
    name = "google"
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "FEED_FORMAT": "json",  
        "FEED_ENCODING": "utf-8",  
        "CONCURRENT_REQUESTS": 16,  
        "CONCURRENT_REQUESTS_PER_DOMAIN": 8,  
        "CONCURRENT_REQUESTS_PER_IP": 8,  
        "DOWNLOAD_DELAY": 0.25,  
        'crawl.middlewares.ProxyMiddleware': 100,  

    }

    script = """
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(5))
        return splash:html()
    end
    """
    def start_requests(self):
        time_filters = {
            "hour": "qdr:h",
            "day": "qdr:d",
            "week": "qdr:w",
            "month": "qdr:m",
            "year": "qdr:y",
        }
        tbs_param = time_filters.get(self.time_range, "qdr:d")

        # url =f"https://www.google.com/search?q={quote(self.query)}&tbs=cdr%3A1%2Ccd_min%3A2024%2Ccd_max%3A&tbm="
        url = f"https://www.google.com/search?q={quote(self.query)}&tbs={tbs_param}&tbm="

    
        yield scrapy.Request(url=url, callback=self.parse, meta={
            "splash": {
                "args": {
                    'lua_source': self.script,
                },
                # "splash_url": "http://localhost:8050",
                "endpoint": "execute"
            },
            "current_page": 1
        })
    


    def parse(self, response):
        current_page = response.meta.get("current_page")
        # searchs = response.css("div > div > div > div > div > span > a")
        searchs = response.css("#rso > div > div > div")

        for search in searchs:
            link = search.css("::attr(href)").get()
            source = search.css("::text").get()
            # published_at get  span.LEwnzc.Sqrs4e
            published_at = search.css("span.LEwnzc.Sqrs4e span::text").get()

            if link:
                parsed_url = urlparse(link)
                domain = parsed_url.netloc

                if "google.com" not in domain:
                    yield scrapy.Request(url=link, callback=self.parse_detail, meta={
                                        'source': source, 
                                        'published_at': published_at
                                    })

        if current_page < int(self.page):
            pnnext = response.css("a#pnnext::attr(href)").get()
            if pnnext:
                url = f"https://www.google.com{pnnext}"
                yield scrapy.Request(url=url, callback=self.parse, meta={
                    "splash": {
                        "args": {
                            'lua_source': self.script,
                        },
                        "endpoint": "execute"
                    },
                    "current_page": current_page + 1
                })

    '''
    crawl4ai
    '''
    def parse_detail(self, response):
        source = response.meta.get("source")
        title = response.css("h1::text").get() 
        published_at = response.meta.get("published_at")
        # Lấy thời gian cào hiện tại tính trên máy không phải thẻ trang web
        crawl_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")        

        parsed_url = urlparse(response.url)
        website = parsed_url.netloc  # Ví dụ: "motcuocsong.vn"

        yield {
            'source': source,
            "title": title,
            "url": response.url ,
            "crawl_at": crawl_at,
            "website": website,
            "published_at": published_at

        }
        
    