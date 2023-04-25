from PyQt5.QtWidgets import QApplication, QMainWindow
import pyqtgraph.opengl as gl
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQtGraph 3D Sphere")
        self.setGeometry(0, 0, 800, 600)  # x, y, width, height

        # create an OpenGL widget
        self.widget = gl.GLViewWidget(self)
        self.widget.setCameraPosition(distance=30, elevation=8)

        # create a sphere item
        self.sphere = gl.MeshData.sphere(rows=10, cols=20)
        self.sphere_item = gl.GLMeshItem(
            meshdata=self.sphere, smooth=True, shader='normalColor', color=[1, 0, 0, 1])
        self.widget.addItem(self.sphere_item)

        # add the widget to the main window
        self.setCentralWidget(self.widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
