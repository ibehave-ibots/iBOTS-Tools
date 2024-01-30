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
data_to_plot = {'x':[0], 'y':[0]}
#line1, = ax.plot(data_to_plot['x'], data_to_plot['y'] ,'kx')
try:
    for _ in range(0,2):
        while len(data_to_plot['x']) < 100:
            serial_data = ser.readline().decode().strip() # read data from arduino
            serial_data = int(serial_data)
            if serial_data > 1024:
                serial_data = 0
            print(serial_data)
        
            data_to_plot['y'].append(serial_data)
            data_to_plot['x'].append(len(data_to_plot['y']))
            # print(data_to_plot)
            # line1.set_ydata( data_to_plot['y'])
            # line1.set_xdata( data_to_plot['x'])

            ax.plot(data_to_plot['x'], data_to_plot['y'] ,'kx-')

            fig.canvas.draw() # update plot
            fig.canvas.flush_events()
            time.sleep(0.05)
        plt.clf()
except KeyboardInterrupt: # pres CTRL + C to stop program 
    pass

# Close the  serial connection
ser.close()