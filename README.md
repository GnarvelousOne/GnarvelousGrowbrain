# GnarvelousGrowbrain


Uses Python, SQLite3, and the cronjob to automate garden functions.

Hardware is a Raspberry Pi, 5V relay board, wireless keyboard, touchscreen display.

GUI created using Tkinter and ttkbootstrap (https://ttkbootstrap.readthedocs.io/en/latest/).

BASIC OPERATION:

Run menu.py to view the current environmental varibles, and to run modules such as Lights, Water, etc.  You could set menu.py to automatically run on boot up of the pi, or create an executable icon on the Desktop.  Menu.py accesses dht.db and gb_config.db to retrieve the current recorded values, and displays them on the screen.

Use the different modules to store values in the SQL database, such as "lights_on_hour", as well as manually control the power to each device. 

The cronjob automatically runs gpiobrain.py every minute.

gpiobrain.py runs a function for each module, such as "light_cycle()", which grabs the values from the database and makes changes to the GPIO pins as necessary.

Example:  You want the lights to come on at 8:00 AM.  You open the lights.py module from menu.py, and enter "8" for the Lights ON Hour, and "00" or "0" for the Lights ON Minute, and click on "SAVE".  These values are then stored in the database.  The cronjob runs gpiobrain.py every minute, and when it does so at 8:00 AM, the conditional for lights turning on will evaluate to True, and the script will then turn on the lights. 

gpiobrain.py also takes measurements of Temp, Humidity, and other environment variables at a specified interval (default is 15 minutes), and adds a new SQL entry recording including the datetime of the measurement.


TO DO:
* Create other modules to control other devices such as fans, drain pumps.
* 
* Create option to send email alerts
