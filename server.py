

from time import sleep
from datetime import date, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import BaseJobStore
from resources.config import settings_server

settings = settings_server()

# Start the scheduler
sched = BackgroundScheduler()




## on init, load all posts from the scheduled post database

# Maybe switch post handlers based on which social media is being used?  
def post_handler(post_data):
    print(post_data)



def process_pending_scheduled_posts():
    # load all from data base
    # load all in current memory storage
    # compare the two and process anything unprocessed



# Here's the format used: 
to_convert = "2022-01-26 20:03:00"

# The job will be executed on November 6th, 2009
exec_date = date(2022, 11, 6)
exec_date_full = datetime(2022, 1, 24, 3, 36, 35)
job = sched.add_job(func=post_handler, trigger='date',run_date=exec_date_full, args=['text']) #need to add post data here. 
# need to store job in storage for reboot protection


# Start the scheduler
sched.start()

while True:
    sleep(1)
    # Check if there are any new posts. If so, process them into the system. 
    #print(datetime.now())
    #print(sched.get_jobs())