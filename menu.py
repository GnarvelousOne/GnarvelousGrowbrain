import tkinter as tk
import ttkbootstrap as ttk
import os

# window
window = ttk.Window(themename = 'darkly')
window.title("Gnarvelous Growbrain")
window.geometry('350x150')

def run_water():
	os.system('python3 water.py')
	
def run_lights():
	os.system('python3 lights.py')
	
# define the grid
window.columnconfigure(0, weight = 2, uniform = 'a')
window.columnconfigure(1, weight = 2, uniform = 'a')

window.rowconfigure(0, weight = 2, uniform = 'a')
window.rowconfigure(1, weight = 2, uniform = 'a')

# widgets
water_button = ttk.Button(window,
	text='Water Module', 
	command=run_water,
	bootstyle = 'info'
	)

lights_button = ttk.Button(window, 
	text='Lights Module', 
	command=run_lights,
	bootstyle = 'warning'
	)
	
adios = ttk.Button(window,
	text='EXIT', 
	command=exit,
	bootstyle = 'danger'
	)

button_sticky = 'nsew'
button_pad = 2

# layout
water_button.grid(row = 0, column = 0, sticky = button_sticky, padx = button_pad, pady = button_pad)
lights_button.grid(row = 0, column = 1, sticky = button_sticky, padx = button_pad, pady = button_pad)
adios.grid(row = 1, column = 0, columnspan = 2, sticky = 'nsew', padx = button_pad, pady = button_pad)

# run
window.mainloop()
