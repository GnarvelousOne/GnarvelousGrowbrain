#! /usr/bin/python
import RPi.GPIO as GPIO
import time
import datetime
import board
import adafruit_dht
import sqlite3
import os



#from dht import dhtRun
#import dht


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

global try_counter
try_counter = 0

# Create master brain program here to check all DB values and make changes as needed

# Get values from sensors
    # run DHT brain, update DB

# Get values from database

# Compare time-based values to the current time to decide if change needs to be made

# Change the GPIO statuses




def temphumcheck():
    
    timeNow = datetime.datetime.now()
    #print(timeNow.minute)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbersIN
    GPIO.setup(4, GPIO.IN)

    # Get the temperature and humidity from dht
    
    #if True:
    if not int(timeNow.minute) % 15: 

        # get the current time
        timeNow = datetime.datetime.now()

        # set the high and low temp and hum alerts
        # to trigger sending an email alert:
        hightemp = 78
        lowtemp = 45
        highhum = 70
        
        # email addresses to send alert warnings
        recipientList = ['stephenmparvin@gmail.com']
        
        # Initial the dht device, with data pin connected to:
        dhtDevice = adafruit_dht.DHT11(board.D4)

        # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
        # This may be necessary on a Linux single board computer like the Raspberry Pi,
        # but it will not work in CircuitPython.
        # dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

        # make the lists to hold the readings
        temp_C_list = []
        temp_F_list = []
        humidity_list = []  

        # Now take the average of 3 DHT readings, and adjust for any errors.
        # Add each reading to its list.  
        # Sleep for 2.5 seconds inbetween readings because it takes 2 seconds
        # for the sensor to take a new reading.
        # The DHT measures two things: temp in celsius and relative humidity,
        # so we will convert C to F mathematically
        for i in range(3):
            try:
                temperature_c = dhtDevice.temperature
                temp_C_list.append(temperature_c)
            except:
                pass
                
            try:
                temperature_f = temperature_c * (9 / 5) + 32
                temp_F_list.append(temperature_f)
            except:
                pass
                
            try:
                humidity = dhtDevice.humidity
                humidity_list.append(humidity)
            except:
                pass

            time.sleep(2.5)

        # Add together the 3 readings so we can take the average.
        temp_C_sum = 0
        for i in temp_C_list:
            try:
                temp_C_sum += i
            except:
                pass

        temp_F_sum = 0
        for i in temp_F_list:
            try:
                temp_F_sum += i
            except:
                pass

        humidity_sum = 0
        for i in humidity_list:
            try:
                humidity_sum += i
            except:
                pass

        # Take average, unless we have non-integer readings due to an error.
        # In that case, return zero.
        try:
            displaytemp_c = (temp_C_sum/len(temp_C_list))
        except:
            displaytemp_c = 0

        try:
            displaytemp_f = (temp_F_sum/len(temp_F_list))
        except:
            displaytemp_f = 0
            
        # If there is an error, the DHT returns a Nonetype for humidity, so 
        # work it different than the temp reading.
        try:
            if humidity_sum < humidity*3:
                displayhum = humidity_list[-1]
            else:
                displayhum = (humidity_sum/len(humidity_list))
        except:
            displayhum = humidity_list[-1]
            
        # Sometimes the averaging results in repeating decimals, so round off.
        if type(displaytemp_f) == int or type(displaytemp_f) == float:
            displaytemp_f = round(displaytemp_f)
        if type(displaytemp_c) == int or type(displaytemp_c) == float:
            displaytemp_c = round(displaytemp_c)
        if type(displayhum) == int or type(displayhum) == float:
            displayhum = round(displayhum)
        
        # Prepare results to be returned in a list.
        results = []
        results.append(displaytemp_c)
        results.append(displaytemp_f)
        results.append(displayhum)

        # Display the results.
        print(
            "DHT reading on " + str(timeNow.strftime('%A %m/%d %H:%M %p')) +
             ": "+"Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                displaytemp_f, displaytemp_c, displayhum)
        )

        # Write the results to a .txt file.
        with open('ForecastLog.txt', 'a') as forecastLog:
                    forecastLog.write("DHT reading on " +
                     str(timeNow.strftime('%A %m/%d %H:%M %p')) +": " +
                      "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                displaytemp_f, displaytemp_c, displayhum)+"\n")
                        
                        
        # Write the results to the SQL database.
        
        path = os.path.dirname(os.path.abspath(__file__))
        db = os.path.join(path, 'dht.db')
        
        conn = sqlite3.connect(db)
        c = conn.cursor()
        
        # Only run this the first time to create the table.
        '''c.execute("""CREATE TABLE dht (
                    day_of_week text,
                    date text,
                    time text,
                    celsius int,
                    fahrenheit int,
                    humidity int
                    )""")'''
                    
        c.execute("INSERT INTO dht VALUES (?,?,?,?,?,?)",
                    (timeNow.strftime('%A'),
                    timeNow.strftime('%m/%d'),
                    timeNow.strftime('%H:%M %p'),
                     results[0], results[1], results[2]))
        
        conn.commit()
        conn.close()
        
        # Write the results to a .xlsx file.  This takes several seconds.
        '''print('writing to xlsx file')
        wb = openpyxl.load_workbook('dhtdata.xlsx')
        ws = wb.active

        row = [[str(timeNow.strftime('%m/%d %H:%M')), displaytemp_f, displayhum]]

        for data in row:
            if displaytemp_f == 0:
                pass
            else:
                ws.append(data)

        wb.save('dhtdata.xlsx')'''
        # close out the DHT properly. If you get an error that interrupts
        # the program before this gets to run, you may need to restart power
        # to the sensor for it to work properly.
        dhtDevice.exit()
        
        # Check if all 3 measurements failed. If so, the module runs again,
        # up to 5 times. If you get multiple failed readings, replace sensor.
        # Finally, return the results.    
        if type(displayhum) == int or type(displayhum) == float:
            
            return results
        
        else:

            try_counter += 1
            print(f'Reading failed, attempt {try_counter} initiated.')
            if try_counter < 5:
                dhtRun()

            else:
                return results


            
            #data = dht()
            #print(f'data from dhtbrain: {data}')
        
    else:
        print('not on the 15')
    
    # Upload the newest version to Google Drive
    #dhtUpload()
    
    
def lightcycle():
    
    path = os.path.dirname(os.path.abspath(__file__))
    db = os.path.join(path, 'gb_config.db')
    
    conn = sqlite3.connect(db)
    c = conn.cursor()

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
    c.execute("SELECT lights_status FROM gb")
    light_status = c.fetchone()[0]
    c.execute("SELECT lights_manual FROM gb")
    lights_manual = c.fetchone()[0]

    on_time = lights_on_hour + (lights_on_minute/60)
    on_time_display = str(lights_on_hour) + ':' + str(lights_on_minute)
    
    off_time = lights_off_hour + (lights_off_minute/60)
    off_time_display = str(lights_off_hour) + ':' + str(lights_off_minute)
    
    hour_now = int(timeNow.strftime('%H'))
    minute_now = int(timeNow.strftime('%M'))
    
    time_now = hour_now + (minute_now/60)
    time_now_display = str(hour_now) + ':' + str(minute_now)

    print(f"lightcycle() called at: {time_now_display}")
    
    # time must be expressed in military to do the math
    
        
    if time_now == on_time:
        
        # turn lights on  
        GPIO.output(lights, False)
        
        # set light_status to on
        c.execute("UPDATE gb SET lights_status = ?", (1,))
        
        conn.commit()
        conn.close()
        
        print("Light Status changed to: On")
        print(f"time_now: {time_now_display}")
        print(f"on_time: {on_time_display}")
        
    if not lights_manual:
                  
        if time_now == off_time:
            
            # turn lights off
            GPIO.output(lights, True)
            
            # set light_status to off
            c.execute("UPDATE gb SET lights_status = ?", (0,))

            conn.commit()
            conn.close()
            
            print("Light Status changed to: Off")
            print(f"time_now: {time_now_display}")
            print(f"off_time: {off_time_display}")
            

def watercycle():
    
    path = os.path.dirname(os.path.abspath(__file__))
    db = os.path.join(path, 'gb_config.db')
    
    conn = sqlite3.connect(db)
    c = conn.cursor()
    
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

temphumcheck()
lightcycle()
watercycle()
