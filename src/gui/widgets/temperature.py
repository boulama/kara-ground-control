from PyQt5 import QtWidgets, QtGui
import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from src.gui import config as cfg


class TemperatureWidget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        self.figure = Figure(figsize=(6, 6/cfg.MAIN_PLOT_WIDGET_AR))  # Set the size of the figure here
        self.canvas = FigureCanvas(self.figure)
        self.temp = self.figure.add_subplot(111)
        self.temp_line = self.temp.plot([], [], lw=1)
        self.temp.set_title('Temperature (*C)')
        self.temp.set_xlabel('Time')
        self.temp.set_ylabel('Value')

        layout.addWidget(self.canvas)

        bottom_layout = QtWidgets.QHBoxLayout()
        self.temp_label = QtWidgets.QLabel("curr. temp")
        self.temp_color = QtWidgets.QLabel()
        self.temp_color.setFixedSize(10, 10)
        self.temp_color.setStyleSheet("background-color: green;border-radius: 100%!important;")

        bottom_layout.addWidget(self.temp_color)
        bottom_layout.addWidget(self.temp_label)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)
        self.setFrameShape(QtWidgets.QFrame.Box)

        self.temperature_data = np.zeros(100)
        self.time_data = np.linspace(-10, 0, 100)
        self.canvas.setFixedSize(cfg.MAIN_PLOT_WIDGET_WIDTH, cfg.MAIN_PLOT_WIDGET_HEIGHT)  # Set the desired width and height

    def update_temperature_plot(self, data):
        self.temperature_data[:-1] = self.temperature_data[1:]
        self.temperature_data[-1] = data['temperature']
        self.temp_line[0].set_data(self.time_data, self.temperature_data)
        self.temp.set_xlim(self.time_data[0], self.time_data[-1])
        self.temp.set_ylim(0, 60)
        self.canvas.draw()
