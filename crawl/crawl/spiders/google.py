import scrapy
from urllib.parse import quote
from datetime import datetime
from urllib.parse import urlparse


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
        url =f"https://www.google.com/search?q={quote(self.query)}&tbs=cdr%3A1%2Ccd_min%3A2024%2Ccd_max%3A&tbm="
        print("*******", url)
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

        searchs = response.css("div > div > div > div > div > span > a")

        for search in searchs:
            link = search.css("::attr(href)").get()
            source = search.css("::text").get()

            if link:
                parsed_url = urlparse(link)
                domain = parsed_url.netloc

                if "google.com" not in domain:
                    yield scrapy.Request(url=link, callback=self.parse_detail, meta={'source': source})

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
        # get author header > div > span
        author = response.css("header > div > span::text").get()
        # get published_date header > div > date
        published_date = response.css("header > div > date::text").get().strip().replace("\n",' ')
        
        # Lấy thời gian cào hiện tại tính trên máy không phải thẻ trang web
        crawl_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")        
        # get description  div.right-content > div.main-post
        description =  " ".join(response.css("article *::text").getall()).strip()
        description = " ".join(description.split())
        parsed_url = urlparse(response.url)
        website = parsed_url.netloc  # Ví dụ: "motcuocsong.vn"
        article_id = response.css("article::attr(id)").get()

        yield {
            'source': source,
            "title": title,
            "url": response.url ,
            "author": author,
            "published_date": published_date,
            "crawl_at": crawl_at,
            "description": description,
            "website": website, 
            "article_id": article_id

        }
        
    
