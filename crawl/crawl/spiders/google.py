import scrapy
from urllib.parse import quote


class GoogleSpider(scrapy.Spider):
    name = "google"
    # allowed_domains = ["google.com"]
    custom_settings = {
        "ROBOTSTXT_OBEY": False
    }

    script = """
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(10))
        return splash:html()
    end
    """

    def start_requests(self):
        url = f"https://www.google.com/search?q={quote(self.query)}"
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
            
        searchs = response.css("div#search > div > div > div")
        for search in searchs:
            yield {
                "link": search.css("a::attr(href)").get()
            }

        if current_page < int(self.page):
            pnnext = response.css("a#pnnext::attr(href)").get()
            url = f"https://www.google.com{pnnext}"
            yield scrapy.Request(url=url, callback=self.parse, meta={
                "splash": {
                    "args": {
                        'lua_source': self.script,
                    },
                    # "splash_url": "http://localhost:8050",
                    "endpoint": "execute"
                },
                "current_page": current_page + 1
            })