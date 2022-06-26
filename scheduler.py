import os
import schedule
import time
import random
import pymysql
import asyncio
from hcskr.hcskr import selfcheck, QuickTestResult

def job():
   print("scheduler started")
   db= pymysql.connect(host=os.getenv('db_host'), port=os.getenv('db_port'), user=os.getenv('db_us'), password=os.getenv('db_ps'), db=os.getenv('db_database'), charset='utf8')
   cur= db.cursor()
   sql1= "SELECT COUNT(*) FROM autocheck;"
   cur.execute(sql1)
   result1 = cur.fetchall()
   print(result1)
   for i in range(result1[0][0]):
    il = i + 1
    sql2= f"SELECT * FROM autocheck WHERE indexrow = {il};"
    cur.execute(sql2)
    result2 = cur.fetchall()
    data = selfcheck(result2[0][1],result2[0][2],result2[0][3],result2[0][4],result2[0][5],result2[0][6],quicktestresult=QuickTestResult['none'])
    print(data)
   schedule_next_run()


def schedule_next_run():
   time_str = '{:02d}:{:02d}'.format(random.randint(5, 6), random.randint(30, 50))
   schedule.clear()
   print("Scheduled for {}".format(time_str))
   schedule.every().day.at(time_str).do(job)

schedule_next_run()

while True:
   schedule.run_pending()
   time.sleep(1)
    