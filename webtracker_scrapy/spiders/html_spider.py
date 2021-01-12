import scrapy
from scrapy.selector import Selector

class HTMLSpider(scrapy.Spider):
    name = "HTMLSpider"

    def __init__(self, tracks=[], **kwargs):
        self.tracks = tracks
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        for track in self.tracks:
            url = track["url"]
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(track=track))

    def parse(self, response, track): 
        try:
            text = response.css(track["selector"]+"::text").get()
            track["result"] = text
        except:
            raise Exception(ValueError, response.url + " failed to parse, make sure selector is correct!")
        track["response_url"] = response.url
        yield track
