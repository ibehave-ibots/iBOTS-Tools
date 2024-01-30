import serial
import struct

# Establish serial communication with Arduino
arduino_port = 'COM5'  # Replace with your Arduino port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=10)


while True:
    data = struct.iter_unpack('2h', ser.read(2*20))
    data = list(data)
    print(data)
