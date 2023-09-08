# GnarvelousGrowbrain


Uses Python, SQLite3, and the cronjob to automate garden functions.

Hardware is a Raspberry Pi (Model 3 used), 5V relay board, wireless keyboard, touchscreen display.

GUI created using Tkinter and ttkbootstrap (https://ttkbootstrap.readthedocs.io/en/latest/).

TO DO:
* Add functionality to the number keypad
* Integrate option to send email alerts
* Create other modules to control other devices
* Real world test

BASIC OPERATION

FARM.PY:
* Main script.  You could set farm.py to automatically run on boot up of the pi, or create an executable icon on the Desktop.  Farm.py connects to dht.db and gb_config.db to update and retrieve the environmental values and timer settings.
 
CRONJOB:
* The cronjob automatically runs gpiobrain.py every minute. See photos in support for an example of the cron task

GPIOBRAIN.PY:
* gpiobrain.py runs a function for each module, such as "light_cycle()", which grabs the values from the database and makes changes to the GPIO pins as necessary.

* Example:  You want the lights to come on at 8:00 AM.  You navigate to the Lights module in farm.py, and enter "8" for the Lights ON Hour, and "00" or "0" for the Lights ON Minute, and click on "SAVE".  These values are then stored in the database.  The cronjob runs gpiobrain.py every minute, and when it does so at 8:00 AM, the conditional for lights turning on will evaluate to True, and the script will then turn on the lights.

* gpiobrain.py also takes measurements of Temp, Humidity, and other environment variables at a specified interval (default is 15 minutes), and adds a new SQL entry recording including the datetime of the measurement.

SUPPORT:
* photos and media to support construction and design

UTILITIES:
* useful scripts to reset the Pi, reset GPIO pins, manual control of outlets

VERSIONS:
* deprecated files, alternate configurations