# Continuous start script, not ready.
from scrapyscript import Job, Processor
from webtracker.spiders.text_spider import TextSpider
import logging
import threading
import parse
import time
import atexit
import checker

running = True
threads = []
jobs = []


def run_scrape_job(job, run_int):
    while running:
        processor = Processor(settings=None)
        data = processor.run(job)
        print(data)
        time.sleep(run_int)


def exit_handler():
    running = False
    for thread in threads:
        print(thread)
        thread.join(1)


atexit.register(exit_handler)

logging.getLogger('scrapy').propagate = False

file_list = parse.convert_file_to_list(parse.read_file("track.txt"))
file_list = parse.clean_list(file_list)
file_list = parse.extract_track_inputs(file_list)

email_info = parse.extract_email_input("config.cfg")

for track in file_list:
    jobs.append(
        Job(TextSpider, url=track[parse.TRACK_PARAMS.index("url")], xpath=track[parse.TRACK_PARAMS.index("xpath")]))

for job in jobs:
    t = threading.Thread(target=run_scrape_job, args=(job, 5))
    threads.append(t)
    t.start()
