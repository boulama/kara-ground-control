import sys
import serial
import logging
import numpy as np
import threading
import sys
from PyQt5 import QtWidgets, QtGui

from src.gui.widgets.altitude import AltitudeWidget
# widgets
from widgets.gyroscope import GyroWidget
from widgets.accelerometer import AccelerometerWidget
from widgets.pressure import PressureWidget
from widgets.temperature import TemperatureWidget
from widgets.serial_settings import SerialSettingsWidget
from widgets.rocket_viewer import RocketViewer

import matplotlib

matplotlib.use('Qt5Agg')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RocketPositionSTLUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.isRunning = True

    def initUI(self):
        # Create the main layout
        main_layout = QtWidgets.QVBoxLayout()

        # Create the top row layout
        top_row_layout = QtWidgets.QHBoxLayout()

        # Create the rocket position STL layout
        self.stl_viewer = RocketViewer('../../src/files/k01.stl')
        top_row_layout.addWidget(self.stl_viewer, 2)

        # Create the system-health layout
        system_health_layout = QtWidgets.QVBoxLayout()
        system_health_frame = QtWidgets.QFrame()
        system_health_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.antenna_strength_label = QtWidgets.QLabel("antenna strength")
        self.barometer_status_label = QtWidgets.QLabel("Barometer status")
        self.imu_status_label = QtWidgets.QLabel("IMU status")
        system_health_layout.addWidget(self.antenna_strength_label)
        system_health_layout.addWidget(self.barometer_status_label)
        system_health_layout.addWidget(self.imu_status_label)
        system_health_frame.setLayout(system_health_layout)
        top_row_layout.addWidget(system_health_frame, 1)

        # Create the bottom row layout
        bottom_row_layout = QtWidgets.QGridLayout()

        # Create the gyro widget
        self.gyro_widget = GyroWidget()
        bottom_row_layout.addWidget(self.gyro_widget, 0, 0)  # Add to the first column of the first row

        # Create the accelerometer widget
        self.accelerometer_widget = AccelerometerWidget()
        bottom_row_layout.addWidget(self.accelerometer_widget, 0, 1)  # Add to the second column of the first row

        # Create the temperature widget
        self.temperature_widget = TemperatureWidget()
        bottom_row_layout.addWidget(self.temperature_widget, 0, 2)  # Add to the third column of the first row

        # Create the altitude widget
        self.altitude_widget = AltitudeWidget()
        bottom_row_layout.addWidget(self.altitude_widget, 1, 0)  # Add to the first column of the second row

        # Create the pressure widget
        self.pressure_widget = PressureWidget()
        bottom_row_layout.addWidget(self.pressure_widget, 1, 1)  # Add to the second column of the second row

        self.serial_settings_widget = SerialSettingsWidget()
        bottom_row_layout.addWidget(self.serial_settings_widget, 1, 2)

        # Set the column stretch to make the widgets expand evenly
        bottom_row_layout.setColumnStretch(0, 1)
        bottom_row_layout.setColumnStretch(1, 1)
        bottom_row_layout.setColumnStretch(2, 1)

        # Add the layouts to the main layout
        main_layout.addLayout(top_row_layout)
        main_layout.addLayout(bottom_row_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Rocket Position STL")
        self.setGeometry(100, 100, 800, 600)

    def get_telemetry(self, serial_port: str = '/dev/cu.usbserial-19',
                      baud_rate: int = 57600
                      ):
        # Use threading for telemetry
        self.telemetry_thread = TelemetryThread(serial_port, baud_rate, self)
        self.telemetry_thread.start()

    def closeEvent(self, event):
        self.isRunning = False
        self.telemetry_thread.join()

    def parse_telemetry(self, line):
        # Implement your telemetry parsing logic here
        from src import kara
        data = kara.parse_telemetry(line)
        return data

class TelemetryThread(threading.Thread):
    def __init__(self, serial_port, baud_rate, ui):
        threading.Thread.__init__(self)
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.ui = ui

    def run(self):
        logger.info("start connecting to serial port")
        ser = serial.Serial(self.serial_port, self.baud_rate)  # Use the correct serial port and baud rate
        try:
            logger.info(f"reading from serial port {self.serial_port}")
            while self.ui.isRunning:
                try:
                    line = ser.readline().decode().strip()
                    logger.debug(line)
                    data = self.ui.parse_telemetry(line)
                    logger.info(data)
                    self.ui.gyro_widget.update_gyro_plot(data)
                    self.ui.accelerometer_widget.update_acc_plot(data)
                    self.ui.temperature_widget.update_temperature_plot(data)
                    self.ui.altitude_widget.update_altitude_plot(data)
                except Exception as e:
                    logger.exception(e)
        except KeyboardInterrupt:
            ser.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = RocketPositionSTLUI()
    ui.get_telemetry()
    ui.show()
    sys.exit(app.exec_())
