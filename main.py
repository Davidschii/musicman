import sys
import pygame
from glob import glob
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Player(QWidget):
    def __init__(self):
        super().__init__()
#        self.resize(1280,720)
        self.setWindowTitle("Musicman")
        self.song_directory = "music/"
        pygame.mixer.init()

        # Widgets
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.label = QLabel("Song selection:", self)
        self.button_play = QPushButton("Play", self)
        self.button_pause = QPushButton("Pause / Resume", self)
        self.songlistbox = QComboBox(self)

        # Layout
        hbl = QHBoxLayout()
        hbl.addWidget(self.label)
        hbl.addWidget(self.songlistbox)

        vbl = QVBoxLayout()
        vbl.addLayout(hbl)
        vbl.addWidget(self.button_play)
        vbl.addWidget(self.button_pause)

        self.setLayout(vbl)
        self.songlist_init()

        # Connections
        self.songname = "Please choose a song!"
        self.songlistbox.activated[str].connect(self.song_change)
        self.button_play.clicked.connect(self.song_play)
        self.button_pause.clicked.connect(self.song_pause)

        self.show()

    def songlist_init(self):
        start = len(self.song_directory)
        songlist = [self.song_directory + "Please choose a song!"]
        songlist = songlist + glob(self.song_directory + "*.mp3") + glob(self.song_directory + "*.wav") \
                           + glob(self.song_directory + "*.flac") + glob(self.song_directory + "*.ogg")
        for song in songlist:
            self.songlistbox.addItem(song[start:])

    def song_change(self):
        self.songname = str(self.songlistbox.currentText())

    def song_play(self):
        if self.songname != "Please choose a song!":
            song = self.song_directory + self.songname
            try:
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
            except pygame.error:
                pass

    def song_pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = Player()
    sys.exit(app.exec_())