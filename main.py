import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(qtg.QIcon('cortex.ico'))
        self.setWindowTitle("Hello, icon not working?")
        self.show()


app = qtw.QApplication([])
mw = MainWindow()
app.exec_()
