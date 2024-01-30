import serial
import time
import json
import matplotlib.pyplot as plt



# Establish serial communication with Arduino
arduino_port = 'COM5'  # Replace with your Arduino port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)

# set up plot
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

# initialise variables to store data
data_to_plot = []
try:
    while True:
        serial_data = ser.readline().decode().strip() # read data from arduino
        
        try: # first few loops are often corrupted
            data = json.loads(serial_data)
        except Exception as e:
            print(str(e))
            data = {'value':0, "scaled value":0, "number to light":0}

        data_to_plot.append(data['value'])
        ax.plot(data_to_plot, 'kx')

        fig.canvas.draw() # update plot
        fig.canvas.flush_events()
        time.sleep(0.05)

except KeyboardInterrupt: # pres CTRL + C to stop program 
    pass

# Close the  serial connection
ser.close()




