#import tkinter as tk
from tkinter import *
import ttkbootstrap as ttk
import RPi.GPIO as GPIO
import time
import datetime
import sqlite3

import board
import adafruit_dht
import os

# window
window = ttk.Window(themename = 'darkly')
window.title("Gnarvelous Growbrain")
window.geometry('450x250')


#Style

main_font = "Roboto" 

primary_style = ttk.Style()
primary_style.configure('primary.TButton', font=(main_font, 10))

secondary_style = ttk.Style()
secondary_style.configure('secondary.TButton', font=(main_font, 10))

info_style = ttk.Style()
info_style.configure('info.TButton', font=(main_font, 10))

success_style = ttk.Style()
success_style.configure('success.TButton', font=(main_font, 10))

warning_style = ttk.Style()
warning_style.configure('warning.TButton', font=(main_font, 10))

danger_style = ttk.Style()
danger_style.configure('danger.TButton', font=(main_font, 10))

light_style = ttk.Style()
light_style.configure('light.TButton', font=(main_font, 10))


# fonts
label_font = "Roboto 10"


# Add Label to display most recent dht reading from dht.db
# Add shroom.py


def run_water():
	os.system('python water.py')
	
def run_lights():
	os.system('python lights.py')

def run_shroom():
	pass

def run_status():
	timeNow = datetime.datetime.now().strftime("%m/%d/%y %H:%m")
	conn = sqlite3.connect("dht.db")
	
	c = conn.cursor()	
	
	query = c.execute("SELECT * FROM dht").fetchall()[-1]
	
	update = f"Last Reading: {query[0]}, {query[1]} {query[2]}\n{query[4]} F / {query[5]}% rH"
	
	status_var.set(update)
	
	print(query)
	print(status_var.get())
	
	conn.commit()
	conn.close()
	
	
# define the grid
window.columnconfigure(0, weight = 2, uniform = 'a')
window.columnconfigure(1, weight = 2, uniform = 'a')
window.columnconfigure(2, weight = 2, uniform = 'a')

window.rowconfigure(0, weight = 2, uniform = 'a')
window.rowconfigure(1, weight = 2, uniform = 'a')
window.rowconfigure(2, weight = 2, uniform = 'a')

# widgets

status_var = ttk.StringVar()
status_var.set('Status')

status_button = ttk.Button(window, textvariable=status_var, command=run_status, bootstyle = 'light', style = 'light.TButton')

water_button = ttk.Button(window, text='Water Module', command=run_water, bootstyle = 'info', style = 'info.TButton')
lights_button = ttk.Button(window, text='Lights Module', command=run_lights, bootstyle = 'warning', style = 'warning.TButton')
shroom_button = ttk.Button(window, text='Shroom Module', command=run_shroom, bootstyle = 'secondary', style = 'secondary.TButton')
adios = ttk.Button(window, text='EXIT', command=exit, bootstyle = 'danger', style = 'danger.TButton')

button_sticky = 'nsew'
button_pad = 2

# layout
status_button.grid(row = 0, column = 0, columnspan = 3, sticky = 'nsew', padx = button_pad, pady = button_pad)
water_button.grid(row = 1, column = 0, sticky = button_sticky, padx = button_pad, pady = button_pad)
lights_button.grid(row = 1, column = 1, sticky = button_sticky, padx = button_pad, pady = button_pad)
shroom_button.grid(row = 1, column = 2, sticky = button_sticky, padx = button_pad, pady = button_pad)
adios.grid(row = 2, column = 0, columnspan = 3, sticky = 'nsew', padx = button_pad, pady = button_pad)

# run
window.mainloop()
