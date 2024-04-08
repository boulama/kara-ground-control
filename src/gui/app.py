import sys
from PyQt5 import QtWidgets, QtGui
from widgets.gyroscope import GyroWidget
from widgets.accelerometer import AccelerometerWidget
from widgets.pressure import PressureWidget
from widgets.temperature import TemperatureWidget


class RocketPositionSTLUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # ... (the rest of the code remains the same)
        # Create the main layout
        main_layout = QtWidgets.QVBoxLayout()

        # Create the top row layout
        top_row_layout = QtWidgets.QHBoxLayout()

        # Create the rocket position STL layout
        rocket_pos_layout = QtWidgets.QVBoxLayout()
        rocket_pos_frame = QtWidgets.QFrame()
        rocket_pos_frame.setFrameShape(QtWidgets.QFrame.Box)
        rocket_pos_layout.addWidget(QtWidgets.QLabel("ROCKET POSITION STL"))
        rocket_pos_frame.setLayout(rocket_pos_layout)
        top_row_layout.addWidget(rocket_pos_frame, 2)

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
        bottom_row_layout = QtWidgets.QHBoxLayout()

        # Create the gyro widget
        self.gyro_widget = GyroWidget()
        bottom_row_layout.addWidget(self.gyro_widget, 1)

        # Create the accelerometer widget
        self.accelerometer_widget = AccelerometerWidget()
        bottom_row_layout.addWidget(self.accelerometer_widget, 1)

        # Create the sensor widgets
        self.temperature_widget = TemperatureWidget()
        bottom_row_layout.addWidget(self.temperature_widget, 1)

        self.pressure_widget = PressureWidget()
        bottom_row_layout.addWidget(self.pressure_widget, 1)

        # Create the enter com port and baud rate layout
        enter_layout = QtWidgets.QVBoxLayout()
        enter_frame = QtWidgets.QFrame()
        enter_frame.setFrameShape(QtWidgets.QFrame.Box)
        com_baud_layout = QtWidgets.QHBoxLayout()
        self.com_port_label = QtWidgets.QLabel("enter com port")
        self.baud_rate_label = QtWidgets.QLabel("enter baud rate")
        self.ok_button = QtWidgets.QPushButton("ok")
        com_baud_layout.addWidget(self.com_port_label)
        com_baud_layout.addWidget(self.baud_rate_label)
        com_baud_layout.addWidget(self.ok_button)
        enter_layout.addLayout(com_baud_layout)
        enter_frame.setLayout(enter_layout)
        bottom_row_layout.addWidget(enter_frame, 1)

        # Add the layouts to the main layout
        main_layout.addLayout(top_row_layout)
        main_layout.addLayout(bottom_row_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Rocket Position STL")
        self.setGeometry(100, 100, 800, 600)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = RocketPositionSTLUI()
    ui.show()
    sys.exit(app.exec_())
