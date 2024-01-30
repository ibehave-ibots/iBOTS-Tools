import time
import numpy as np
import pyqtgraph as pg
from collections import deque
import serial
import struct
import pandas as pd
#######
# Establish serial communication with Arduino
arduino_port = 'COM5'  # Replace with your Arduino port
baud_rate = 115200
ser = serial.Serial(arduino_port, baud_rate, timeout=10)
######

maxlen = 1000
data =deque([], maxlen=maxlen)

widget = pg.plot()
curve = widget.plot()

while not widget.isHidden():
    Serial_data = list(struct.iter_unpack('2h', ser.read(2*2)))
    df=pd.DataFrame(Serial_data,columns= ['loopNum','value'])
    
    data.extend(df.value)
    
    curve.setData(data)
    pg.QtGui.QGuiApplication.processEvents()
    #time.sleep(1)

