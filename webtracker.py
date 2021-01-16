import parse
import mailer
import checker
import logging
import time
import threading
import datetime

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
        self.threads = []


    def run_track(self, track):
        while True:
            try:
                job = Job(HTMLSpider, tracks=[track])
                processor = Processor(settings=None)
                data = processor.run([job])
                track = checker.process_command(data[0])
                t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("[" + t + "]", "\"" + track["title"] + "\"", "command:", track["check"],"expected:", track["element_title"], "actual:", track["result"])
                if track["redirect"]:
                    print("[" + t + "]", "\"" + track["title"] + "\"", "respone URL is not equal to request!")
                elif track["trigger"]:
                    mailer.send_email(self.config_info["sender_email"], self.config_info["sender_email_password"], self.config_info["recipient_email"], 
                    parse.message_format(track, track["message_header"]), parse.message_format(track, track["message_body"]))      
            except Exception as err:
                mailer.send_email(self.config_info["sender_email"], self.config_info["sender_email_password"], self.config_info["recipient_email"], 
                parse.message_format(track, "$title failure"), parse.message_format(track, "$url \n" + err))
            time.sleep(int(track["timer"]))


    def start_thread(self):    
        for track in self.tracking_info:
            x = threading.Thread(target=self.run_track, args=(track,))
            self.threads.append(x)
            x.start()


    def start(self):
        job = Job(HTMLSpider, tracks=self.tracking_info)
        while True:
            processor = Processor(settings=None)
            tracks = processor.run([job])

            for track in tracks:
                track = checker.process_command(track)
                t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("[" + t + "]", "\"" + track["title"] + "\"", "command:", track["check"],"expected:", track["element_title"], "actual:", track["result"])
                if track["redirect"]:
                    print("[" + t + "]", "\"" + track["title"] + "\"", "respone URL is not equal to request!")
                elif track["trigger"]:
                    mailer.send_email(self.config_info["sender_email"], self.config_info["sender_email_password"], self.config_info["recipient_email"], 
                    parse.message_format(track, track["message_header"]), parse.message_format(track, track["message_body"]))
            job = Job(HTMLSpider, tracks=tracks)
            time.sleep(int(track["timer"]))


if __name__ == "__main__":
    track = WebTracker()
    track.start_thread()