BOT_NAME = "crawl"

SPIDER_MODULES = ["crawl.spiders"]
NEWSPIDER_MODULE = "crawl.spiders"


# Obey robots.txt rules
ROBOTSTXT_OBEY = True


# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Splash settings
SPLASH_URL = 'http://splash:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

REQUEST_FINGERPRINTER_CLASS = 'scrapy_splash.SplashRequestFingerprinter'

