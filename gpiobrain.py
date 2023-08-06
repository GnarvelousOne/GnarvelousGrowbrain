#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import datetime
import sqlite3

    # outlets numbered from left to right
    # 1 is 5
    # 2 is 6
    # 3 is 13
    # 4 is 19
    # 5 is 26
    # 6 is 16
    # 7 is 20
    # 8 is 21



timeNow = datetime.datetime.now()


# Create master brain program here to check all DB values and make changes as needed

# Get values from sensors
    # run DHT brain, update DB

# Get values from database

# Compare time-based values to the current time to decide if change needs to be made

# Change the GPIO statuses

# 


conn = sqlite3.connect("gb_config.db")
c = conn.cursor()


def lightcycle():
    
    # change this into a config screen to choose values for the outputs
    lights = 5
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(lights, GPIO.OUT)
    #GPIO.output(lights, GPIO.LOW)


    c.execute("SELECT lights_on_hour FROM gb")
    lights_on_hour = c.fetchone()[0]
    c.execute("SELECT lights_on_minute FROM gb")
    lights_on_minute = c.fetchone()[0]
    c.execute("SELECT lights_off_hour FROM gb")
    lights_off_hour = c.fetchone()[0]
    c.execute("SELECT lights_off_minute FROM gb")
    lights_off_minute = c.fetchone()[0]
    c.execute("SELECT light_status FROM gb")
    light_status = c.fetchone()[0]


    
    on_time = lights_on_hour + (lights_on_minute/60)
    on_time_display = str(lights_on_hour) + ':' + str(lights_on_minute)
    
    off_time = lights_off_hour + (lights_off_minute/60)
    off_time_display = str(lights_off_hour) + ':' + str(lights_off_minute)
    
    hour_now = int(timeNow.strftime('%H'))
    minute_now = int(timeNow.strftime('%M'))
    
    time_now = hour_now + (minute_now/60)
    time_now_display = str(hour_now) + ':' + str(minute_now)

    print(f"light_cycle() called at: {time_now_display}")
    
    # time must be expressed in military to do the math
    
    # check status of lights
    #if light_status == 0: # if the lights are currently off
        
    if time_now == on_time: # if the time now is either equal to or later than the time for lights to come on
        
        # turn lights on  
        GPIO.output(lights, False)
        
        # set light_status to on
        c.execute("UPDATE gb SET light_status = ?", (1,))
        
        conn.commit()
        conn.close()
        
        print("Light Status changed to: On")
        print(f"time_now: {time_now_display}")
        print(f"on_time: {on_time_display}")
        
              
    #else: # if the lights are currently on
        
    if time_now == off_time: # if the time now is either equal to or later than the time for lights to turn off
        
        
        # create a range of times to compare the time_now - see if it fits in the lights on range, or is it the lights off range?
        
        
        # turn lights off
        GPIO.output(lights, True)
        
        # set light_status to off
        c.execute("UPDATE gb SET light_status = ?", (0,))

        conn.commit()
        conn.close()
        
        print("Light Status changed to: Off")
        print(f"time_now: {time_now_display}")
        print(f"off_time: {off_time_display}")


lightcycle()
