import serial

# Establish serial communication with Arduino
arduino_port = 'COM5'  # Replace with your Arduino port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)


try:
    while True:
        # Read a line of serial data from Arduino
        serial_data = ser.readline().decode().strip()
        
        data_to_write = serial_data
        with open("test.txt", 'a') as f:
            f.write(data_to_write + '\n')
       
        
except KeyboardInterrupt:
    pass

# Close the  serial connection
ser.close()