from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawl.spiders.reviews import ReviewsSpider
from crawl.spiders.bing import BingSearchSpider  
from crawl.spiders.reviews import GoogleNewsSpiders

project_settings = get_project_settings()
process = CrawlerProcess(settings=project_settings)

process.crawl(GoogleNewsSpiders)

process.start()
