from PyQt5 import QtWidgets, QtGui
import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from src.gui import config as cfg


class AltitudeWidget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        self.figure = Figure(figsize=(6, 6/cfg.MAIN_PLOT_WIDGET_AR))  # Set the size of the figure here
        self.canvas = FigureCanvas(self.figure)
        self.alt = self.figure.add_subplot(111)
        self.alt_line = self.alt.plot([], [], lw=1)
        self.alt.set_title('Altitude (m)')
        self.alt.set_xlabel('Time')
        self.alt.set_ylabel('Value')

        layout.addWidget(self.canvas)

        bottom_layout = QtWidgets.QHBoxLayout()
        self.alt_label = QtWidgets.QLabel("curr. alt")
        self.alt_color = QtWidgets.QLabel()
        self.alt_color.setFixedSize(10, 10)
        self.alt_color.setStyleSheet("background-color: green;border-radius: 100%!important;")

        bottom_layout.addWidget(self.alt_color)
        bottom_layout.addWidget(self.alt_label)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)
        self.setFrameShape(QtWidgets.QFrame.Box)

        self.altitude_data = np.zeros(100)
        self.time_data = np.linspace(-10, 0, 100)
        self.canvas.setFixedSize(cfg.MAIN_PLOT_WIDGET_WIDTH, cfg.MAIN_PLOT_WIDGET_HEIGHT)  # Set the desired width and height

    def update_altitude_plot(self, data):
        self.altitude_data[:-1] = self.altitude_data[1:]
        self.altitude_data[-1] = data['altitude']
        self.alt_line[0].set_data(self.time_data, self.altitude_data)
        self.alt.set_xlim(self.time_data[0], self.time_data[-1])
        self.alt.set_ylim(-50, 1000)
        self.canvas.draw()