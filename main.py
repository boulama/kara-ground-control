import serial
import socketio
from time import sleep

print("start connecting to serial port")
# Configure the serial port
ser = serial.Serial('/dev/tty.usbserial-0001', 57600)  # Use the correct serial port and baud rate
print("connected to port")
try:
    with socketio.SimpleClient() as sio:
        sio.connect('http://127.0.0.1:6969')
        print('connected to server: ', sio.sid)
        print("reading from serial port")
        while True:
            sio.emit('cool-event', )
            # Read a line from the serial port
            line = ser.readline().decode().strip()
            print(line)
            sleep(1)

except KeyboardInterrupt:
    # Close the serial port on keyboard interrupt
    ser.close()
