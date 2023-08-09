# GnarvelousGrowbrain


Uses Python, SQLite3, and the cronjob to automate garden functions.

Hardware is a Raspberry Pi, 5V relay board, wireless keyboard, touchscreen display.

GUI created using Tkinter and ttkbootstrap.


Use the different modules such as lights.py to store values in the SQL database, such as "lights_on_hour". 

The cronjob runs gpiobrain.py every minute.

gpiobrain.py runs a function for each module, such as "light_cycle()", which grabs the values from the database and makes changes to the GPIO pins as necessary.


Example:  You want the lights to come on at 8:00 AM.  You open lights.py and enter "8" for the Lights ON Hour, and "00" or "0" for the Lights ON Minute, and click on "SAVE".  These values are then stored in the database.  The cronjob runs gpiobrain.py every minute, and when it does so at 8:00 AM, the conditional for lights turning on will evaluate to True, and the script will then turn on the lights. 


TO DO:
* Create other modules to control other devices such as fans, irrigation.
* Create sensor module to record Temperature and Humidity
* Create a main screen from which to open each module
* Create option to send email alerts
* Clean up .py files, update comments
