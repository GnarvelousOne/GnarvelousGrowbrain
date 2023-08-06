import tkinter as tk
import ttkbootstrap as ttk
import RPi.GPIO as GPIO
import time
import datetime
import sqlite3

# window
window = ttk.Window(themename = 'darkly')
window.title("Light Module")
window.geometry('575x300')


def save_inputs_bind(events):
	save_inputs()

def save_inputs():
	
	# Update database values
	
	# Write the results to the SQL database.
	conn = sqlite3.connect("gb_config.db")
	
	c = conn.cursor()
	
	# Only run this the first time to create the table.
	
	'''c.execute("""CREATE TABLE gb (
				lights_on_hour int,
				lights_on_minute int,
				lights_off_hour int,
				lights_off_minute int,
				light_status int,
				water_on_hour int,
				water_on_minute int,
				water_off_hour int,
				water_off_minute int,
				water_status int
				
				)""")'''

	w_dict = {
		'lights_on_hour':lights_on_hour_var, 
		'lights_on_minute':lights_on_minute_var,
		'lights_off_hour':lights_off_hour_var, 
		'lights_off_minute':lights_off_minute_var
		}

	for i,j in w_dict.items():
		if len(j.get()) > 0:
			c.execute("UPDATE gb SET {} = ?".format(i), (j.get(),))
				
				 
	conn.commit()
	conn.close()

	
def reset():
	
	lights_on_hour_var.set('')
	lights_on_minute_var.set('')
	lights_off_hour_var.set('')
	lights_off_minute_var.set('')
	water_on_hour_var.set('')
	water_on_minute_var.set('')
	water_off_hour_var.set('')
	water_off_minute_var.set('')

def clear():
	pass


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


status_var = tk.StringVar()
status_var.set('Status')

status = ttk.Label(window, text = 'Status', textvariable = status_var)

save = ttk.Button(window,
	text='SAVE', 
	command=save_inputs,
	bootstyle = 'success'
	)

resetb = ttk.Button(window, 
	text='RESET', 
	command=reset,
	bootstyle = 'warning'
	)

adios = ttk.Button(window,
	text='EXIT', 
	command=exit,
	bootstyle = 'danger'
	)

label1 = ttk.Label(window, text = 'Lights ON\nHour:')
label2 = ttk.Label(window, text = 'Lights ON\nMinute:')
label3 = ttk.Label(window, text = 'Lights OFF\nHour:')
label4 = ttk.Label(window, text = 'Lights OFF\nMinute:')


lights_on_hour_var = tk.StringVar()
lights_on_minute_var = tk.StringVar()
lights_off_hour_var = tk.StringVar()
lights_off_minute_var = tk.StringVar()

lights_on_hour = ttk.Entry(window, textvariable = lights_on_hour_var)
lights_on_minute = ttk.Entry(window, textvariable = lights_on_minute_var)
lights_off_hour = ttk.Entry(window, textvariable = lights_off_hour_var)
lights_off_minute = ttk.Entry(window, textvariable = lights_off_minute_var)


keypad9_input = tk.IntVar(value = 9)
keypad9 = ttk.Button(window, textvariable = keypad9_input, text = '9')

keypad8_input = tk.IntVar(value = 8)
keypad8 = ttk.Button(window, textvariable = keypad8_input, text = '8')

keypad7_input = tk.IntVar(value = 7)
keypad7 = ttk.Button(window, textvariable = keypad7_input, text = '7')

keypad6_input = tk.IntVar(value = 6)
keypad6 = ttk.Button(window, textvariable = keypad6_input, text = '6')

keypad5_input = tk.IntVar(value = 5)
keypad5 = ttk.Button(window, textvariable = keypad5_input, text = '5')

keypad4_input = tk.IntVar(value = 4)
keypad4 = ttk.Button(window, textvariable = keypad4_input, text = '4')

keypad3_input = tk.IntVar(value = 3)
keypad3 = ttk.Button(window, textvariable = keypad3_input, text = '3')

keypad2_input = tk.IntVar(value = 2)
keypad2 = ttk.Button(window, textvariable = keypad2_input, text = '2')

keypad1_input = tk.IntVar(value = 1)
keypad1 = ttk.Button(window, textvariable = keypad1_input, text = '1')

keypad0_input = tk.IntVar(value = 0)
keypad0 = ttk.Button(window, textvariable = keypad0_input, text = '0')

#keypad_clear_input = tk.IntVar(value = )
keypad_clear = ttk.Button(window, text = 'CE', command = clear)

keypad_sticky = 'nsew'
label_sticky = 'sw'
entry_sticky = 'w'
label_entry_padx = 2
keypad_padding = 2

# layout

status.grid(row = 4, column = 0, columnspan = 2, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
save.grid(row = 4, column = 2, columnspan = 2, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
resetb.grid(row = 4, column = 4, columnspan = 2, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
adios.grid(row = 4, column = 6, columnspan = 2, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)

label1.grid(row = 0, column = 0, sticky = label_sticky, padx = label_entry_padx)
label2.grid(row = 0, column = 2, sticky = label_sticky, padx = label_entry_padx)
label3.grid(row = 2, column = 0, sticky = label_sticky, padx = label_entry_padx)
label4.grid(row = 2, column = 2, sticky = label_sticky, padx = label_entry_padx)

lights_on_hour.grid(row = 1, column = 0, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)
lights_on_minute.grid(row = 1, column = 2, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)
lights_off_hour.grid(row = 3, column = 0, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)
lights_off_minute.grid(row = 3, column = 2, columnspan = 2, sticky = entry_sticky, padx = label_entry_padx)

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
