#!/usr/bin/python

import os
import datetime

timeNow = datetime.datetime.now()
print("\n"+"*** Now running reboot.py at " + str(timeNow.strftime('%A %m/%d %H:%M %p')) + " as scheduled in crontab ***"+"\n")
os.system("sudo reboot")
