from PyQt5 import QtWidgets, QtGui

class SerialSettingsWidget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Baud rate input
        baud_rate_layout = QtWidgets.QHBoxLayout()
        baud_rate_label = QtWidgets.QLabel("Baud Rate:")
        self.baud_rate_input = QtWidgets.QLineEdit()
        self.baud_rate_input.setText('57600')
        baud_rate_layout.addWidget(baud_rate_label)
        baud_rate_layout.addWidget(self.baud_rate_input)
        layout.addLayout(baud_rate_layout)

        # COM port selection
        com_port_layout = QtWidgets.QHBoxLayout()
        com_port_label = QtWidgets.QLabel("COM Port:")
        self.com_port_select = QtWidgets.QComboBox()
        # Add available COM ports to the combobox
        com_ports = ["COM1", "COM2", "COM3", "COM4"]  # Example list of COM ports
        self.com_port_select.addItems(com_ports)
        com_port_layout.addWidget(com_port_label)
        com_port_layout.addWidget(self.com_port_select)
        layout.addLayout(com_port_layout)

        # Add a button
        button = QtWidgets.QPushButton("Show Dialog")
        # Connect button click signal to showDialog method
        button.clicked.connect(self.showDialog)
        layout.addWidget(button)

        self.setLayout(layout)


    def showDialog(self):
        # Create and show the dialog
        QtWidgets.QMessageBox.information(self, "Dialog Title", "OK")