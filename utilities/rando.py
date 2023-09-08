#!/usr/bin/python3
#import tkinter as tk

from tkinter import *
import ttkbootstrap as ttk
import RPi.GPIO as GPIO

import random
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pin = 5

GPIO.setup(pin, GPIO.OUT)

window = ttk.Window(themename = 'superhero')
window.title("Gnarvelous Random Light")
window.geometry("575x300")


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


# outlets are numbered from left to right
    # 1 is 5 
    # 2 is 6 
    # 3 is 13
    # 4 is 19
    # 5 is 26
    # 6 is 16
    # 7 is 20
    # 8 is 21

    
def run(state):

    while True:    
        try:
            if state:
                try:
                    lightint = random.randint(1,5)
                    print(lightint)
                    GPIO.output(5, False)
                    sleep(lightint*.1)
                    lightint = random.randint(1,5)
                    print(lightint)
                    GPIO.output(5, True)
                    sleep(lightint*.1)
                    
                except KeyboardInterrupt:
                    raise
            else:
                pass
        except (KeyboardInterrupt, SystemExit):
            raise
        
        
# define the grid
window.columnconfigure(0, weight = 2, uniform = 'a')
window.columnconfigure(1, weight = 2, uniform = 'a')
window.rowconfigure(0, weight = 2, uniform = 'a')
window.rowconfigure(1, weight = 2, uniform = 'a')
window.rowconfigure(2, weight = 2, uniform = 'a')

t = ttk.StringVar()
t.set("Random Outlet Control")

welcome = ttk.Label(window, textvariable=t, font=label_font, bootstyle = 'primary')
on = ttk.ttk.Button(window, textvariable='ON', command= lambda: run(True), bootstyle='info')
off = ttk.Button(window, textvariable='OFF', command= lambda: run(False), bootstyle='info')
adios = ttk.Button(window, text="EXIT", command=exit, bootstyle='danger')

keypad_sticky = 'nsew'
label_sticky = 'nsew'
entry_sticky = 'w'
label_entry_padx = 2
keypad_pad = 2

welcome.grid(column = 0, row = 0, columnspan = 4, sticky = label_sticky, padx = label_entry_padx)
on.grid(column = 0, row = 1, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)
off.grid(column = 1, row = 1, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)
adios.grid(column = 0, row = 2, columnspan=2, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)

window.mainloop()
