import sys
import mutagen
import pygame
from glob import glob
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.flac import FLAC
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaObject


class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Musicman")
        self.song_directory = "music/"
        self.icon = "assets/icon.png"
        self.songliststart = "Please choose a song."
        self.songname = self.songliststart
        pygame.mixer.init()

        # Widgets
        self.setWindowIcon(QIcon(self.icon))
        self.label = QLabel("Song selection:", self)
        self.button_play = QPushButton("Play", self)
        self.button_pause = QPushButton("Pause / Resume", self)
        self.button_min = QPushButton("Minimize to tray", self)
        self.songlistbox = QComboBox(self)
        self.progressSlider = QSlider(Qt.Horizontal)
        self.timelabel1 = QLabel("00:00", self)
        self.timelabel2 = QLabel("00:00", self)

        # Tray
        self.trayicon = QSystemTrayIcon(QIcon(self.icon))
        self.trayicon.setToolTip("Musicman")
        traymenu = QMenu()
        trayopen = traymenu.addAction("Open")
        trayexit = traymenu.addAction("Exit")
        self.trayicon.setContextMenu(traymenu)

        # Songlist
        start = len(self.song_directory)
        songlist = [self.song_directory + self.songliststart]
        songlist = songlist + glob(self.song_directory + "*.mp3") + glob(self.song_directory + "*.wav") \
                            + glob(self.song_directory + "*.flac")
        for song in songlist:
            self.songlistbox.addItem(song[start:])

        # Layout
        hbl = QHBoxLayout()
        hbl.addWidget(self.label)
        hbl.addWidget(self.songlistbox)

        hbl2 = QHBoxLayout()
        hbl2.addWidget(self.timelabel1)
        hbl2.addWidget(self.progressSlider)
        hbl2.addWidget(self.timelabel2)


        hbl3 = QHBoxLayout()
        hbl3.addWidget(self.button_play)
        hbl3.addWidget(self.button_pause)

        vbl = QVBoxLayout()
        vbl.addLayout(hbl)
        vbl.addLayout(hbl2)
        vbl.addLayout(hbl3)
        vbl.addWidget(self.button_min)

        self.setLayout(vbl)

        # Connections
        self.songlistbox.activated[str].connect(self.song_change)
        self.button_play.clicked.connect(self.song_play)
        self.button_pause.clicked.connect(self.song_pause)
        self.button_min.clicked.connect(self.minimize)

        trayopen.triggered.connect(self.minimize)
        trayexit.triggered.connect(self.stop)

        self.show()

    def song_change(self):
        self.songname = str(self.songlistbox.currentText())
        if self.songname != self.songliststart:
            self.song = self.song_directory + self.songname
        try:
            if self.song[-3:] == "mp3":
                audio = MP3(self.song)
            elif self.song[-3:] == "wav":
                audio = WAVE(self.song)
            elif self.song[-4:] == "flac":
                audio = FLAC(self.song)
            audio_info = audio.info
            self.length = int(audio_info.length)
        except mutagen.MutagenError:
            self.length = 0
        self.progressSlider.setRange(0, self.length)
        self.progressSlider.setValue(0)
        hours, mins, secs = (self.lengthconv(self.length))
        hours = str(hours)
        mins = str(mins)
        secs = str(secs)
        if len(hours) == 1:
            hours = "0" + hours
        if len(mins) == 1:
            mins = "0" + mins
        if len(secs) == 1:
            secs = "0" + secs
        if hours == "00":
            self.timelabel2.setText(f"{mins}:{secs}")
        else:
            self.timelabel2.setText(f"{hours}:{mins}:{secs}")


    def song_play(self):
        try:
            pygame.mixer.music.load(self.song)
            pygame.mixer.music.play()
        except pygame.error:
            pass
        except AttributeError:
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
        sys.exit()

    def lengthconv(self, length):
        hours = int(length / 3600)
        minutes = int(length / 60)
        seconds = length - minutes*60
        return hours, minutes, seconds

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = Player()
    sys.exit(app.exec_())
