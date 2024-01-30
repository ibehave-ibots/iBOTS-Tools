#########################################################
# Loads packets of JSON data sent from an Arduino and plots the results live
# 
# While the script is running press CTRL + C to kill it. After a while it will stop automatically
#
#
#


import serial
import time
import json
import matplotlib.pyplot as plt
import numpy as np


# Establish serial communication with Arduino
arduino_port = 'COM5'  # Replace with your Arduino port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)

# set up plot
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

# initialise variables to store data
data_to_plot = {'x':[], 'y':[]}
try:
    #for _ in range(0,100):
    while len(data_to_plot['x']) < 500:
        serial_data = ser.readline().decode().strip() # read data from arduino
        
        try: # first few loops are often corrupted
            data = json.loads(serial_data)
        except Exception as e:
            print(str(e))
            data = {'loop number':np.nan, "value":np.nan,"analogue sensor value":np.nan }
        
        #loop_numbers = [x['loop number'] for x in data]
        #sensor_values = [x['digital sensor value'] for x in data]
        values = data['value']
        #print(sensor_values)
        print(values)
        data_to_plot['y'].append(values)
        data_to_plot['x'].append(len(data_to_plot['x']))
        #data_to_plot['y'].extend([x['analogue sensor value'] for x in data])


        ax.plot(data_to_plot['x'], data_to_plot['y'] ,'kx')

        fig.canvas.draw() # update plot
        fig.canvas.flush_events()
        time.sleep(0.05)

except KeyboardInterrupt: # pres CTRL + C to stop program 
    pass

# Close the  serial connection
ser.close()