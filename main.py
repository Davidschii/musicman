import sys
import os
import mutagen
from glob import glob
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.flac import FLAC
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

# changes QMediaPlayer backend
os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'


class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Musicman")
        self.song_directory = "music/"
        self.icon = "assets/icon.png"
        self.songliststart = "Please choose a song."
        self.songname = self.songliststart
        self.musicplayer = QMediaPlayer(self)

        # Widgets
        self.setWindowIcon(QIcon(self.icon))
        self.progressSlider = QSlider(Qt.Horizontal)
        self.label = QLabel("Song selection:", self)
        self.button_play = QPushButton("Play", self)
        self.button_pause = QPushButton("Pause / Resume", self)
        self.button_min = QPushButton("Minimize to tray", self)
        self.songlistbox = QComboBox(self)
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
        self.musicplayer.positionChanged.connect(self.positionupdate)
        self.progressSlider.sliderMoved.connect(self.progress_Slider)

        trayopen.triggered.connect(self.minimize)
        trayexit.triggered.connect(sys.exit)

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
        hours, mins, secs = (self.timeconv(self.length))
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
        self.progressSlider.setRange(0, self.length)
        self.progressSlider.setValue(0)

    def song_play(self):
        try:
            self.musicplayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.song)))
            self.musicplayer.play()
        except AttributeError:
            pass

    def positionupdate(self, position):
        self.position = round(position / 1000)
        hours, mins, secs = self.timeconv(self.position)
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
            self.timelabel1.setText(f"{mins}:{secs}")
        else:
            self.timelabel1.setText(f"{hours}:{mins}:{secs}")
        self.progressSlider.setValue(self.position)

    def progress_Slider(self, position):
        self.musicplayer.setPosition(position * 1000)

    def song_pause(self):
        if self.musicplayer.state() == QMediaPlayer.PlayingState:
            self.musicplayer.pause()
        else:
            self.musicplayer.play()

    def minimize(self):
        if self.isVisible():
            self.trayicon.show()
            self.hide()
        else:
            self.trayicon.hide()
            self.show()

    def timeconv(self, length):
        hours = int(length / 3600)
        minutes = int(length / 60 - hours * 60)
        seconds = round(length - hours * 3600 - minutes * 60)
        return hours, minutes, seconds


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = Player()
    sys.exit(app.exec_())
