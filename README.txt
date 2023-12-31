﻿The Gnarvelous Growbrain (GG) – open source farm automation to build the commons


Cast of Characters:
(files such as credentials, tokens, pickles from google are not included, you will have to generate them yourself)

dhtbrain.py – this is the main program which calls dht.py and quickstart.py.

dht.py – takes temperature and humidity measurements, writes them to the logs, and sends alert emails if measurements are outside the desired range.

dhtdata.xlsx – spreadsheet that collects the temp and hum data. Can be uploaded to Google Drive through quickstart.py. * Currently not using due to very slow write times.

dht.db - a SQLite database that replaces dhtdata.xlsx. Perfoms the same recording of temperature, humidity and timestamp.

sprinkleron.py & sprinkleroff.py – examples of controlling the 5v DC relays to turn things on and off.  They are separated into and on and off scripts so that they may be scheduled through the crontab without having to use over complicated python scripts or by using time.sleep() to put the computer to sleep for extended periods.

forecastbrain.py – web scrapes accuweather.com for local 7 day forecast and sends the user an email periodically. Scheduled through crontab.

quickstart.py – uploads dhtdata.xlsx to a google drive folder for cloud access. Requires the Rpi to run in X due to having to open a web browser for authentication.

alerts.py – sends alert emails if the temp or hum is outside of desired range.  ** Merged this directly into dht.py so that the email can easily send the actual temperature readings without having pull them across scripts.

reboot.py – reboots the Rpi periodically to correct for any authentication issues that can arise occasionally during quickstart.py and the google drive authentication process.  If certain errors occur during temperature readings or while the user is modifying and debugging code, it can cause authentication errors until the Rpi is rebooted.

ForecastLog.txt – txt file that receives forecast and temp hum data.  May be obsolete as the cron.log collects the same data as long as it is printed to the terminal and the program is run through a cron job.

cron.log – logs output and errors from each cron scheduled task.



The Rpi is setup to automatically log in to the X gui upon boot.  This ensures that in a power failure, the Rpi will start back up automatically and that quickstart.py will work properly as it needs to open a web browser.  It also allows the user to simply unplug the device if anything is not working properly, plug it back in, and it will start over fresh.

The GG uses the crontab to schedule all jobs.  This prevents the need from writing a python script to do the scheduling which would need to be running continuously.  The crontab also conviently provides its own log, and runs automatically as long as the Rpi is powered on.  An incredibly powerful tool that is easy to get the hang of.  You can disable scheduling by simply commenting out a job with a '#' in the front of a line.  For example, if you have reboot.py set to run periodically, you don't want it to run if you are the middle of adding new code to a script.

The GG can run headless or with a number of displays – HDMI, LCD, Touchscreens, etc.  Remote access can be done through SSH.

The GG can control 5v DC relays to turn on and off mains power to anything running on 120 AC voltage.  This means you can control lights, pumps, fans, humidifiers, etc., based on any programmable data point.  Your lights can turn on every day at 6 AM, or whenever Britney Spears tweets the word “y’all”.  It is completely up to you.

A simple DHT temperature and humidity sensor is used to record data, which can then either be simply stored for analysis or can be used as the trigger to activate a 5v DC relay.

Common USB webcams can be used to visually monitor your garden.

The Rpi can work with or without internet access.  It is even concievable to power it temporarily with cell-phone charger batteries in the event you have no electricity available.

The Rpi itself is a full functioning Linux based computer.  It has a web browser, office productivity software, VLC media player, python editors, and more.  It can charge your cell phone.  You can install video game emulators.  You can stream Spotify songs through it.  The incredible potentiality combined with everything being open-source and in your control means the GG can truly be as unique as each individual using it.  There is not much limit to what you do with it, except perhaps for the limited computing power.


Hardware:

The main piece of hardware is the Raspberry Pi.  It is also conceivable that other microcontrollers could be used, such as the Arduino.  The key to using these microcontrollers is the GPIO pins which allow the Rpi to receive data input and then send control output.

The main input source is the DHT11 or DHT22 temperature and humidity sensor. Additional sensors could include soil moisture testers to control when water should be given to the crops, or a light sensor to control turning on and off of lights.

Webcams can be attached via the USB ports.

A useful accessory is a powered USB hub which can sit outside the enclosure. This allows for charging cellphones, using thumbdrives, attaching old playstation controllers to play emulator games, etc. 

USB Wireless keyboards work well and reduce cable clutter.

USB Wifi dongle is essential to connect the Rpi to the internet.

An HDMI output can connect a display such as a 5” touchscreen or even a large TV or regular computer monitor.  You can also use something as simple as a 2 or 4 line LCD display.  Or you can use a laptop to connect to the Rpi through SSH.

Audio can be sent out via the 3.5mm (1/8”) headphone jack, or through HDMI if connecting to a TV monitor with internal speakers.

The GPIO pins can also connect to 5V DC relay switches, which themselves connect to standard 3-prong 120V outlets.  You must also supply mains voltage to these relays.  Keep in mind the more outlets you use at once will increase the load on the wires, the same as when using a power strip, so there is a limit to how much voltage can run through any single system.  For large applications you may need to use more than one circuit breaker or consider a dedicated 50 amp 240V line which can then be broken down into separate 15 or 20 amp 120V lines. 


Software Configuration

Python 3
- Comes preinstalled with the Rpi. You should have a good understanding of Python, but you only need a basic understanding to get things started.  An additional benefit of the GG is that by using it you will naturally gain proficiency in programming.  There is no limit to what you can do as you modify the GG to fit your specific farming needs 

raspi-config – access through “sudo raspi-config” at the terminal
-set automatic login and boot to X

crontab – access through “crontab -e” at the terminal
- crontab.guru is an excellent website to help determine how to schedule things the way you want.
- the key elements are the five “* * * * *” which determine when the programs will run.  It is very important that you do not schedule multiple programs to run at the same time, rather, you should space them out by at least a minute or however long it takes for each one to finish.  
- the second part is the path to the file that you want to run.
- the third part pipes the output of that program to cron.log so you can debug and verify things are working.

Google developer account
- if you want to upload files to a Google Drive, you will need to create a developer account through Google and follow the steps online.  You will receive token files which must be saved in the working directory.  There are many sources and tutorials online to get this done.

Emailing data and alerts
- ezgmail is the Python module needed to do this.  Once installed it is very simple to use.  Follow the steps online for Google Gmail in the same way you set up access for Drive.

