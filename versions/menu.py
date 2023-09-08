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
spinbox_font = "Roboto 8"

# Add Label to display most recent dht reading from dht.db
# Add shroom.py

'''
def run_water():
	os.system('python water.py')
	
def run_lights():
	os.system('python lights.py')

def run_shroom():
	pass
'''

def run_status():
	timeNow = datetime.datetime.now().strftime("%m/%d/%y %H:%m")
	conn = sqlite3.connect("dht.db")
	
	c = conn.cursor()	
	
	query = c.execute("SELECT * FROM dht").fetchall()[-1]
    
    update = f"Last Reading: {query[0]}, {query[1]} {query[2]}:  {query[4]} F / {query[5]}% rH"
    
    status_var.set(update)
    
    print(query)
    print(status_var.get())
    
    conn.commit()
    conn.close()
	
	
def start():
	
	conn = sqlite3.connect("gb_config.db")
	
	c = conn.cursor()
	
	# Only run this if you need to create the table.
	'''
	c.execute("""CREATE TABLE menu (
					widget_string_1 str,
					widget_string_2 str,
					widget_string_3 str,
					widget_string_4 str,
					widget_string_5 str,
					widget_string_6 str,
					widget_string_7 str,
					widget_string_8 str,
					widget_string_9 str,
					output_string_1 str,
					output_string_2 str,
					output_string_3 str,
					output_string_4 str,
					output_string_5 str,
					output_string_6 str,
					output_string_7 str,
					output_string_8 str,
					output_string_9 str								
				)""")'''

	w_dict = {
		'widget_string_1':widget_string_1,
		'widget_string_2':widget_string_2,
		'widget_string_3':widget_string_3,
		'widget_string_4':widget_string_4,
		'widget_string_5':widget_string_5,
		'widget_string_6':widget_string_6,
		'widget_string_7':widget_string_7,
		'widget_string_8':widget_string_8,
		'widget_string_9':widget_string_9,
		'output_string_1':output_string_1,
		'output_string_2':output_string_2,
		'output_string_3':output_string_3,
		'output_string_4':output_string_4,
		'output_string_5':output_string_5,
		'output_string_6':output_string_6,
		'output_string_7':output_string_7,
		'output_string_8':output_string_8,
		'output_string_9':output_string_9
		}
	

	for i,j in w_dict.items():
		if len(j.get()) > 0:
			c.execute("UPDATE menu SET {} = ?".format(i), (j.get(),))
			print(f'updated {i} {j.get()}')
				
				 
	conn.commit()
	conn.close()
	
	'''
	# Get values of all variables
	m_dict = {}
	for i in range(1,9):
		ws = f'widget_string_{i}'
		os = f'output_string{i}'
		m_dict[ws] = os
		
	
	menu_dict = {}
	print(len(menu_dict))
	menu_dict[widget_string_1.get()] = output_string_1.get()
	print(menu_dict)
	menu_dict[widget_string_2.get()] = output_string_2.get()
	print(menu_dict)
	menu_dict[widget_string_3.get()] = output_string_3.get()
	print(menu_dict)
	menu_dict[widget_string_4.get()] = output_string_4.get()
	print(menu_dict)
	menu_dict[widget_string_5.get()] = output_string_5.get()
	print(menu_dict)
	menu_dict[widget_string_6.get()] = output_string_6.get()
	print(menu_dict)
	menu_dict[widget_string_7.get()] = output_string_7.get()
	print(menu_dict)
	menu_dict[widget_string_8.get()] = output_string_8.get()
	print(menu_dict)
	menu_dict[widget_string_9.get()] = output_string_9.get()
	print(len(menu_dict))
	
	#print(menu_dict)
	# What needs to be sent to widget frame?
	# Call the widget frame and pass the variables
	
	pass
	'''
	
# define the grid
window.columnconfigure(0, weight = 2, uniform = 'a')
window.columnconfigure(1, weight = 2, uniform = 'a')
window.columnconfigure(2, weight = 2, uniform = 'a')
window.columnconfigure(3, weight = 2, uniform = 'a')
window.columnconfigure(4, weight = 2, uniform = 'a')
window.columnconfigure(5, weight = 2, uniform = 'a')
window.columnconfigure(6, weight = 2, uniform = 'a')
window.columnconfigure(7, weight = 2, uniform = 'a')
window.columnconfigure(8, weight = 2, uniform = 'a')


window.rowconfigure(0, weight = 2, uniform = 'a')
window.rowconfigure(1, weight = 2, uniform = 'a')
window.rowconfigure(2, weight = 2, uniform = 'a')
window.rowconfigure(3, weight = 2, uniform = 'a')
window.rowconfigure(4, weight = 2, uniform = 'a')
window.rowconfigure(5, weight = 2, uniform = 'a')
window.rowconfigure(6, weight = 2, uniform = 'a')
window.rowconfigure(7, weight = 2, uniform = 'a')


# widgets

status_var = ttk.StringVar()
status_var.set('Status')

status_button = ttk.Button(window, textvariable=status_var, command=run_status, bootstyle = 'light', style = 'light.TButton')


items = ('OFF','Lights', 'Water', 'Shroom', 'Intake Fan', 'Exhaust Fan', 'Humidifier', 'Circulation')
# (5, 6, 13, 19, 26, 16, 20, 21)
output = ('', '1', '2', '3', '4', '5', '6', '7', '8')

widget_string_1 = ttk.StringVar(value = items[0])
widget_string_2 = ttk.StringVar(value = items[0])
widget_string_3 = ttk.StringVar(value = items[0])
widget_string_4 = ttk.StringVar(value = items[0])
widget_string_5 = ttk.StringVar(value = items[0])
widget_string_6 = ttk.StringVar(value = items[0])
widget_string_7 = ttk.StringVar(value = items[0])
widget_string_8 = ttk.StringVar(value = items[0])
widget_string_9 = ttk.StringVar(value = items[0])

output_string_1 = ttk.StringVar(value = output[0])
output_string_2 = ttk.StringVar(value = output[0])
output_string_3 = ttk.StringVar(value = output[0])
output_string_4 = ttk.StringVar(value = output[0])
output_string_5 = ttk.StringVar(value = output[0])
output_string_6 = ttk.StringVar(value = output[0])
output_string_7 = ttk.StringVar(value = output[0])
output_string_8 = ttk.StringVar(value = output[0])
output_string_9 = ttk.StringVar(value = output[0])

mod_1 = ttk.Spinbox(window, wrap = True, textvariable = widget_string_1, command = lambda: print(widget_string_1.get()), bootstyle = 'info', font = spinbox_font )
mod_1['values'] = items

mod_2 = ttk.Spinbox(window, wrap = True, textvariable = widget_string_2, command = lambda: print(widget_string_2.get()), bootstyle = 'info', font = spinbox_font )
mod_2['values'] = items

mod_3 = ttk.Spinbox(window, wrap = True, textvariable = widget_string_3, command = lambda: print(widget_string_3.get()), bootstyle = 'info', font = spinbox_font )
mod_3['values'] = items

mod_4 = ttk.Spinbox(window, wrap = True, textvariable = widget_string_4, command = lambda: print(widget_string_4.get()), bootstyle = 'info', font = spinbox_font)
mod_4['values'] = items

mod_5 = ttk.Spinbox(window, wrap = True, textvariable = widget_string_5, command = lambda: print(widget_string_5.get()), bootstyle = 'info', font = spinbox_font)
mod_5['values'] = items

mod_6 = ttk.Spinbox(window, wrap = True, textvariable = widget_string_6, command = lambda: print(widget_string_6.get()), bootstyle = 'info', font = spinbox_font)
mod_6['values'] = items

mod_7 = ttk.Spinbox(window, wrap = True, textvariable = widget_string_7, command = lambda: print(widget_string_7.get()), bootstyle = 'info', font = spinbox_font)
mod_7['values'] = items

mod_8 = ttk.Spinbox(window, wrap = True, textvariable = widget_string_8, command = lambda: print(widget_string_8.get()), bootstyle = 'info', font = spinbox_font)
mod_8['values'] = items

mod_9 = ttk.Spinbox(window, wrap = True, textvariable = widget_string_9, command = lambda: print(widget_string_9.get()), bootstyle = 'info', font = spinbox_font)
mod_9['values'] = items


output_1 = ttk.Spinbox(window, wrap = True, textvariable = output_string_1, command = lambda: print(output_string_1.get()), bootstyle = 'info', font = spinbox_font)
output_1['values'] = output

output_2 = ttk.Spinbox(window, wrap = True, textvariable = output_string_2, command = lambda: print(output_string_2.get()), bootstyle = 'info', font = spinbox_font)
output_2['values'] = output

output_3 = ttk.Spinbox(window, wrap = True, textvariable = output_string_3, command = lambda: print(output_string_3.get()), bootstyle = 'info', font = spinbox_font)
output_3['values'] = output

output_4 = ttk.Spinbox(window, wrap = True, textvariable = output_string_4, command = lambda: print(output_string_4.get()), bootstyle = 'info', font = spinbox_font)
output_4['values'] = output

output_5 = ttk.Spinbox(window, wrap = True, textvariable = output_string_5, command = lambda: print(output_string_5.get()), bootstyle = 'info', font = spinbox_font)
output_5['values'] = output

output_6 = ttk.Spinbox(window, wrap = True, textvariable = output_string_6, command = lambda: print(output_string_6.get()), bootstyle = 'info', font = spinbox_font)
output_6['values'] = output

output_7 = ttk.Spinbox(window, wrap = True, textvariable = output_string_7, command = lambda: print(output_string_7.get()), bootstyle = 'info', font = spinbox_font)
output_7['values'] = output

output_8 = ttk.Spinbox(window, wrap = True, textvariable = output_string_8, command = lambda: print(output_string_8.get()), bootstyle = 'info', font = spinbox_font)
output_8['values'] = output

output_9 = ttk.Spinbox(window, wrap = True, textvariable = output_string_9, command = lambda: print(output_string_9.get()), bootstyle = 'info', font = spinbox_font)
output_9['values'] = output


mod_1_label = ttk.Label(window, text = 'Module 1', font = label_font, bootstyle = 'info')
mod_2_label = ttk.Label(window, text = 'Module 2', font = label_font, bootstyle = 'info')
mod_3_label = ttk.Label(window, text = 'Module 3', font = label_font, bootstyle = 'info')
mod_4_label = ttk.Label(window, text = 'Module 4', font = label_font, bootstyle = 'info')
mod_5_label = ttk.Label(window, text = 'Module 5', font = label_font, bootstyle = 'info')
mod_6_label = ttk.Label(window, text = 'Module 6', font = label_font, bootstyle = 'info')
mod_7_label = ttk.Label(window, text = 'Module 7', font = label_font, bootstyle = 'info')
mod_8_label = ttk.Label(window, text = 'Module 8', font = label_font, bootstyle = 'info')
mod_9_label = ttk.Label(window, text = 'Module 9', font = label_font, bootstyle = 'info')


#water_button = ttk.Button(window, text='Water Module', command=run_water, bootstyle = 'info', style = 'info.TButton')
#lights_button = ttk.Button(window, text='Lights Module', command=run_lights, bootstyle = 'warning', style = 'warning.TButton')
#shroom_button = ttk.Button(window, text='Shroom Module', command=run_shroom, bootstyle = 'secondary', style = 'secondary.TButton')
start = ttk.Button(window, text='START', command=start, bootstyle = 'success', style = 'success.TButton')
adios = ttk.Button(window, text='EXIT', command=exit, bootstyle = 'danger', style = 'danger.TButton')


# layout
button_sticky = 'nsew'
label_sticky = 'sw'
entry_sticky = 'w'
button_pad = 2
label_entry_padx = 2

status_button.grid(row = 0, column = 0, columnspan = 9, sticky = 'nsew', padx = button_pad, pady = button_pad)

mod_1_label.grid(row = 1, column = 0, columnspan = 3, sticky = label_sticky, padx = label_entry_padx)
mod_2_label.grid(row = 1, column = 3, columnspan = 3, sticky = label_sticky, padx = label_entry_padx)
mod_3_label.grid(row = 1, column = 6, columnspan = 3, sticky = label_sticky, padx = label_entry_padx)
mod_4_label.grid(row = 3, column = 0, columnspan = 3, sticky = label_sticky, padx = label_entry_padx)
mod_5_label.grid(row = 3, column = 3, columnspan = 3, sticky = label_sticky, padx = label_entry_padx)
mod_6_label.grid(row = 3, column = 6, columnspan = 3, sticky = label_sticky, padx = label_entry_padx)
mod_7_label.grid(row = 5, column = 0, columnspan = 3, sticky = label_sticky, padx = label_entry_padx)
mod_8_label.grid(row = 5, column = 3, columnspan = 3, sticky = label_sticky, padx = label_entry_padx)
mod_9_label.grid(row = 5, column = 6, columnspan = 3, sticky = label_sticky, padx = label_entry_padx)


mod_1.grid(row = 2, column = 0, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)
mod_2.grid(row = 2, column = 3, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)
mod_3.grid(row = 2, column = 6, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)
mod_4.grid(row = 4, column = 0, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)
mod_5.grid(row = 4, column = 3, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)
mod_6.grid(row = 4, column = 6, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)
mod_7.grid(row = 6, column = 0, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)
mod_8.grid(row = 6, column = 3, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)
mod_9.grid(row = 6, column = 6, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)

output_1.grid(row = 2, column = 2, sticky = entry_sticky, padx = label_entry_padx)
output_2.grid(row = 2, column = 5, sticky = entry_sticky, padx = label_entry_padx)
output_3.grid(row = 2, column = 8, sticky = entry_sticky, padx = label_entry_padx)
output_4.grid(row = 4, column = 2, sticky = entry_sticky, padx = label_entry_padx)
output_5.grid(row = 4, column = 5, sticky = entry_sticky, padx = label_entry_padx)
output_6.grid(row = 4, column = 8, sticky = entry_sticky, padx = label_entry_padx)
output_7.grid(row = 6, column = 2, sticky = entry_sticky, padx = label_entry_padx)
output_8.grid(row = 6, column = 5, sticky = entry_sticky, padx = label_entry_padx)
output_9.grid(row = 6, column = 8, sticky = entry_sticky, padx = label_entry_padx)

#water_button.grid(row = 1, column = 0, sticky = button_sticky, padx = button_pad, pady = button_pad)
#lights_button.grid(row = 1, column = 1, sticky = button_sticky, padx = button_pad, pady = button_pad)
#shroom_button.grid(row = 1, column = 2, sticky = button_sticky, padx = button_pad, pady = button_pad)
start.grid(row = 7, column = 0, columnspan = 4, sticky = 'nsew', padx = button_pad, pady = button_pad)
adios.grid(row = 7, column = 5, columnspan = 4, sticky = 'nsew', padx = button_pad, pady = button_pad)

# run
window.mainloop()
