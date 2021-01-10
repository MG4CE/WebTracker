import parse
import mailer
import checker
import logging
import time

from scrapyscript import Job, Processor
from webtracker_scrapy.spiders.html_spider import HTMLSpider

CONFIG_FILE = "config.cfg"
TRACKING_FILE = "track.txt"

class WebTracker():
    def __init__(self):
        logging.getLogger('scrapy').propagate = False

        self.tracking_info = parse.convert_file_to_list(parse.read_file(TRACKING_FILE))
        self.tracking_info = parse.clean_list(self.tracking_info)
        self.tracking_info = parse.extract_track_inputs(self.tracking_info)

        self.config_info = parse.extract_config_input(CONFIG_FILE)

    def start(self):
        while True:
            job = Job(HTMLSpider, tracks=self.tracking_info)
            processor = Processor(settings=None)
            tracks = processor.run([job])

            for track in tracks:
                if checker.process_command(track):
                    mailer.send_email(self.config_info["sender_email"], self.config_info["sender_email_password"], self.config_info["recipient_email"], 
                    parse.message_format(track, track["message_header"]), parse.message_format(track, track["message_body"]))
            time.sleep(int(self.config_info["timeout"]))

if __name__ == "__main__":
    track = WebTracker()
    track.start()