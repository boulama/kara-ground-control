import serial
import socketio
import logging
import numpy as np

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_telemetry(serial_port: str = '/dev/tty.usbserial-0001',
                  baud_rate: int = 57600,
                  socket_server: str = 'http://127.0.0.1:6969'
                  ):
    logger.info("start connecting to serial port")
    # Configure the serial port
    ser = serial.Serial(serial_port, baud_rate)  # Use the correct serial port and baud rate
    logger.info("connected to port")
    try:
        with socketio.SimpleClient() as sio:
            sio.connect(socket_server)
            logger.info(f'connected to server {socket_server} with SID: {sio.sid}')
            logger.info(f"reading from serial port {serial_port}")
            while True:
                try:
                    # Read a line from the serial port
                    line = ser.readline().decode().strip()
                    logger.debug(line)
                    sio.emit('telemetry', parse_telemetry(line))
                except Exception as e:
                    logger.exception(e)

    except KeyboardInterrupt:
        # Close the serial port on keyboard interrupt
        ser.close()


def parse_telemetry(telemetry: str = '') -> dict:
    """Parses telemetry data from a string in a specific format.

    This function takes a string containing telemetry data separated by pipe characters (`|`)
    and returns a dictionary with the following keys:

    - `timestamp`: The timestamp (integer) extracted from the first element of the string.
    - `gyro`: A list of three floats representing the gyroscope readings (X, Y, Z).
    - `acc`: A list of three floats representing the accelerometer readings (X, Y, Z).
    - `temperature`: A float representing the temperature reading.

    Args:
      telemetry: The telemetry data string formatted as "timestamp|gyro_x|gyro_y|gyro_z|acc_x|acc_y|acc_z|temperature".
                  An empty string (`''`) is allowed as default.

    Returns:
      A dictionary containing the parsed telemetry data.

    Raises:
      ValueError: If the telemetry string format is invalid.
    """
    arr = telemetry.split('|')

    gyro_values = [to_float_or_zero(arr[i]) for i in range(1, 4)]
    gyro_values.append(magnitude(gyro_values))

    acc_values = [to_float_or_zero(arr[i]) for i in range(4, 7)]
    acc_values.append(magnitude(acc_values))

    obj = {
        'timestamp': int(int(arr[0])/1000),  # seconds
        'gyro': gyro_values,  # x, y, z, magnitude
        'acc': acc_values,  # x, y, z, magnitude
        'temperature': float(arr[7]),
        'pressure': float(arr[8]),
        'altitude': float(arr[9])
    }
    return obj


def to_float_or_zero(value):
    try:
        return float(value)
    except ValueError:
        return 0.0

def magnitude(vector):
    return round(np.linalg.norm(vector), 3)
