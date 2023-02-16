import sys
import pygame
from glob import glob
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Musicman")
        self.song_directory = "music/"
        self.icon = "assets/icon.png"
        pygame.mixer.init()

        # Tray Icon
        self.trayicon = QSystemTrayIcon(QIcon(self.icon))
        self.trayicon.setToolTip("Musicman")
        traymenu = QMenu()
        trayopen = traymenu.addAction("Open")
        trayexit = traymenu.addAction("Exit")
        self.trayicon.setContextMenu(traymenu)

        # Widgets
        self.setWindowIcon(QIcon(self.icon))
        self.label = QLabel("Song selection:", self)
        self.button_play = QPushButton("Play", self)
        self.button_pause = QPushButton("Pause / Resume", self)
        self.button_min = QPushButton("Minimize to tray", self)
        self.songlistbox = QComboBox(self)

        # Layout
        hbl = QHBoxLayout()
        hbl.addWidget(self.label)
        hbl.addWidget(self.songlistbox)

        hbl2 = QHBoxLayout()
        hbl2.addWidget(self.button_play)
        hbl2.addWidget(self.button_pause)

        vbl = QVBoxLayout()
        vbl.addLayout(hbl)
        vbl.addLayout(hbl2)
        vbl.addWidget(self.button_min)

        self.setLayout(vbl)
        self.songlist_init()

        # Connections
        self.songname = "Please choose a song!"
        self.songlistbox.activated[str].connect(self.song_change)
        self.button_play.clicked.connect(self.song_play)
        self.button_pause.clicked.connect(self.song_pause)
        self.button_min.clicked.connect(self.minimize)
        trayopen.triggered.connect(self.minimize)
        trayexit.triggered.connect(self.stop)
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

    def minimize(self):
        if self.isVisible():
            self.trayicon.show()
            self.hide()
        else:
            self.trayicon.hide()
            self.show()

    def stop(self):
        pygame.mixer.quit()
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = Player()
    sys.exit(app.exec_())
