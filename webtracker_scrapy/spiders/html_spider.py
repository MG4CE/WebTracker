import scrapy

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
        text = response.xpath(track["xpath"]).get()
        track["response_url"] = response.url
        track["result"] = text
        #print(track)
        yield track
