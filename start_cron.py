# Starting script for cron jobs.
from scrapyscript import Job, Processor
from webtracker.spiders.text_spider import TextSpider
import logging
import multiprocessing
import parse
import atexit
import checker

running = True
processes = []
jobs = []


def run_scrape_job(job, track):
    processor = Processor(settings=None)
    data = processor.run(job)
    if data:
        checker.CommandProcessor(track, data[0]["text"], email_info)


def exit_handler():
    for p in processes:
        p.terminate()


atexit.register(exit_handler)

logging.getLogger('scrapy').propagate = False

file_list = parse.convert_file_to_list(parse.read_file("track.txt"))
file_list = parse.clean_list(file_list)
file_list = parse.extract_track_inputs(file_list)

email_info = parse.extract_email_input("config.cfg")

for track in file_list:
    jobs.append(Job(TextSpider, url=track[parse.TRACK_PARAMS.index("url")], xpath=track[parse.TRACK_PARAMS.index("xpath")]))

for i in range(len(jobs)):
    x = multiprocessing.Process(target=run_scrape_job, args=(jobs[i], file_list[i],))
    processes.append(x)
    x.start()

for process in processes:
    process.join()