# Set the config path and timing (on demand or timed)
# Access a list of ETL job links
# Iterate through list and visit each link
    # If midway is required - first route to the midway-auth (use existing cookie grabber)
    # If "Progress" is favourable
        #  Find the "Prioritize" button and click it
        #  Add job to the list of completed jobs
    # If "Progress" is not favourable
        #  Add job to the list of pending jobs
# Give a status report 

import os
from config import *
from utils import *

processor = SeleniumClass()


for link in get_job_list():
    site = processor.open_link(link)
    if processor.evaluate_job(site):
        completed_jobs.append(link)
        continue
    elif processor.button_clickable(site):
        processor.prioritize_job()
        completed_jobs.append(link)
        continue
    else:
        completed_jobs.append(link)

processor.close()
status_report()


if __name__ == "__main__":
    os.join(os.getcwd(), "main.py")