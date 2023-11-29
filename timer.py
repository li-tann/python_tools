# -*- coding:utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import time
import random

def print_time():
    print('get time, Now is %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def work():
    sec = random.randint(2,7)
    print("randint: {}".format(sec))
    time.sleep(sec)
    print("work over.")

    

        

sched = BlockingScheduler()

job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

sched.configure(job_defaults=job_defaults)

# 每隔5秒运行一次my_job1
sched.add_job(print_time, 'interval', seconds=1, id='print_time')
# 每隔5秒运行一次my_job2
sched.add_job(work, 'interval', seconds=3, id='work')
sched.start()


