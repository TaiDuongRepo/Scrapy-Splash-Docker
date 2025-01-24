import scrapy


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
        url = "https://www.google.com/search?q=site:www.24h.com.vn%20%22mono%22"
        yield scrapy.Request(url=url, callback=self.parse, meta={
            "splash": {
                "args": {
                    'lua_source': self.script,
                },
                # "splash_url": "http://localhost:8050",
                "endpoint": "execute"
            }
        })

    def parse(self, response):
        searchs = response.css("div#search > div > div > div")
        for search in searchs:
            yield {
                "link": search.css("a::attr(href)").get()
            }