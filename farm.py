#import tkinter as tk
from tkinter import *
import ttkbootstrap as ttk
import RPi.GPIO as GPIO
import time
import datetime
import sqlite3
import os


# window
window = ttk.Window(themename = 'darkly')
window.title("|   The Gnarvelous Growbrain   |")
window.geometry('575x300')


# fonts
main_font = "Roboto" 
main_font_size = 8

label_font = "Roboto 8"


# style
primary_style = ttk.Style()
primary_style.configure('primary.TButton', font=(main_font, main_font_size))

secondary_style = ttk.Style()
secondary_style.configure('secondary.TButton', font=(main_font, main_font_size))

info_style = ttk.Style()
info_style.configure('info.TButton', font=(main_font, main_font_size))

success_style = ttk.Style()
success_style.configure('success.TButton', font=(main_font, main_font_size))

warning_style = ttk.Style()
warning_style.configure('warning.TButton', font=(main_font, main_font_size))

danger_style = ttk.Style()
danger_style.configure('danger.TButton', font=(main_font, main_font_size))

light_style = ttk.Style()
light_style.configure('light.TButton', font=(main_font, main_font_size))


def save_inputs_bind(events):
    save_inputs()

def save_inputs():
    
    timeNow = datetime.datetime.now().strftime("%H:%M")
    
    # Update database values
    
    # Write the results to the SQL database.
    conn = sqlite3.connect("gb_config.db")
    
    c = conn.cursor()
    
    # Only run this the first time to create the table.
    
    '''
    c.execute("""CREATE TABLE gb (
                lights_on_hour str,
                lights_on_minute str,
                lights_off_hour str,
                lights_off_minute str,
                lights_manual bool,
                lights_status str,
                water_on_hour str,
                water_on_minute str,
                water_off_hour str,
                water_off_minute str,
                water_manual bool,
                water_status str,
                circfan_manual bool,
                circfan_status str,
                intake_manual str,
                intake_status str,
                exhaust_manual bool,
                exhaust_status str,
                humidifier_manual str,
                humidifier_status str
                )""")'''
                
    w_dict = {
        'lights_on_hour':lights_on_hour_var, 
        'lights_on_minute':lights_on_minute_var,
        'lights_off_hour':lights_off_hour_var, 
        'lights_off_minute':lights_off_minute_var,
        'lights_manual':lights_manual_var,
        'lights_status':lights_status_var,
        'water_on_hour':water_on_hour_var, 
        'water_on_minute':water_on_minute_var,
        'water_off_hour':water_off_hour_var, 
        'water_off_minute':water_off_minute_var,
        'water_manual':water_manual_var,
        'water_status':water_status_var,
        'circfan_manual':circfan_manual_var,
        'circfan_status':circfan_status_var,
        'intake_manual':intake_manual_var,
        'intake_status':intake_status_var,
        'exhaust_manual':exhaust_manual_var,
        'exhaust_status':exhaust_status_var,
        'humidifier_manual':humidifier_manual_var,
        'humidifier_status':humidifier_status_var
        }

    for i,j in w_dict.items():
        if j.get():
            c.execute("UPDATE gb SET {} = ?".format(i), (j.get(),))
            #print('updated db')
            #print(j.get())
                
                 
    conn.commit()
    
    conn.close()
    
    print("Settings Saved")
    
    save_label_var.set(f'Last save:\n{timeNow}')
        
    next_event()
    refresh_temp_hum()


def current_temp_hum():
    
    timeNow = datetime.datetime.now().strftime("%H:%M")
    
    # get the last readings from dht.db

    conn = sqlite3.connect("dht.db")
    c = conn.cursor()

    query = c.execute("SELECT * FROM dht").fetchall()[-1]
    
    update = f"Last check:\n{query[4]}F / {query[5]}% rH\n{timeNow}"
    
    #print(query)
    #print(update)
    
    conn.commit()
    conn.close()
    
    return update
    
    
grid_index = 0
def page_change(forward):
    global grid_index
    #print(grid_index)

    grid_list = [empty_grid,lights_grid, water_grid, air_grid]   
    
    if forward:
        grid_index += 1
        last = 3
        if grid_index > (len(grid_list)-1):
            grid_index = 1

        grid_list[grid_index]()
        
        #print('grid_index += 1')
        #print(f'grid_index: {grid_index}')
        
    else:
        grid_index -= 1

        if grid_index < 1:
            grid_index = (len(grid_list)-1)
            
        grid_list[grid_index]()
        
        #print('grid_index -= 1')
        #print(f'grid_index: {grid_index}')
        

def manual(device, var):
    
    timeNow = datetime.datetime.now().strftime("%H:%M")
    
    title = device.title()
    
    if device == 'lights':
        pin = 5
    if device == 'water':
        pin = 6
    if device == 'circfan':
        pin = 13
    if device == 'intake':
        pin = 19
    if device == 'exhaust':
        pin = 26
    
    
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
    
    c.execute("SELECT water_on_hour FROM gb")
    testvar = c.fetchone()[0]
    #print(testvar)
    
    conn.commit()
    conn.close()
    
    last_var.set(f"Last: {title}\nManual {status_text}\n{timeNow}")
    
    status_light()


def status_light():

    # Read the states of the GPIOs to update the labels
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    status_dict = {outlet_one_label:[outlet_one_var, 5, 'Outlet 1'],
                    outlet_two_label:[outlet_two_var, 6, 'Outlet 2'],
                    outlet_three_label:[outlet_three_var, 13, 'Outlet 3'],
                    outlet_four_label:[outlet_four_var, 19, 'Outlet 4'],
                    outlet_five_label:[outlet_five_var, 26, 'Outlet 5'],
                    outlet_six_label:[outlet_six_var, 16, 'Outlet 6'],
                    outlet_seven_label:[outlet_seven_var, 20, 'Outlet 7'],
                    outlet_eight_label:[outlet_eight_var, 21, 'Outlet 8']}
    
    for i, j in status_dict.items():
        
        GPIO.setup(j[1], GPIO.OUT)
        
        pin_state = GPIO.input(j[1])
        
        if pin_state:
            i.configure(bootstyle = 'inverse danger')
            j[0].set(f'{j[2]}\nOFF')
            #print(f'{j[2]}\nOFF')
        
        else:
            i.configure(bootstyle = 'inverse success')
            j[0].set(f'{j[2]}\nON')
            #print(f'{j[2]}\nON')
            
    #print('----------')
    
    
def reset():
    
    lights_on_hour_var.set('')
    lights_on_minute_var.set('')
    lights_off_hour_var.set('')
    lights_off_minute_var.set('')
    water_on_hour_var.set('')
    water_on_minute_var.set('')
    water_off_hour_var.set('')
    water_off_minute_var.set('')
    
    #status_var.set(f"Status:\n Input fields reset\n{timeNow}")
    print('Input fields reset')


def clear():

    next_event()
    current_temp_hum()


keypad_num = 'e'
def keypad(entry, number):
    
    print(f'entry: {keypad_num}')
    print(f'number: {number}')
    
    terms = (keypad_num, number)
    blob = ''.join(terms)
    print(f'blob: {blob}')
    
    print(f'entry: {keypad_num}')
    print(f'number: {number}')
    
    a = '1'
    b = '2'
    
    print(a.join(b))


def next_event():
    
    # get timenow and all stored time values from db
    # compare all to timenow, find closest value and update label text
    
    timeNow = datetime.datetime.now()
    
    path = os.path.dirname(os.path.abspath(__file__))
    db = os.path.join(path, 'gb_config.db')
    
    conn = sqlite3.connect(db)
    c = conn.cursor()
    
    c.execute("SELECT lights_on_hour FROM gb")
    lights_on_hour = c.fetchone()[0]
    c.execute("SELECT lights_on_minute FROM gb")
    lights_on_minute = c.fetchone()[0]
    c.execute("SELECT lights_off_hour FROM gb")
    lights_off_hour = c.fetchone()[0]
    c.execute("SELECT lights_off_minute FROM gb")
    lights_off_minute = c.fetchone()[0]
    c.execute("SELECT water_on_hour FROM gb")
    water_on_hour = c.fetchone()[0]
    c.execute("SELECT water_on_minute FROM gb")
    water_on_minute = c.fetchone()[0]
    c.execute("SELECT water_off_hour FROM gb")
    water_off_hour = c.fetchone()[0]
    c.execute("SELECT water_off_minute FROM gb")
    water_off_minute = c.fetchone()[0]

    conn.commit()
    conn.close()

    time_dict = {}

    lights_on_time = int(lights_on_hour) + (int(lights_on_minute)/60)
    lights_on_time_display = str(lights_on_hour) + ':' + str(lights_on_minute)
    time_dict['Lights On'] = lights_on_time
    
    lights_off_time = int(lights_off_hour) + (int(lights_off_minute)/60)
    lights_off_time_display = str(lights_off_hour) + ':' + str(lights_off_minute)
    time_dict['Lights Off'] = lights_off_time
    
    water_on_time = int(water_on_hour) + (int(water_on_minute)/60)
    water_on_time_display = str(water_on_hour) + ':' + str(water_on_minute)
    time_dict['Water On'] = water_on_time
    
    water_off_time = int(water_off_hour) + (int(water_off_minute)/60)
    water_off_time_display = str(water_off_hour) + ':' + str(water_off_minute)
    time_dict['Water Off'] = water_off_time
    
    hour_now = int(timeNow.strftime('%H'))
    minute_now = int(timeNow.strftime('%M'))
    time_now = hour_now + (minute_now/60)
    time_now_display = str(hour_now) + ':' + str(minute_now)
    
    #print(time_dict)
    
    distance_list = []
    
    for i, j in time_dict.items():
        if j >= time_now:
            distance = j - time_now
            time_dict[i] = distance
            #distance_list.append(distance)
        
        else:
            distance = (24 - time_now) + j
            time_dict[i] = distance
            #distance_list.append(distance)
    
    #print(time_dict)
        
    next_event_name = min(time_dict, key = time_dict.get)
    #print(next_event_name)
    
    next_time = time_now + time_dict[next_event_name]
    #print(next_time)
    
    next_time_minute = str(round((next_time % 1) * 60))
    if len(next_time_minute) == 1:
        next_time_minute = '0' + next_time_minute
    #print(next_time_minute)
    
    next_time_hour = int(next_time - (next_time % 1))
    #print(next_time_hour)
    
    next_var.set(f'Next:\n{next_event_name}\n{next_time_hour}:{next_time_minute}')
    
    
def refresh_temp_hum():
    status_var.set(current_temp_hum())
    
    
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
status_var.set(current_temp_hum())

save_label_var = ttk.StringVar()
save_label_var.set('Last save:')

module_label_var = ttk.StringVar()
module_label_var.set('No module\nloaded')

last_var = ttk.StringVar()
last_var.set('Last:\nnone\nnone')

next_var = ttk.StringVar()
next_var.set('Next:\nnone\nnone')

status = ttk.Label(window, font = label_font, textvariable = status_var, bootstyle = 'inverse secondary')
save_label = ttk.Label(window, font = label_font, textvariable = save_label_var, bootstyle = 'inverse secondary')
module_label = ttk.Label(window, font = label_font, textvariable = module_label_var, bootstyle = 'inverse secondary')
last_label = ttk.Label(window, font = label_font, textvariable = last_var, bootstyle = 'inverse secondary')
next_label = ttk.Label(window, font = label_font, textvariable = next_var, bootstyle = 'inverse secondary')

next_page = ttk.Button(window, text='Next\nPage', command = lambda:page_change(1), bootstyle = 'light')
prev_page = ttk.Button(window, text='Prev\nPage', command = lambda:page_change(0), bootstyle = 'light')

lights_manual_on = ttk.Button(window, text='ON', command = lambda:manual('lights', 1), bootstyle = 'warning', style = 'warning.TButton')
lights_manual_off = ttk.Button(window, text='OFF', command = lambda:manual('lights', 0), bootstyle = 'warning', style = 'warning.TButton')

water_manual_on = ttk.Button(window, text='ON', command = lambda:manual('water', 1), bootstyle = 'info', style = 'info.TButton')
water_manual_off = ttk.Button(window, text='OFF', command = lambda:manual('water', 0), bootstyle = 'info', style = 'info.TButton')

circfan_manual_on = ttk.Button(window, text='ON', command = lambda:manual('circfan', 1), bootstyle = 'light outline')
circfan_manual_off = ttk.Button(window, text='OFF', command = lambda:manual('circfan', 0), bootstyle = 'light outline')

intake_manual_on = ttk.Button(window, text='ON', command = lambda:manual('intake', 1), bootstyle = 'light outline')
intake_manual_off = ttk.Button(window, text='OFF', command = lambda:manual('intake', 0), bootstyle = 'light outline')

exhaust_manual_on = ttk.Button(window, text='ON', command = lambda:manual('exhaust', 1), bootstyle = 'light outline')
exhaust_manual_off = ttk.Button(window, text='OFF', command = lambda:manual('exhaust', 0), bootstyle = 'light outline')

save = ttk.Button(window, text='SAVE /\nUPDATE', command = save_inputs, bootstyle = 'success', style = 'success.TButton')
resetb = ttk.Button(window, text='RESET', command = reset, bootstyle = 'warning', style = 'warning.TButton')
adios = ttk.Button(window, text='EXIT', command = exit, bootstyle = 'danger', style = 'danger.TButton')


# Lights
lights_on_time_label = ttk.Label(window, text = 'ON\nTime:', font = label_font, bootstyle = 'warning')
lights_off_time_label = ttk.Label(window, text = 'OFF\nTime:', font = label_font, bootstyle = 'warning')
lights_manual_label = ttk.Label(window, text = 'Manual:', font = label_font, bootstyle = 'warning')

lights_on_hour_var = ttk.StringVar()
lights_on_minute_var = ttk.StringVar()
lights_off_hour_var = ttk.StringVar()
lights_off_minute_var = ttk.StringVar()

lights_on_hour = ttk.Entry(window, textvariable = lights_on_hour_var, bootstyle = 'warning')
lights_on_minute = ttk.Entry(window, textvariable = lights_on_minute_var, bootstyle = 'warning')
lights_off_hour = ttk.Entry(window, textvariable = lights_off_hour_var, bootstyle = 'warning')
lights_off_minute = ttk.Entry(window, textvariable = lights_off_minute_var, bootstyle = 'warning')


# Water
water_on_time_label = ttk.Label(window, text = 'ON\nTime:', font = label_font, bootstyle = 'info')
water_off_time_label = ttk.Label(window, text = 'OFF\nTime:', font = label_font, bootstyle = 'info')
water_manual_label = ttk.Label(window, text = 'Manual:', font = label_font, bootstyle = 'info')

water_on_hour_var = ttk.StringVar()
water_on_minute_var = ttk.StringVar()
water_off_hour_var = ttk.StringVar()
water_off_minute_var = ttk.StringVar()

water_on_hour = ttk.Entry(window, textvariable = water_on_hour_var, bootstyle = 'info')
water_on_minute = ttk.Entry(window, textvariable = water_on_minute_var, bootstyle = 'info')
water_off_hour = ttk.Entry(window, textvariable = water_off_hour_var, bootstyle = 'info')
water_off_minute = ttk.Entry(window, textvariable = water_off_minute_var, bootstyle = 'info')


water_manual_var = ttk.IntVar()
water_status_var = ttk.StringVar()
lights_manual_var = ttk.IntVar()
lights_status_var = ttk.StringVar()
humidifier_manual_var = ttk.IntVar()
humidifier_status_var = ttk.StringVar()
circfan_manual_var = ttk.IntVar()
circfan_status_var = ttk.StringVar()
intake_manual_var = ttk.IntVar()
intake_status_var = ttk.StringVar()
exhaust_manual_var = ttk.IntVar()
exhaust_status_var = ttk.StringVar()


# Air
circfan_manual_label = ttk.Label(window, text = 'Circulation:', font = label_font, bootstyle = 'light')
intake_manual_label = ttk.Label(window, text = 'Intake:', font = label_font, bootstyle = 'light')
exhaust_manual_label = ttk.Label(window, text = 'Exhaust:', font = label_font, bootstyle = 'light')


# Status Lights
outlet_one_var = ttk.StringVar()
outlet_one_var.set('Output 1')
outlet_two_var = ttk.StringVar()
outlet_two_var.set('Output 2')
outlet_three_var = ttk.StringVar()
outlet_three_var.set('Output 3')
outlet_four_var = ttk.StringVar()
outlet_four_var.set('Output 4')
outlet_five_var = ttk.StringVar()
outlet_five_var.set('Output 5')
outlet_six_var = ttk.StringVar()
outlet_six_var.set('Output 6')
outlet_seven_var = ttk.StringVar()
outlet_seven_var.set('Output 7')
outlet_eight_var = ttk.StringVar()
outlet_eight_var.set('Output 8')

outlet_one_label = ttk.Label(window, textvariable = outlet_one_var, font = label_font, bootstyle = 'inverse info')
outlet_two_label = ttk.Label(window, textvariable = outlet_two_var, font = label_font, bootstyle = 'inverse info')
outlet_three_label = ttk.Label(window, textvariable = outlet_three_var, font = label_font, bootstyle = 'inverse info')
outlet_four_label = ttk.Label(window, textvariable = outlet_four_var, font = label_font, bootstyle = 'inverse info')
outlet_five_label = ttk.Label(window, textvariable = outlet_five_var, font = label_font, bootstyle = 'inverse info')
outlet_six_label = ttk.Label(window, textvariable = outlet_six_var, font = label_font, bootstyle = 'inverse info')
outlet_seven_label = ttk.Label(window, textvariable = outlet_seven_var, font = label_font, bootstyle = 'inverse info')
outlet_eight_label = ttk.Label(window, textvariable = outlet_eight_var, font = label_font, bootstyle = 'inverse info')


# Keypad
keypad9_input = ttk.StringVar(value = '9')
keypad9 = ttk.Button(window, textvariable = keypad9_input, text = '9', command = lambda: keypad(keypad_num, keypad9_input.get()), style = 'primary.TButton')

keypad8_input = ttk.StringVar(value = '8')
keypad8 = ttk.Button(window, textvariable = keypad8_input, text = '8', command = lambda: keypad(keypad_num, keypad8_input.get()), style = 'primary.TButton')

keypad7_input = ttk.StringVar(value = '7')
keypad7 = ttk.Button(window, textvariable = keypad7_input, text = '7', command = lambda: keypad(keypad_num, keypad7_input.get()), style = 'primary.TButton')

keypad6_input = ttk.StringVar(value = '6')
keypad6 = ttk.Button(window, textvariable = keypad6_input, text = '6', command = lambda: keypad(keypad_num, keypad6_input.get()), style = 'primary.TButton')

keypad5_input = ttk.StringVar(value = '5')
keypad5 = ttk.Button(window, textvariable = keypad5_input, text = '5', command = lambda: keypad(keypad_num, keypad5_input.get()),style = 'primary.TButton')

keypad4_input = ttk.StringVar(value = '4')
keypad4 = ttk.Button(window, textvariable = keypad4_input, text = '4', command = lambda: keypad(keypad_num, keypad4_input.get()),style = 'primary.TButton')

keypad3_input = ttk.StringVar(value = '3')
keypad3 = ttk.Button(window, textvariable = keypad3_input, text = '3', command = lambda: keypad(keypad_num, keypad3_input.get()), style = 'primary.TButton')

keypad2_input = ttk.StringVar(value = '2')
keypad2 = ttk.Button(window, textvariable = keypad2_input, text = '2', command = lambda: keypad(keypad_num, keypad2_input.get()), style = 'primary.TButton')

keypad1_input = ttk.StringVar(value = '1')
keypad1 = ttk.Button(window, textvariable = keypad1_input, text = '1', command = lambda: keypad(keypad_num, keypad1_input.get()), style = 'primary.TButton')

keypad0_input = ttk.StringVar(value = '0')
keypad0 = ttk.Button(window, textvariable = keypad0_input, text = '0', command = lambda: keypad(keypad_num, keypad0_input.get()), style = 'primary.TButton')

keypad_clear = ttk.Button(window, text = 'CE', command = clear, style = 'primary.TButton')


keypad_sticky = 'nsew'
label_sticky = 'sw'
entry_sticky = 'w'
label_entry_padx = 2
keypad_padding = 2


# Grid layout
status.grid(row = 4, column = 3, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
save_label.grid(row = 4, column = 4, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
module_label.grid(row = 0, column = 2, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
last_label.grid(row = 4, column = 0, columnspan = 2, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
next_label.grid(row = 4, column = 2, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
prev_page.grid(row = 0, column = 3, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
next_page.grid(row = 0, column = 4, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)

outlet_one_label.grid(row = 0, column = 0, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
outlet_two_label.grid(row = 0, column = 1, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
outlet_three_label.grid(row = 1, column = 0, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
outlet_four_label.grid(row = 1, column = 1, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
outlet_five_label.grid(row = 2, column = 0, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
outlet_six_label.grid(row = 2, column = 1, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
outlet_seven_label.grid(row = 3, column = 0, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
outlet_eight_label.grid(row = 3, column = 1, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)

save.grid(row = 4, column = 5, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
resetb.grid(row = 4, column = 6, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)
adios.grid(row = 4, column = 7, sticky = 'nsew', padx = label_entry_padx, pady = label_entry_padx)


def empty_grid():
    pass

def lights_grid():
        
    # Remove
            
    water_on_time_label.grid_remove()
    water_off_time_label.grid_remove()
    water_manual_label.grid_remove()
    
    water_on_hour.grid_remove()
    water_on_minute.grid_remove()
    water_off_hour.grid_remove()
    water_off_minute.grid_remove()
    
    water_manual_on.grid_remove()
    water_manual_off.grid_remove()
    
    circfan_manual_label.grid_remove()
    intake_manual_label.grid_remove()
    exhaust_manual_label.grid_remove()
    
    circfan_manual_on.grid_remove()
    circfan_manual_off.grid_remove()
    intake_manual_on.grid_remove()
    intake_manual_off.grid_remove()
    exhaust_manual_on.grid_remove()
    exhaust_manual_off.grid_remove()

    
    # Add
    
    module_label_var.set(f'Lights\nModule')
    module_label.configure(bootstyle = 'warning')
        
    lights_on_time_label.grid(row = 1, column = 2, padx = label_entry_padx)
    lights_off_time_label.grid(row = 2, column = 2, padx = label_entry_padx)
    lights_manual_label.grid(row = 3, column = 2, padx = label_entry_padx)
    
    lights_on_hour.grid(row = 1, column = 3, sticky = entry_sticky, padx = label_entry_padx),
    lights_on_minute.grid(row = 1, column = 4, sticky = entry_sticky, padx = label_entry_padx),
    lights_off_hour.grid(row = 2, column = 3, sticky = entry_sticky, padx = label_entry_padx),
    lights_off_minute.grid(row = 2, column = 4, sticky = entry_sticky, padx = label_entry_padx)
    
    lights_manual_on.grid(row = 3, column = 3, sticky = keypad_sticky, padx = label_entry_padx, pady = label_entry_padx)
    lights_manual_off.grid(row = 3, column = 4, sticky = keypad_sticky, padx = label_entry_padx, pady = label_entry_padx)
    

def water_grid():
    
    # Remove
            
    lights_on_time_label.grid_remove()
    lights_off_time_label.grid_remove()
    lights_manual_label.grid_remove()
    
    lights_on_hour.grid_remove()
    lights_on_minute.grid_remove()
    lights_off_hour.grid_remove()
    lights_off_minute.grid_remove()
    
    lights_manual_on.grid_remove()
    lights_manual_off.grid_remove()
    
    circfan_manual_label.grid_remove()
    intake_manual_label.grid_remove()
    exhaust_manual_label.grid_remove()
    
    circfan_manual_on.grid_remove()
    circfan_manual_off.grid_remove()
    intake_manual_on.grid_remove()
    intake_manual_off.grid_remove()
    exhaust_manual_on.grid_remove()
    exhaust_manual_off.grid_remove()


    # Add
    
    module_label_var.set(f'Water\nModule')
    module_label.configure(bootstyle = 'info')
        
    water_on_time_label.grid(row = 1, column = 2, padx = label_entry_padx)
    water_off_time_label.grid(row = 2, column = 2, padx = label_entry_padx)
    water_manual_label.grid(row = 3, column = 2, padx = label_entry_padx)
    
    water_on_hour.grid(row = 1, column = 3, sticky = entry_sticky, padx = label_entry_padx),
    water_on_minute.grid(row = 1, column = 4, sticky = entry_sticky, padx = label_entry_padx),
    water_off_hour.grid(row = 2, column = 3, sticky = entry_sticky, padx = label_entry_padx),
    water_off_minute.grid(row = 2, column = 4, sticky = entry_sticky, padx = label_entry_padx)
    
    water_manual_on.grid(row = 3, column = 3, sticky = keypad_sticky, padx = label_entry_padx, pady = label_entry_padx)
    water_manual_off.grid(row = 3, column = 4, sticky = keypad_sticky, padx = label_entry_padx, pady = label_entry_padx)
        
    
def air_grid():
    
    # Remove
            
    lights_on_time_label.grid_remove()
    lights_off_time_label.grid_remove()
    lights_manual_label.grid_remove()
    
    lights_on_hour.grid_remove()
    lights_on_minute.grid_remove()
    lights_off_hour.grid_remove()
    lights_off_minute.grid_remove()
    
    lights_manual_on.grid_remove()
    lights_manual_off.grid_remove()
    
    
    water_on_time_label.grid_remove()
    water_off_time_label.grid_remove()
    water_manual_label.grid_remove()
    
    water_on_hour.grid_remove()
    water_on_minute.grid_remove()
    water_off_hour.grid_remove()
    water_off_minute.grid_remove()
    
    water_manual_on.grid_remove()
    water_manual_off.grid_remove()

    
    # Add
    
    module_label_var.set(f'Air\nModule')
    module_label.configure(bootstyle = 'light')
    
    circfan_manual_label.grid(row = 1, column = 2, padx = label_entry_padx)
    intake_manual_label.grid(row = 2, column = 2, padx = label_entry_padx)
    exhaust_manual_label.grid(row = 3, column = 2, padx = label_entry_padx)
    
    circfan_manual_on.grid(row = 1, column = 3, sticky = keypad_sticky, padx = label_entry_padx, pady = label_entry_padx)
    circfan_manual_off.grid(row = 1, column = 4, sticky = keypad_sticky, padx = label_entry_padx, pady = label_entry_padx)
    intake_manual_on.grid(row = 2, column = 3, sticky = keypad_sticky, padx = label_entry_padx, pady = label_entry_padx)
    intake_manual_off.grid(row = 2, column = 4, sticky = keypad_sticky, padx = label_entry_padx, pady = label_entry_padx)
    exhaust_manual_on.grid(row = 3, column = 3, sticky = keypad_sticky, padx = label_entry_padx, pady = label_entry_padx)
    exhaust_manual_off.grid(row = 3, column = 4, sticky = keypad_sticky, padx = label_entry_padx, pady = label_entry_padx)
    

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

next_event()
status_light()

# run
window.mainloop()
