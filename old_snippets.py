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

    '''
    if var == 1:
        lights_manual.config(text = f'{title} - ON')
        lights_manual.update()
    else:
        lights_manual.config(text = f'{title} - OFF')
        lights_manual.update()
        '''
    
    #print(device)
    #print(bool_state)
    
        '''
    outlet_one_state = GPIO.input(5)
    outlet_two_state = GPIO.input(6)
    outlet_three_state = GPIO.input(13)
    outlet_four_state = GPIO.input(19)
    outlet_five_state = GPIO.input(26)
    outlet_six_state = GPIO.input(16)
    outlet_seven_state = GPIO.input(20)
    outlet_eight_state = GPIO.input(21)
    '''
    
    #print(f"{outlet_one_state}")
    '''
    if outlet_one_state:
        outlet_one_label.configure(bootstyle = 'warning')
        outlet_one_var.set(f'Outlet 1\nOFF')
    else:
        outlet_one_label.configure(bootstyle = 'success')
        outlet_one_var.set(f'Outlet 1\nON')
    '''
    
    
    '''
    conn = sqlite3.connect("gb_config.db")

    c = conn.cursor()

    c.execute("SELECT light_status FROM gb")
    
    #testvar = c.fetchall()
    print(testvar)

    status_dict = {'light_status': testvar[0]
    
    }
    for i, j in status_dict:
        if sql_var:
            outlet_one_label.configure(bootstyle = 'success')
            outlet_one_var.set(f'Outlet 1\nON')
        else:
            outlet_one_label.configure(bootstyle = 'warning')
            outlet_one_var.set(f'Outlet 1\nOFF')
    '''    '''
    light_on_distance = distance_list[0]
    light_off_distance = distance_list[1]
    water_on_distance = distance_list[2]
    water_off_distance = distance_list[3]
    '''
    
    
    #for i in time_dict:
        #time_dict.update({time_dict[i]: distance_list[i]}) 
        
#print(time_dict[next_event_name])
    #print(time_now + 10)
    #print(int(time_dict[f'{next_event_name}']))
    #print(time_dict)


'''
def method_change():
    methods = ['Growbrain', 'Shrooms', 'Micros']
    
    if method_var.get() == 'Growbrain':
        method_var.set('Shrooms')
        method_button.configure(bootstyle = 'warning')
        # cue the different modules for the method
        
    elif method_var.get() == 'Shrooms':
        method_var.set('Micros')
        method_button.configure(bootstyle = 'info')
        # cue the different modules for the method
        
    else:
        method_var.set('Growbrain')
        method_button.configure(bootstyle = 'secondary')
        # cue the different modules for the method
    
    # not working yet
    print(methods[-1])

    for i in methods:
        print(methods.index(i)+1)
        if method_var.get() == methods[-1]:
            method_var.set(methods[0])
        else:
            method_var.set(methods[methods.index(i)+1])
'''
    # Set Focus
# lights_on_hour.focus_set()
