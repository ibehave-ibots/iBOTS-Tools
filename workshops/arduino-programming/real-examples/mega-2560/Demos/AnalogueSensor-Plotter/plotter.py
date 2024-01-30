##########
## Try DearPyGUI
###########

import serial
import time
import json
# import matplotlib.pyplot as plt
import pyqtgraph as pqt



# Establish serial communication with Arduino
arduino_port = 'COM5'  # Replace with your Arduino port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)

widget = pqt.plot()
plot_item = widget.getPlotItem()

# initialise variables to store data
try:
    for _ in range(0,10):
        data_to_plot = []
        while len(data_to_plot)< 150:
            serial_data = ser.readline().decode().strip() # read data from arduino
            
            try: # first few loops are often corrupted
                data = json.loads(serial_data)
            except Exception as e:
                print(str(e))
                data = {'value':0, "loopnum":0,}

            data_to_plot.append(int(data['value']))
            plot_item.plot(data_to_plot)
            

            time.sleep(0.01)
        print(data)

except KeyboardInterrupt: # pres CTRL + C to stop program 
    pass

# Close the  serial connection
ser.close()




