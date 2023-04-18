#!/usr/bin/env python
# coding: utf-8

import datetime
import time

import schedule
from dotenv import load_dotenv

from main import run


def run_script():
    start_date = str(datetime.date.today() - datetime.timedelta(days=7))
    end_date = str(datetime.date.today())
    print('Start date:', start_date)
    print('End date:', end_date)
    run('db.sqlite3', start_date, end_date, True)


load_dotenv()
schedule.every(6).hours.do(run_script)

while True:
    schedule.run_pending()
    time.sleep(1)
