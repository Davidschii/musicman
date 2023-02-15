import sys
from glob import glob
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1280,720)
        self.setWindowTitle("Musicman")
        self.song_directory = "music/"

        # Widgets
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.label = QLabel("Song selection:", self)
        self.button_play = QPushButton("Play", self)
        self.songlistbox = QComboBox(self)

        # Layout
        hbl = QHBoxLayout()
        hbl.addWidget(self.label)
        hbl.addWidget(self.songlistbox)

        vbl = QVBoxLayout()
        vbl.addLayout(hbl)
        vbl.addWidget(self.button_play)

        self.setLayout(vbl)
        self.songlist_init()

        # Connections
        self.songname = "Please choose a song!"
        self.songlistbox.activated[str].connect(self.song_change)
        self.button_play.clicked.connect(self.song_play)

        self.show()

    def songlist_init(self):
        start = len(self.song_directory)
        songlist = [self.song_directory + "Please choose a song!"]
        songlist = songlist + glob(self.song_directory + "*.mp3") + glob(self.song_directory + "*.wav") \
                            + glob(self.song_directory + "*.flac")
        for song in songlist:
            self.songlistbox.addItem(song[start:])

    def song_change(self):
        self.songname = str(self.songlistbox.currentText())

    def song_play(self):
        if self.songname != "Please choose a song!":
            song = self.song_directory + self.songname
            print(song)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Player()
    sys.exit(app.exec_())