from PyQt5 import QtWidgets, QtGui
import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from src.gui import config as cfg

class GyroWidget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        self.figure = Figure(figsize=(6, 6/cfg.MAIN_PLOT_WIDGET_AR))  # Set the size of the figure here
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.gyro_lines = [
            self.ax.plot([], [], lw=1, label='gyro x')[0],
            self.ax.plot([], [], lw=1, label='gyro y')[0],
            self.ax.plot([], [], lw=1, label='gyro z')[0]
        ]
        self.ax.set_title('Gyro')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')

        layout.addWidget(self.canvas)

        bottom_layout = QtWidgets.QHBoxLayout()
        self.gyro_x_label = QtWidgets.QLabel("gyro x")
        self.gyro_x_color = QtWidgets.QLabel()
        self.gyro_x_color.setFixedSize(20, 20)
        self.gyro_x_color.setStyleSheet("background-color: green;")
        self.gyro_y_label = QtWidgets.QLabel("gyro y")
        self.gyro_y_color = QtWidgets.QLabel()
        self.gyro_y_color.setFixedSize(20, 20)
        self.gyro_y_color.setStyleSheet("background-color: blue;")
        self.gyro_z_label = QtWidgets.QLabel("gyro z")
        self.gyro_z_color = QtWidgets.QLabel()
        self.gyro_z_color.setFixedSize(20, 20)
        self.gyro_z_color.setStyleSheet("background-color: red;")
        bottom_layout.addWidget(self.gyro_x_label)
        bottom_layout.addWidget(self.gyro_x_color)
        bottom_layout.addWidget(self.gyro_y_label)
        bottom_layout.addWidget(self.gyro_y_color)
        bottom_layout.addWidget(self.gyro_z_label)
        bottom_layout.addWidget(self.gyro_z_color)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)
        self.setFrameShape(QtWidgets.QFrame.Box)

        self.gyro_data = [
            np.zeros(100),
            np.zeros(100),
            np.zeros(100),
        ]
        self.time_data = np.linspace(-10, 0, 100)

        # Set fixed size for the graph
        self.canvas.setFixedSize(cfg.MAIN_PLOT_WIDGET_WIDTH, cfg.MAIN_PLOT_WIDGET_HEIGHT)  # Set the desired width and height

    def update_gyro_plot(self, data):
        gyro_values = data['gyro'][:3]  # Extract x, y, z values
        for axis, value in enumerate(gyro_values):
            self.gyro_data[axis][:-1] = self.gyro_data[axis][1:]
            self.gyro_data[axis][-1] = value
            self.gyro_lines[axis].set_data(self.time_data, self.gyro_data[axis])
        self.ax.set_xlim(self.time_data[0], self.time_data[-1])
        self.ax.set_ylim(-10, 10)
        self.canvas.draw()
