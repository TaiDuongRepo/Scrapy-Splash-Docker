import scrapy


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    
    def start_requests(self):
        url = "https://web-scraping.dev/testimonials"
        yield scrapy.Request(url=url, callback=self.parse, meta={
            "splash": {
                "args": {
                    "html": 1,
                    "png": 1
                }
            }
        })

    def parse(self, response):
        print(response.data.keys())
        "dict_keys(['png', 'url', 'requestedUrl', 'geometry', 'title', 'html'])"
        reviews = response.css("div.testimonial")
        for review in reviews:
            yield {
                "rate": len(review.css("span.rating > svg").getall()),
                "text": review.css("p.text::text").get()
            }