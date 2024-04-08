from PyQt5 import QtWidgets, QtGui


class PressureWidget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("pressure plot"))
        self.pressure_label = QtWidgets.QLabel("pressure")
        layout.addWidget(self.pressure_label)
        self.setLayout(layout)
        self.setFrameShape(QtWidgets.QFrame.Box)