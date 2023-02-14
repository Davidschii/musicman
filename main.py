import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(1280,720)
        self.setWindowTitle("Musicman")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())
