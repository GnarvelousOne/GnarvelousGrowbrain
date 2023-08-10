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


conn = sqlite3.connect("gb_config.db")
c = conn.cursor()


def lightcycle():
    
    lights = 5
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(lights, GPIO.OUT)

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
    
        
    if time_now == on_time:
        
        # turn lights on  
        GPIO.output(lights, False)
        
        # set light_status to on
        c.execute("UPDATE gb SET light_status = ?", (1,))
        
        conn.commit()
        conn.close()
        
        print("Light Status changed to: On")
        print(f"time_now: {time_now_display}")
        print(f"on_time: {on_time_display}")
        
              
    if time_now == off_time:
        
        # turn lights off
        GPIO.output(lights, True)
        
        # set light_status to off
        c.execute("UPDATE gb SET light_status = ?", (0,))

        conn.commit()
        conn.close()
        
        print("Light Status changed to: Off")
        print(f"time_now: {time_now_display}")
        print(f"off_time: {off_time_display}")

def watercycle():
    
    water = 6
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(water, GPIO.OUT)

    c.execute("SELECT water_on_hour FROM gb")
    water_on_hour = c.fetchone()[0]
    c.execute("SELECT water_on_minute FROM gb")
    water_on_minute = c.fetchone()[0]
    c.execute("SELECT water_off_hour FROM gb")
    water_off_hour = c.fetchone()[0]
    c.execute("SELECT water_off_minute FROM gb")
    water_off_minute = c.fetchone()[0]
    c.execute("SELECT water_status FROM gb")
    water_status = c.fetchone()[0]

    on_time = water_on_hour + (water_on_minute/60)
    on_time_display = str(water_on_hour) + ':' + str(water_on_minute)
    
    off_time = water_off_hour + (water_off_minute/60)
    off_time_display = str(water_off_hour) + ':' + str(water_off_minute)
    
    hour_now = int(timeNow.strftime('%H'))
    minute_now = int(timeNow.strftime('%M'))
    
    time_now = hour_now + (minute_now/60)
    time_now_display = str(hour_now) + ':' + str(minute_now)

    print(f"watercycle() called at: {time_now_display}")
    
    # time must be expressed in military to do the math
    
        
    if time_now == on_time:
        
        # turn water on  
        GPIO.output(water, False)
        
        # set water_status to on
        c.execute("UPDATE gb SET water_status = ?", (1,))
        
        conn.commit()
        conn.close()
        
        print("Water Status changed to: On")
        print(f"time_now: {time_now_display}")
        print(f"on_time: {on_time_display}")
        
              
    if time_now == off_time:
        
        # turn water off
        GPIO.output(water, True)
        
        # set water_status to off
        c.execute("UPDATE gb SET water_status = ?", (0,))

        conn.commit()
        conn.close()
        
        print("Water Status changed to: Off")
        print(f"time_now: {time_now_display}")
        print(f"off_time: {off_time_display}")

# run the functions

lightcycle()
watercycle()
