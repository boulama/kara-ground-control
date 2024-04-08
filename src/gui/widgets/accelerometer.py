from PyQt5 import QtWidgets, QtGui
import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from src.gui import config as cfg

class AccelerometerWidget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        self.figure = Figure(figsize=(6, 6/cfg.MAIN_PLOT_WIDGET_AR))  # Set the size of the figure here
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.acc_lines = [
            self.ax.plot([], [], lw=1, label='acc x')[0],
            self.ax.plot([], [], lw=1, label='acc y')[0],
            self.ax.plot([], [], lw=1, label='acc z')[0]
        ]
        self.ax.set_title('Accelerometer')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')

        layout.addWidget(self.canvas)

        bottom_layout = QtWidgets.QHBoxLayout()
        self.acc_x_label = QtWidgets.QLabel("acc x")
        self.acc_x_color = QtWidgets.QLabel()
        self.acc_x_color.setFixedSize(20, 20)
        self.acc_x_color.setStyleSheet("background-color: green;")
        self.acc_y_label = QtWidgets.QLabel("acc y")
        self.acc_y_color = QtWidgets.QLabel()
        self.acc_y_color.setFixedSize(20, 20)
        self.acc_y_color.setStyleSheet("background-color: blue;")
        self.acc_z_label = QtWidgets.QLabel("acc z")
        self.acc_z_color = QtWidgets.QLabel()
        self.acc_z_color.setFixedSize(20, 20)
        self.acc_z_color.setStyleSheet("background-color: red;")
        bottom_layout.addWidget(self.acc_x_label)
        bottom_layout.addWidget(self.acc_x_color)
        bottom_layout.addWidget(self.acc_y_label)
        bottom_layout.addWidget(self.acc_y_color)
        bottom_layout.addWidget(self.acc_z_label)
        bottom_layout.addWidget(self.acc_z_color)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)
        self.setFrameShape(QtWidgets.QFrame.Box)

        self.acc_data = [
            np.zeros(100),
            np.zeros(100),
            np.zeros(100),
        ]
        self.time_data = np.linspace(-10, 0, 100)
        self.canvas.setFixedSize(cfg.MAIN_PLOT_WIDGET_WIDTH, cfg.MAIN_PLOT_WIDGET_HEIGHT)  # Set the desired width and height

    def update_acc_plot(self, data):
        acc_values = data['acc'][:3]  # Extract x, y, z values
        for axis, value in enumerate(acc_values):
            self.acc_data[axis][:-1] = self.acc_data[axis][1:]
            self.acc_data[axis][-1] = value
            self.acc_lines[axis].set_data(self.time_data, self.acc_data[axis])
        self.ax.set_xlim(self.time_data[0], self.time_data[-1])
        self.ax.set_ylim(-25, 25)
        self.canvas.draw()
