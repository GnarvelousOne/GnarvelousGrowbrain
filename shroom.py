#import tkinter as tk
from tkinter import *
import ttkbootstrap as ttk
import RPi.GPIO as GPIO
import time
import datetime
import sqlite3

import board
import adafruit_dht

# window
window = ttk.Window(themename = 'superhero')
window.title("Shroom Module")
window.geometry('575x300')


# style

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


# fonts
label_font = "Roboto 10"

'''
def status_var_update(text):
	
	# make sure this is updating each time
	timeNow = datetime.datetime.now().strftime("%m/%d/%y %H:%m")

	current_status = status_var.get()
	
	if len(current_status) < 300:
		status_update = current_status+"\n"+f"{text}:"+"\n"+f"{timeNow}"
		status_var.set(status_update)
		
	else:
		status_var.set("Status:")
	'''


def save_inputs_bind(events):
	save_inputs()


def save_inputs():
	
	timeNow = datetime.datetime.now().strftime("%m/%d/%y %H:%m")
	
	# Update database values
	
	# Write the results to the SQL database.
	conn = sqlite3.connect("gb_config.db")
	
	c = conn.cursor()


	### Controls ###
	# blue rope light
		# fruiting: 12 hrs/day
		# manual on/off
		# lights_on, lights_off 
	# humidifier
		# Fruiting: 80 - 95%
		# humidity_on, off
		# set an alert if using standalone unit
	# A/C
		# Colonization: 68 - 75 deg
		# Fruiting: 50 - 77 deg
	# intake fans
		# manual on/off
		# scheduled, and periodical options?
	# c02 monitoring and exhaust
		# if able to find sensor
		# turn exhaust fan on if level exceeds
	# spore exhaust fan
		# manual on/off
	# circulation fans
		# manual on/off
		# scheduled, and periodical options?
	# vapor pressure deficit
		# calculate and display


	# Only run this if you need to create the table.
	c.execute("""CREATE TABLE db (
				lights_on_hour int,
				lights_on_minute int,
				lights_off_hour int,
				lights_off_minute int,
				lights_manual int,
				light_status int,
				humidifer_manual int,
				humidifier_status int,
				circfan_manual int,
				circfan_status int,
				intake_manual int,
				intake_status int,
				exhaust_manual int,
				exhaust_status int
				)""")
				
				
	w_dict = {
		'lights_on_hour':lights_on_hour_var, 
		'lights_on_minute':lights_on_minute_var,
		'lights_off_hour':lights_off_hour_var, 
		'lights_off_minute':lights_off_minute_var,
		'lights_manual':lights_manual_var,
		'light_status':light_status_var,
		'humidifier_manual':humidifier_manual_var,
		'humidifier_status':humidifier_status_var,
		'circfan_manual':circfan_manual_var,
		'circfan_status':circfan_status_var,
		'intake_manual':intake_manual_var,
		'intake_status':intake_status_var,
		'exhaust_manual':exhaust_manual_var,
		'exhaust_status':exhaust_status_var
		}

	for i,j in w_dict.items():
		if len(j.get()) > 0:
			c.execute("UPDATE gb SET {} = ?".format(i), (j.get(),))
				
				 
	conn.commit()
	conn.close()
	
	status_var.set(f"Status:\n Settings saved\n{timeNow}")


def manual(device, var):
	
	timeNow = datetime.datetime.now().strftime("%m/%d/%y %H:%m")
	
	title = device.title()
	
	if var == 1:
		lights_manual.config(text = f'{title} - ON')
		lights_manual.update()
	else:
		lights_manual.config(text = f'{title} - OFF')
		lights_manual.update()
	
	#print(device)
	#print(bool_state)
	
	if device == 'lights':
		pin = 5
	
	if var:
		status_text = 'ON'
	else:
		status_text = 'OFF'	
	
	not_var = not var
	sql_manual = f"{device}_manual"
	sql_status = f"{device}_status"
	
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)
	
	# change state of GPIO pin  
	GPIO.output(pin, not_var)
		
	# Write the results to the SQL database.
	conn = sqlite3.connect("gb_config.db")
	c = conn.cursor()
	
	c.execute("UPDATE gb SET {} = ?".format(sql_manual), (var,))
	c.execute("UPDATE gb SET {} = ?".format(sql_status), (var,))
	
	conn.commit()
	conn.close()
	
	status_var.set(f"Status:\n Device turned {status_text} manually\n{timeNow}")
	
	
def reset():
	
	timeNow = datetime.datetime.now().strftime("%m/%d/%y %H:%m")
	
	lights_on_hour_var.set()
	lights_on_minute_var.set()
	lights_off_hour_var.set()
	lights_off_minute_var.set()
	
	status_var.set(f"Status:\n Input fields reset\n{timeNow}")
	

def clear():
	pass


def zero():
	print(keypad0_input.get())


# bind keystrokes
window.bind('<Return>', save_inputs_bind)

# define the grid
window.columnconfigure(0, weight = 2, uniform = 'a')
window.columnconfigure(1, weight = 2, uniform = 'a')
window.columnconfigure(2, weight = 2, uniform = 'a')
window.columnconfigure(3, weight = 2, uniform = 'a')
window.columnconfigure(4, weight = 2, uniform = 'a')
window.columnconfigure(5, weight = 2, uniform = 'a')
window.columnconfigure(6, weight = 2, uniform = 'a')
window.columnconfigure(7, weight = 2, uniform = 'a')
window.rowconfigure(0, weight = 2, uniform = 'a')
window.rowconfigure(1, weight = 2, uniform = 'a')
window.rowconfigure(2, weight = 2, uniform = 'a')
window.rowconfigure(3, weight = 2, uniform = 'a')
window.rowconfigure(4, weight = 2, uniform = 'a')

# widgets


status_var = ttk.StringVar()
status_var.set('Status')

status = ttk.Label(window, text = 'Status', font = label_font, textvariable = status_var, bootstyle = 'success')
manual_on = ttk.Button(window, text='ON', command = lambda:manual('lights', 1), bootstyle = 'secondary', style = 'secondary.TButton')
manual_off = ttk.Button(window, text='OFF', command = lambda:manual('lights', 0), bootstyle = 'secondary', style = 'secondary.TButton')
save = ttk.Button(window, text='SAVE', command = save_inputs, bootstyle = 'success', style = 'success.TButton')
resetb = ttk.Button(window, text='RESET', command = reset, bootstyle = 'warning', style = 'warning.TButton')
adios = ttk.Button(window, text='EXIT', command = exit, bootstyle = 'danger', style = 'danger.TButton')




label1 = ttk.Label(window, text = 'ON\nHour:', font = label_font, bootstyle = 'warning')
label2 = ttk.Label(window, text = 'ON\nMinute:', font = label_font, bootstyle = 'warning')
label3 = ttk.Label(window, text = 'OFF\nHour:', font = label_font, bootstyle = 'warning')
label4 = ttk.Label(window, text = 'OFF\nMinute:', font = label_font, bootstyle = 'warning')


lights_on_hour_var = ttk.IntVar()
lights_on_minute_var = ttk.IntVar()
lights_off_hour_var = ttk.IntVar()
lights_off_minute_var = ttk.IntVar()
lights_manual_var = ttk.IntVar()
light_status_var = ttk.IntVar()
humidifier_manual_var = ttk.IntVar()
humidifier_status_var = ttk.IntVar()
circfan_manual_var = ttk.IntVar()
circfan_status_var = ttk.IntVar()
intake_manual_var = ttk.IntVar()
intake_status_var = ttk.IntVar()
exhaust_manual_var = ttk.IntVar()
exhaust_status_var = ttk.IntVar()


lights_manual = ttk.Checkbutton(window, text = "Lights - OFF", command = lambda:manual('lights', lights_manual_var), variable= lights_manual_var, onvalue = 1, offvalue = 0, bootstyle = 'primary, round-toggle')

lights_on_hour = ttk.Entry(window, textvariable = lights_on_hour_var, bootstyle = 'warning')
lights_on_minute = ttk.Entry(window, textvariable = lights_on_minute_var, bootstyle = 'warning')
lights_off_hour = ttk.Entry(window, textvariable = lights_off_hour_var, bootstyle = 'warning')
lights_off_minute = ttk.Entry(window, textvariable = lights_off_minute_var, bootstyle = 'warning')

# Set Focus
lights_on_hour.focus_set()

keypad9_input = ttk.IntVar(value = 9)
keypad9 = ttk.Button(window, textvariable = keypad9_input, text = '9', style = 'primary.TButton')

keypad8_input = ttk.IntVar(value = 8)
keypad8 = ttk.Button(window, textvariable = keypad8_input, text = '8', style = 'primary.TButton')

keypad7_input = ttk.IntVar(value = 7)
keypad7 = ttk.Button(window, textvariable = keypad7_input, text = '7', style = 'primary.TButton')

keypad6_input = ttk.IntVar(value = 6)
keypad6 = ttk.Button(window, textvariable = keypad6_input, text = '6', style = 'primary.TButton')

keypad5_input = ttk.IntVar(value = 5)
keypad5 = ttk.Button(window, textvariable = keypad5_input, text = '5', style = 'primary.TButton')

keypad4_input = ttk.IntVar(value = 4)
keypad4 = ttk.Button(window, textvariable = keypad4_input, text = '4', style = 'primary.TButton')

keypad3_input = ttk.IntVar(value = 3)
keypad3 = ttk.Button(window, textvariable = keypad3_input, text = '3', style = 'primary.TButton')

keypad2_input = ttk.IntVar(value = 2)
keypad2 = ttk.Button(window, textvariable = keypad2_input, text = '2', style = 'primary.TButton')

keypad1_input = ttk.IntVar(value = 1)
keypad1 = ttk.Button(window, textvariable = keypad1_input, text = '1', style = 'primary.TButton')

keypad0_input = ttk.IntVar(value = 0)
keypad0 = ttk.Button(window, textvariable = keypad0_input, text = '0', command = zero, style = 'primary.TButton')

#keypad_clear_input = tk.IntVar(value = )
keypad_clear = ttk.Button(window, text = 'CE', command = clear, style = 'primary.TButton')

keypad_sticky = 'nsew'
label_sticky = 'sw'
entry_sticky = 'w'
label_entry_padx = 2
keypad_padding = 2

# layout

status.grid(row = 4, column = 0, columnspan = 3, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
manual_on.grid(row = 4, column = 3, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
manual_off.grid(row = 4, column = 4, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
save.grid(row = 4, column = 5, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
resetb.grid(row = 4, column = 6, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
adios.grid(row = 4, column = 7, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)



label1.grid(row = 0, column = 3, sticky = label_sticky, padx = label_entry_padx)
label2.grid(row = 0, column = 4, sticky = label_sticky, padx = label_entry_padx)
label3.grid(row = 2, column = 3, sticky = label_sticky, padx = label_entry_padx)
label4.grid(row = 2, column = 4, sticky = label_sticky, padx = label_entry_padx)

lights_manual.grid(row = 0, column = 0, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)

lights_on_hour.grid(row = 1, column = 3, sticky = entry_sticky, padx = label_entry_padx)
lights_on_minute.grid(row = 1, column = 4, sticky = entry_sticky, padx = label_entry_padx)
lights_off_hour.grid(row = 3, column = 3, sticky = entry_sticky, padx = label_entry_padx)
lights_off_minute.grid(row = 3, column = 4, sticky = entry_sticky, padx = label_entry_padx)


keypad9.grid(row = 0, column = 7, sticky = keypad_sticky, padx = keypad_padding, pady = keypad_padding)
keypad8.grid(row = 0, column = 6, sticky = keypad_sticky, padx = keypad_padding, pady = keypad_padding)
keypad7.grid(row = 0, column = 5, sticky = keypad_sticky, padx = keypad_padding, pady = keypad_padding)
keypad6.grid(row = 1, column = 7, sticky = keypad_sticky, padx = keypad_padding, pady = keypad_padding)
keypad5.grid(row = 1, column = 6, sticky = keypad_sticky, padx = keypad_padding, pady = keypad_padding)
keypad4.grid(row = 1, column = 5, sticky = keypad_sticky, padx = keypad_padding, pady = keypad_padding)
keypad3.grid(row = 2, column = 7, sticky = keypad_sticky, padx = keypad_padding, pady = keypad_padding)
keypad2.grid(row = 2, column = 6, sticky = keypad_sticky, padx = keypad_padding, pady = keypad_padding)
keypad1.grid(row = 2, column = 5, sticky = keypad_sticky, padx = keypad_padding, pady = keypad_padding)
keypad0.grid(row = 3, column = 6, columnspan = 2, sticky = keypad_sticky, padx = keypad_padding, pady = keypad_padding)
keypad_clear.grid(row = 3, column = 5, sticky = keypad_sticky, padx = keypad_padding, pady = keypad_padding)



# run
window.mainloop()
