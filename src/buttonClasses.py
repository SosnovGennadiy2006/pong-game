from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QPushButton
import os

click_media_player = QMediaPlayer()
url = QtCore.QUrl.fromLocalFile('game/Audios/clickSound.mp3')
content = QMediaContent(url)
click_media_player.setMedia(content)

class CustomSlider(QtWidgets.QSlider):
    def __init__(self, parent=None):
        super(CustomSlider, self).__init__(parent)
        self.setOrientation(Qt.Horizontal)
        self.setToolTip(str(self.value()))
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setFocusPolicy(Qt.NoFocus)
        self.click_media = QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile('game/Audios/clickSound.mp3')
        content = QMediaContent(url)
        self.click_media.setMedia(content)

        self.setStyleSheet(
            'QSlider::groove{\n'
            '   background: #fff;\n'
            '   height: 2px;'
            '   margin: 10px 0;\n'
            '}\n'
            'QSlider::handle{\n'
            '   background: #fff;\n'
            '   width: 10px;\n'
            '   height: 30px;\n'
            '   margin: -10px 0;\n'
            '}\n'
            'QSlider::handle:hover{\n'
            '   background: #ccc;\n'
            '   width: 10px;\n'
            '   height: 30px;\n'
            '   margin: -15px 0;\n'
            '}\n'
            'QSlider::handle:pressed{\n'
            '   background: #b3b3b3;\n'
            '   width: 10px;\n'
            '   height: 30px;\n'
            '   margin: -15px 0;\n'
            '}\n'
        )

        self.sliderReleased.connect(self.onRelease)
        self.valueChanged.connect(self.onChanged)

    def onRelease(self):
        self.click_media.play()
        self.setToolTip(str(self.value()))

    def onChanged(self):
        self.setToolTip(str(self.value()))

    def setVolume(self, volume):
        self.click_media.setVolume(volume)

class CustomCheckBox(QtWidgets.QCheckBox):
    def __init__(self, parent=None):
        super(CustomCheckBox, self).__init__(parent)
        self.setStyleSheet('color: #fff;')
        self.setText('yes')
        self.setChecked(True)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setFocusPolicy(Qt.NoFocus)
        self.click_media = click_media_player

        self.stateChanged.connect(self.togleText)

    def togleText(self, e):
        click_media_player.play()
        if not self.isChecked():
            self.setText('no')
        else:
            self.setText('yes')

    def setVolume(self, volume):
        self.click_media.setVolume(volume)

class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super(CustomButton, self).__init__(text, parent)
        self.select_media_player = QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile('game/Audios/selectSound.mp3')
        content = QMediaContent(url)
        self.select_media_player.setMedia(content)
        path_image = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), "game/Images/backgroundImage.png").replace("\\", "/")
        path_image_active = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), "game/Images/backgroundImageActive.png").replace("\\", "/")
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet("QPushButton\n"
                           "{\n"
                           f"    border-image: url({path_image});\n"
                           "    color: #fff;\n"
                           "}\n"
                           "\n"
                           "QPushButton::hover\n"
                           "{\n"
                           "    color: #000;\n"
                           f"    border-image: url({path_image_active});\n"
                           "}")
        font = QtGui.QFont('Bahnschrift SemiLight SemiConde')
        font.setPointSize(28)
        self.setFont(font)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.click_media = QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile('game/Audios/clickSound.mp3')
        content = QMediaContent(url)
        self.click_media = QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile('game/Audios/clickSound.mp3')
        content = QMediaContent(url)
        self.click_media.setMedia(content)

        self.clicked.connect(self.onClick)

    def onClick(self, e):
        click_media_player.play()

    def enterEvent(self, e):
        self.select_media_player.play()

    def setVolume(self, volume):
        self.click_media.setVolume(volume)
        self.select_media_player.setVolume(volume)

class SquareBtn(QPushButton):
    def __init__(self, text, parent):
        super(SquareBtn, self).__init__(text, parent)

        self.select_media_player = QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile('game/Audios/selectSound.mp3')
        content = QMediaContent(url)
        self.select_media_player.setMedia(content)

        path = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), "game/Images/backgroundImageSquare.png").replace("\\", "/")
        activePath = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), "game/Images/backgroundImageSquareActive.png").replace("\\", "/")
        self.setStyleSheet("QPushButton\n"
                           "{\n"
                           f"    border-image: url({path});"
                           "    color: #fff;\n"
                           "}\n"
                           "\n"
                           "QPushButton::hover\n"
                           "{\n"
                           f"    border-image: url({activePath});"
                           "    color: #000;\n"
                           "}")
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.click_media = QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile('game/Audios/clickSound.mp3')
        content = QMediaContent(url)
        self.click_media.setMedia(content)

        self.clicked.connect(self.onClick)

    def onClick(self, e):
        click_media_player.play()

    def setVolume(self, volume):
        self.select_media_player.setVolume(volume)
        self.click_media.setVolume(volume)

class BackBtn(SquareBtn):
    def __init__(self, text='', parent=None):
        super(BackBtn, self).__init__(text, parent)
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.4)
        self.setGraphicsEffect(self.opacity_effect)
        self.setIcon(QtGui.QIcon('game/Images/backWhite.png'))
        self.setIconSize(QtCore.QSize(50, 50))
        self.setToolTip('<b>To menu</b>')

    def enterEvent(self, e):
        self.select_media_player.play()
        self.opacity_effect.setOpacity(1)
        self.setGraphicsEffect(self.opacity_effect)
        self.setIcon(QtGui.QIcon('game/Images/backBlack.png'))
        self.setIconSize(QtCore.QSize(50, 50))

    def leaveEvent(self, e):
        self.opacity_effect.setOpacity(0.4)
        self.setGraphicsEffect(self.opacity_effect)
        self.setIcon(QtGui.QIcon('game/Images/backWhite.png'))
        self.setIconSize(QtCore.QSize(50, 50))

class RestartBtn(SquareBtn):
    def __init__(self, text='', parent=None):
        super(RestartBtn, self).__init__(text, parent)
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.4)
        self.setGraphicsEffect(self.opacity_effect)
        self.setIcon(QtGui.QIcon('game/Images/againWhite.png'))
        self.setIconSize(QtCore.QSize(50, 50))
        self.setToolTip('<b>Restart</b>')

    def enterEvent(self, e):
        self.select_media_player.play()
        self.opacity_effect.setOpacity(1)
        self.setGraphicsEffect(self.opacity_effect)
        self.setIcon(QtGui.QIcon('game/Images/againBlack.png'))
        self.setIconSize(QtCore.QSize(50, 50))

    def leaveEvent(self, e):
        self.opacity_effect.setOpacity(0.4)
        self.setGraphicsEffect(self.opacity_effect)
        self.setIcon(QtGui.QIcon('game/Images/againWhite.png'))
        self.setIconSize(QtCore.QSize(50, 50))
