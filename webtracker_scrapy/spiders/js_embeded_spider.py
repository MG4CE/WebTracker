# Weird behaviour ecounter, currently not needed
import scrapy
from scrapy_splash import SplashRequest

class JSRenderSpider(scrapy.Spider):
    name = "JSRender"

    def __init__(self, tracks=[], **kwargs):
        self.tracks = tracks
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        for track in self.tracks:
            url = track["url"]
            yield SplashRequest(url, self.parse,  endpoint='render.html', args={'wait': 0.5}, cb_kwargs=dict(track=track))

    def parse(self, response, track):
        text = response.xpath(track["xpath"]).get()
        track["result"] = text
        yield track