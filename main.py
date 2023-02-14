import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class Player(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(1280,720)
        self.setWindowTitle("Musicman")

        # Widgets
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.button_play = QPushButton("Play", self)
        self.songdir = QLineEdit(self)

        # Layout
        hbl = QHBoxLayout()
        hbl.addWidget(self.button_play)

        vbl = QVBoxLayout()
        vbl.addWidget(self.songdir)
        vbl.addLayout(hbl)

        self.setLayout(vbl)

        # Connections
        self.songdir.returnPressed.connect(self.songplay)
        self.button_play.clicked.connect(self.songplay)

        self.show()

    def songplay(self):
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Player()
    sys.exit(app.exec_())
