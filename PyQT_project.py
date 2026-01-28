import sys
import os
import random, time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QTimer
from pygame import mixer
from mutagen.mp3 import MP3

musicList = []
mixer.init()
muted = False
count = 0
songLength = 0
index = 0


def groupboxStyle():
    return """
       QGroupBox {
       background-color:red;
       font:15pt Times Bold;
       color:white;
       border:2px solid gray;
       border-radius:15px;
       }
   """


def progressBarStyle():
    return """
       QProgressBar{
       border: 1px solid #bbb;
       background: white;
       height:10px;
       border-radius:6px;

       }

   """


def playListStyle():
    return """
       QListWidget{
           background-color:#fff;
           border-radius: 10px;
           border: 3px solid blue;
       }

   """


class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.setGeometry(450, 150, 480, 700)
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)
        self.progressBar.setStyleSheet(progressBarStyle())

        # Labels
        self.songTimerLabel = QLabel("0:00")
        self.songLengthLabel = QLabel("/ 0:00")
        # buttons
        self.addButton = QToolButton()
        self.addButton.setIcon(QIcon("icons/arrow_basic_e.svg"))
        self.addButton.setIconSize(QSize(48, 48))
        self.addButton.setToolTip("Add a song")
        self.addButton.clicked.connect(self.addSound)

        self.shuffleButton = QToolButton()
        self.shuffleButton.setIcon(QIcon("icons/arrow_basic_e_small.svg"))
        self.shuffleButton.setIconSize(QSize(48, 48))
        self.shuffleButton.setToolTip("Shuffle the list")
        self.shuffleButton.clicked.connect(self.shufflePlayList)

        self.previousButton = QToolButton()
        self.previousButton.setIcon(QIcon("icons/arrow_basic_e_small.svg"))
        self.previousButton.setIconSize(QSize(48, 48))
        self.previousButton.setToolTip("Play Previous")
        self.previousButton.clicked.connect(self.playPrevious)

        self.playButton = QToolButton()
        self.playButton.setIcon(QIcon("icons/arrow_basic_e_small.svg"))
        self.playButton.setIconSize(QSize(48, 48))
        self.playButton.setToolTip("Play")
        self.playButton.clicked.connect(self.playSounds)

        self.playNextButton = QToolButton()
        self.playNextButton.setIcon(QIcon("icons/arrow_basic_e_small.svg"))
        self.playNextButton.setIconSize(QSize(48, 48))
        self.playNextButton.setToolTip("Play Next")
        self.playNextButton.clicked.connect(self.playNext)

        self.muteButton = QToolButton()
        self.muteButton.setIcon(QIcon("icons/arrow_basic_e_small.svg"))
        self.muteButton.setIconSize(QSize(48, 48))
        self.muteButton.setToolTip("Mute")
        self.muteButton.clicked.connect(self.muteSound)

        # volume slider
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setToolTip("Volume")
        self.volumeSlider.setValue(70)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        mixer.music.set_volume(0.7)
        self.volumeSlider.valueChanged.connect(self.setVolume)

        # playlist
        self.playList = QListWidget()
        self.playList.doubleClicked.connect(self.playSounds)
        self.playList.setStyleSheet(playListStyle())

        # Timer
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updatePrograssBar)

    def layouts(self):
        # creating layouts
        self.mainLayout = QVBoxLayout()
        self.topMainLayout = QVBoxLayout()
        self.topGroupBox = QGroupBox("MusicPlayer")
        self.topGroupBox.setStyleSheet(groupboxStyle())
        self.topLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.bottomLayout = QVBoxLayout()

        # adding widgets

        # top layout widgets

        self.topLayout.addWidget(self.progressBar)
        self.topLayout.addWidget(self.songTimerLabel)
        self.topLayout.addWidget(self.songLengthLabel)
        self.topMainLayout.addLayout(self.topLayout)
        self.topMainLayout.addLayout(self.middleLayout)
        self.topGroupBox.setLayout(self.topMainLayout)
        self.mainLayout.addWidget(self.topGroupBox, 25)
        self.mainLayout.addLayout(self.bottomLayout, 75)
        self.setLayout(self.mainLayout)

        # middle layout widgets
        self.middleLayout.addStretch()
        self.middleLayout.addWidget(self.addButton)
        self.middleLayout.addWidget(self.shuffleButton)
        self.middleLayout.addWidget(self.previousButton)
        self.middleLayout.addWidget(self.playButton)
        self.middleLayout.addWidget(self.playNextButton)
        self.middleLayout.addWidget(self.volumeSlider)
        self.middleLayout.addWidget(self.muteButton)
        self.middleLayout.addStretch()

        # bottom layout widget
        self.bottomLayout.addWidget(self.playList)

    def addSound(self):
        directory = QFileDialog.getOpenFileName(self, "Add Sound", "", "Sound Files (*.mp3 *.ogg *.wav)")
        # print(directory)
        filename = os.path.basename(directory[0])
        # print(filename)
        self.playList.addItem(filename)
        musicList.append(directory[0])

    def shufflePlayList(self):
        random.shuffle(musicList)
        print(musicList)
        self.playList.clear()
        for song in musicList:
            filename = os.path.basename(song)
            self.playList.addItem(filename)

    def playSounds(self):
        global songLength
        global count
        global index
        index = self.playList.currentRow()
        print(index)
        print(musicList[index])
        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()

            sound = MP3(str(musicList[index]))
            songLength = round(sound.info.length)
            print(songLength)
            min, sec = divmod(songLength, 60)
            self.songLengthLabel.setText("/ " + str(min) + ":" + str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)
        except:
            pass

    def setVolume(self):
        self.volume = self.volumeSlider.value()
        # print(self.volume)
        mixer.music.set_volume(self.volume / 100)

    def muteSound(self):
        global muted
        if muted == False:
            mixer.music.set_volume(0.0)
            muted = True
            self.muteButton.setIcon(QIcon("icons/arrow_basic_e.svg"))
            self.muteButton.setToolTip("UnMute")
            self.volumeSlider.setValue(0)
            print("ok")
        else:
            print("not ok")
            mixer.music.set_volume(0.7)
            muted = False
            self.muteButton.setToolTip("Mute")
            self.muteButton.setIcon(QIcon("icons/arrow_basic_e.svg"))
            self.volumeSlider.setValue(70)

    def updatePrograssBar(self):
        global count
        global songLength
        count += 1
        self.progressBar.setValue(count)
        self.songTimerLabel.setText(time.strftime("%M:%S", time.gmtime(count)))
        if count >= songLength:
            self.timer.stop()
            count = 0

    def playPrevious(self):
        global songLength
        global count
        global index
        items = self.playList.count()
        if index == 0:
            index = items
        print(index)
        index -= 1
        print(index)

        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()

            sound = MP3(str(musicList[index]))
            songLength = round(sound.info.length)
            print(songLength)
            min, sec = divmod(songLength, 60)
            self.songLengthLabel.setText("/ " + str(min) + ":" + str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)
        except:
            pass

    def playNext(self):
        global songLength
        global count
        global index
        items = self.playList.count()
        index += 1
        if index == items:
            index = 0

        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()

            sound = MP3(str(musicList[index]))
            songLength = round(sound.info.length)
            print(songLength)
            min, sec = divmod(songLength, 60)
            self.songLengthLabel.setText("/ " + str(min) + ":" + str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)
        except:
            pass


def main():
    App = QApplication(sys.argv)
    window = Player()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()

