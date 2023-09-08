#!/usr/bin/python3
#import tkinter as tk

from tkinter import *
import ttkbootstrap as ttk
import RPi.GPIO as GPIO
import time
import datetime
import sqlite3

import board
import adafruit_dht

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

#master = Tk()

window = ttk.Window(themename = 'superhero')
window.title("Gnarvelous Outlet Control")
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


'''
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
button_width = 13
button_height = 4
button_border = 1
button_font = '-weight bold'
welcome_height = 6
welcome_width = 80
welcome_font = 16
welcome_background = "purple"
welcome_border = 2
welcome_relief = RAISED

print(screen_width)
print(screen_height)
'''

# outlets are numbered from left to right
    # 1 is 5 
    # 2 is 6 
    # 3 is 13
    # 4 is 19
    # 5 is 26
    # 6 is 16
    # 7 is 20
    # 8 is 21

def one():
    
    GPIO.output(5, True)
    if onetext.get() == "1 - ON":
        GPIO.output(5, True)
        onetext.set("1 - OFF")
    else:
        GPIO.output(5, False)
        onetext.set("1 - ON")

def two():
    
    GPIO.output(6, True)
    if twotext.get() == "2 - ON":
        GPIO.output(6, True)
        twotext.set("2 - OFF")
    else:
        GPIO.output(6, False)
        twotext.set("2 - ON")
    
def three():
    
    GPIO.output(13, True)
    if threetext.get() == "3 - ON":
        GPIO.output(13, True)
        threetext.set("3 - OFF")
    else:
        GPIO.output(13, False)
        threetext.set("3 - ON")
    
def four():
    
    GPIO.output(19, True)
    if fourtext.get() == "4 - ON":
        GPIO.output(19, True)
        fourtext.set("4 - OFF")
    else:
        GPIO.output(19, False)
        fourtext.set("4 - ON")
    
def five():
    
    GPIO.output(26, True)
    if fivetext.get() == "5 - ON":
        GPIO.output(26, True)
        fivetext.set("5 - OFF")
    else:
        GPIO.output(26, False)
        fivetext.set("5 - ON")
    
def six():
    
    GPIO.output(16, True)
    if sixtext.get() == "6 - ON":
        GPIO.output(16, True)
        sixtext.set("6 - OFF")
    else:
        GPIO.output(16, False)
        sixtext.set("6 - ON")
    
def seven():
    
    GPIO.output(20, True)
    if seventext.get() == "7 - ON":
        GPIO.output(20, True)
        seventext.set("7 - OFF")
    else:
        GPIO.output(20, False)
        seventext.set("7 - ON")
    
def eight():
    
    GPIO.output(21, True)
    if eighttext.get() == "8 - ON":
        GPIO.output(21, True)
        eighttext.set("8 - OFF")
    else:
        GPIO.output(21, False)
        eighttext.set("8 - ON")

def allon():
    
     GPIO.output(5, False)
     GPIO.output(6, False)
     GPIO.output(13, False)
     GPIO.output(19, False)
     GPIO.output(26, False)
     GPIO.output(16, False)
     GPIO.output(20, False)
     GPIO.output(21, False)
     
     onetext.set("1 - ON")
     twotext.set("2 - ON")
     threetext.set("3 - ON")
     fourtext.set("4 - ON")
     fivetext.set("5 - ON")
     sixtext.set("6 - ON")
     seventext.set("7 - ON")
     eighttext.set("8 - ON")

def alloff():
    
     GPIO.output(5, True)
     GPIO.output(6, True)
     GPIO.output(13, True)
     GPIO.output(19, True)
     GPIO.output(26, True)
     GPIO.output(16, True)
     GPIO.output(20, True)
     GPIO.output(21, True)
     
     onetext.set("1 - OFF")
     twotext.set("2 - OFF")
     threetext.set("3 - OFF")
     fourtext.set("4 - OFF")
     fivetext.set("5 - OFF")
     sixtext.set("6 - OFF")
     seventext.set("7 - OFF")
     eighttext.set("8 - OFF")


# define the grid
window.columnconfigure(0, weight = 2, uniform = 'a')
window.columnconfigure(1, weight = 2, uniform = 'a')
window.columnconfigure(2, weight = 2, uniform = 'a')
window.columnconfigure(3, weight = 2, uniform = 'a')
window.rowconfigure(0, weight = 2, uniform = 'a')
window.rowconfigure(1, weight = 2, uniform = 'a')
window.rowconfigure(2, weight = 2, uniform = 'a')
window.rowconfigure(3, weight = 2, uniform = 'a')

t = ttk.StringVar()
t.set("Tap an outlet to manually toggle on/off")

onetext = ttk.StringVar()
onetext.set("1")
twotext = ttk.StringVar()
twotext.set("2")
threetext = ttk.StringVar()
threetext.set("3")
fourtext = ttk.StringVar()
fourtext.set("4")
fivetext = ttk.StringVar()
fivetext.set("5")
sixtext = ttk.StringVar()
sixtext.set("6")
seventext = ttk.StringVar()
seventext.set("7")
eighttext = ttk.StringVar()
eighttext.set("8")
allontext = ttk.StringVar()
allontext.set("All ON")
allofftext = ttk.StringVar()
allofftext.set("All OFF")


welcome = ttk.Label(window, textvariable=t, font=label_font, bootstyle = 'primary')

one = ttk.ttk.Button(window, textvariable=onetext, command=one, bootstyle='info')
two = ttk.Button(window, textvariable=twotext, command=two, bootstyle='info')
three = ttk.Button(window, textvariable=threetext, command=three, bootstyle='info')
four = ttk.Button(window, textvariable=fourtext, command=four, bootstyle='info')
five = ttk.Button(window, textvariable=fivetext, command=five, bootstyle='info')
six = ttk.Button(window, textvariable=sixtext, command=six, bootstyle='info')
seven = ttk.Button(window, textvariable=seventext, command=seven, bootstyle='info')
eight = ttk.Button(window, textvariable=eighttext, command=eight, bootstyle='info')

all_on = ttk.Button(window, textvariable=allontext, command=allon, bootstyle='success')
all_off = ttk.Button(window, textvariable=allofftext, command=alloff, bootstyle='success')
adios = ttk.Button(window, text="EXIT", command=exit, bootstyle='danger')


keypad_sticky = 'nsew'
label_sticky = 'nsew'
entry_sticky = 'w'
label_entry_padx = 2
keypad_pad = 2

welcome.grid(column = 0, row = 0, columnspan = 4, sticky = label_sticky, padx = label_entry_padx)

one.grid(column = 0, row = 1, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)
two.grid(column = 1, row = 1, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)
three.grid(column = 2, row = 1, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)
four.grid(column = 3, row = 1, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)
five.grid(column = 0, row = 2, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)
six.grid(column = 1, row = 2, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)
seven.grid(column = 2, row = 2, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)
eight.grid(column = 3, row = 2, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)

all_on.grid(column = 1, row = 3, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)
all_off.grid(column = 2, row = 3, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)
adios.grid(column = 3, row = 3, columnspan=2, sticky = keypad_sticky, padx = keypad_pad, pady = keypad_pad)


window.mainloop()
