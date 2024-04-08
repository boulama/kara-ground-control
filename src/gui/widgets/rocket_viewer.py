import pygame
from pygame.locals import *
from PyQt5 import QtWidgets, QtGui
import numpy as np
from src.gui import config as cfg
import stl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys

class RocketViewer(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((cfg.MAIN_PLOT_WIDGET_WIDTH, cfg.MAIN_PLOT_WIDGET_HEIGHT))
        pygame.display.set_caption("Rocket Viewer YEET")

        # Load the STL file
        self.mesh = stl.Mesh.from_file("../../files/k01.stl")

        # Set up the matplotlib figure and canvas
        self.figure = plt.figure(figsize=(6, 6/cfg.MAIN_PLOT_WIDGET_AR))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111, projection='3d')

        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.setFrameShape(QtWidgets.QFrame.Box)

    def update_rocket_view(self):
        self.screen.fill((0, 0, 0))

        # Render the 3D model
        self.ax.plot_trisurf(self.mesh.x, self.mesh.y, self.mesh.z, linewidth=0.2, antialiased=True)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Rocket Viewer')
        self.canvas.draw()

        # Update the Pygame display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    viewer = RocketViewer()
    viewer.show()
    sys.exit(app.exec_())
