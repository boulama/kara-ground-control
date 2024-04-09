import random
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
from pyqtgraph.opengl import GLMeshItem, GLViewWidget, GLScatterPlotItem, MeshData
from stl import mesh


class RocketViewer(QtWidgets.QWidget):
    def __init__(self, stl_path):
        super().__init__()
        self.stl_path = stl_path

        self.pitch = 0
        self.yaw = 0
        self.roll = 0

        self.initUI()

    def initUI(self):
        # Create an OpenGL widget for 3D rendering
        layout = QtWidgets.QVBoxLayout()

        # Set width and height for the GLViewWidget
        width = 600
        height = 300

        # Create an OpenGL widget for 3D rendering
        self.view = GLViewWidget()
        self.view.setMinimumSize(width, height)
        layout.addWidget(self.view)

        self.setLayout(layout)

        # Load the STL file
        self.loadSTL()

    def loadSTL(self):
        stl_mesh = mesh.Mesh.from_file(self.stl_path)

        points = stl_mesh.points.reshape(-1, 3)
        faces = np.arange(points.shape[0]).reshape(-1, 3)

        center = np.mean(points, axis=0)
        new_center = (100, -100, 0)

        # Translate the model to the new center location
        translation = np.array([new_center[0] - center[0], new_center[1] - center[1], new_center[2] - center[2]])
        points += translation

        mesh_data = MeshData(vertexes=points, faces=faces)
        self.mesh_item = GLMeshItem(meshdata=mesh_data, smooth=True, drawFaces=True, drawEdges=True, edgeColor=(1, 1, 1, 1))
        # Set initial zoom to 10%
        scale = 1
        self.mesh_item.scale(scale, scale, scale)
        self.mesh_item.setColor(QtGui.QColor(121, 212, 232))  # Set color to red
        self.view.addItem(self.mesh_item)

        # Set initial view to face the xy plane
        self.view.setCameraPosition(distance=2500, azimuth=90, elevation=0)

    def update_rocket_position(self, data):
        if data['timestamp'] % 20 == 0:
            self.pitch = data['gyro'][0] * 10  # Random pitch change
            self.yaw = data['gyro'][2] * 10    # Random yaw change
            self.roll = data['gyro'][1] * 10   # Random roll change
        else:
            self.pitch += data['gyro'][0] * 10  # Random pitch change
            self.yaw += data['gyro'][2] * 10    # Random yaw change
            self.roll += data['gyro'][1] * 10   # Random roll change

        self.mesh_item.resetTransform()
        self.mesh_item.rotate(self.pitch, 1, 0, 0)  # Pitch
        self.mesh_item.rotate(self.yaw, 0, 1, 0)    # Yaw
        self.mesh_item.rotate(self.roll, 0, 0, 1)   # Roll

# Example usage
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    stl_path = "path_to_your_stl_file.stl"
    viewer = RocketViewer(stl_path)
    viewer.show()
    sys.exit(app.exec_())
