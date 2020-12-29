import scrapy

class TextSpider(scrapy.Spider):
    name = "text"

    def __init__(self, url='', xpath='', **kwargs):
        self.start_urls = [url]  # py36
        self.xpath = xpath
        super().__init__(**kwargs)  # python3

    #def start_requests(self):
    #    for url in self.urls:
    #        yield scrapy.Request(url=url, callback=self.parse, errback=lambda failure, item=None: self.on_error(failure, item))

    #def on_error(self, failure, item):
    #    yield item

    def parse(self, response):
        text = response.xpath(self.xpath).get()
        yield {"text" : text}