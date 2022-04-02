from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QImage, QPainter, QColor
from PyQt5.QtWidgets import QFrame, QPushButton, QWidget, QDialog, QGridLayout, QLabel, QSpacerItem, QSizePolicy
from game.gameClass import Game
from menuClass import Menu
from settingsClass import Settings
from TitleBar import TitleBar
from buttonClasses import BackBtn, RestartBtn
import pygame

class ImageWidget(QWidget):
    def __init__(self, surface, parent=None):
        super(ImageWidget, self).__init__(parent)
        self.w = surface.get_width()
        self.h = surface.get_height()
        self.setGeometry(0, 0, self.w, self.h)
        self.data = surface.get_buffer().raw
        self.image = QImage(self.data, self.w, self.h, QImage.Format_RGB32)

    def update(self, surface):
        self.data = surface.get_buffer().raw
        self.image = QImage(self.data, self.w, self.h, QImage.Format_RGB32)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.drawImage(0, 0, self.image)
        qp.end()

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super(CustomDialog, self).__init__(parent)
        self.width = 500
        self.height = 350 + 30
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.setModal(True)

        self.font = QtGui.QFont('Bahnschrift SemiLight SemiConde')

        self.player_winner = 0
        self.firstScore = 0
        self.secondScore = 0

        self.setupTitleBar()

        self._widget = QFrame(self)
        self._widget.setGeometry(0, 30, self.width, self.height + 30)
        self._widget.setAutoFillBackground(True)
        palette = self._widget.palette()
        palette.setColor(palette.Window, QColor(0, 0, 0))
        self._widget.setPalette(palette)

        self.init_UI()

    def setup(self, s1, s2):
        self.firstScore = s1
        self.secondScore = s2
        if s1 > s2:
            self.player_winner = 1
        else:
            self.player_winner = 2
        self.resultInfo.setText(f'Player №{self.player_winner} - win!')
        self.scoreInfo.setText(
            f'with score: {self.firstScore}:{self.secondScore}')
        self.titleBar.setTitle(
            f'match result - {self.firstScore}:{self.secondScore}')

    def setupTitleBar(self):
        self._pressed = False
        self.Direction = None

        # Фон прозрачный
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Нет границы
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Отслеживание мыши
        self.setMouseTracking(True)

        # Панель заголовка
        self.titleBar = TitleBar(self)
        self.titleBar.buttonMinimum.hide()
        self.titleBar.setGeometry(QtCore.QRect(0, 0, self.width, 30))
        self.titleBar.setTitle('match result - ')
        self.titleBar.setIcon(QtGui.QIcon('game/Images/icon.ico'))

        # слот сигнала
        self.titleBar.windowMinimumed.connect(self.showMinimized)
        self.titleBar.windowClosed.connect(self.close)
        self.titleBar.windowMoved.connect(self.move)

    def init_UI(self):
        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(
            QRect(0, 30, self.width, self.height - 30))

        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayoutWidget.setContentsMargins(10, 10, 10, 10)

        self.resultInfo = QLabel(self.gridLayoutWidget)
        self.resultInfo.setText(f'Player №{self.player_winner} - win!')
        self.font.setPixelSize(38)
        self.resultInfo.setFont(self.font)
        self.resultInfo.setStyleSheet('color: #fff;')
        self.resultInfo.setAlignment(Qt.AlignCenter)
        self.scoreInfo = QLabel(self.gridLayoutWidget)
        self.scoreInfo.setText(f'with score: {self.firstScore}:{self.secondScore}')
        self.font.setPixelSize(24)
        self.scoreInfo.setFont(self.font)
        self.scoreInfo.setStyleSheet('color: #fff;')
        self.scoreInfo.setAlignment(Qt.AlignCenter)

        self.verticalSpacer1 = QSpacerItem(
            0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.tryAgain = QPushButton(self.gridLayoutWidget)
        self.tryAgain.setText('Try again!')
        self.font.setPixelSize(18)
        self.tryAgain.setFont(self.font)
        self.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.tryAgain.setStyleSheet("QPushButton\n"
                            "{\n"
                            "   color: #fff;\n"
                            "   background: #000;\n"
                            "   border: 2px solid #fff;\n"
                            "   padding: 10px 20px;\n"
                            "}\n"
                            "\n"
                            "QPushButton::hover\n"
                            "{\n"
                            "   color: #000;\n"
                            "   background: #fff;\n"
                            "}")

        self.gridLayout.addItem(self.verticalSpacer1, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.resultInfo, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.scoreInfo, 2, 0, 1, 3)
        self.gridLayout.addItem(self.verticalSpacer1, 3, 0, 1, 3)
        self.gridLayout.addWidget(self.tryAgain, 4, 1, 1, 1)
        self.gridLayout.addItem(self.verticalSpacer1, 5, 0, 1, 3)

# Перечислить верхнюю левую, нижнюю правую и четыре неподвижные точки
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)

class MainWindow(QWidget):
    def __init__(self, config):
        super(MainWindow, self).__init__()

        self.config = config
        self.width = self.config['WIDTH']
        self.height = self.config['HEIGHT'] + 30
        self.FPS = self.config['FPS']
        self.setFixedSize(self.width, self.height)
        self.winScore = self.config['WIN_SCORE']
        self.appSoundsVolume = 50
        self.appMusicVolume = 50
        self.musicPlayer = QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile('game/Audios/background_music.mp3')
        content = QMediaContent(url)
        self.musicPlayer.setMedia(content)
        self.musicPlayer.setVolume(self.appMusicVolume)
        self.musicPlayer.stateChanged.connect(self.loopMusic)
        self.musicPlayer.play()

        self.game_result_dialog = CustomDialog()
        self.game_result_dialog.titleBar.buttonClose.clicked.connect(self.go_to_menu)
        self.game_result_dialog.tryAgain.clicked.connect(self.restart_by_modal)

        self.setupTitleBar()

        self._widget = QFrame(self)
        self._widget.setGeometry(0, 30, self.width, self.height + 30)
        self._widget.setAutoFillBackground(True)
        palette = self._widget.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        self._widget.setPalette(palette)
        self._widget.installEventFilter(self)

        self.init_UI()
        self.setAudioVolume()

    def setupTitleBar(self):
        self._pressed = False
        self.Direction = None

        # Нет границы
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Отслеживание мыши
        self.setMouseTracking(True)

        # Панель заголовка
        self.titleBar = TitleBar(self)
        self.titleBar.setGeometry(QtCore.QRect(0, 0, self.width, 30))
        self.titleBar.setTitle('Table Tennis, v1.1')
        self.titleBar.setIcon(QtGui.QIcon('game/Images/icon.ico'))

        # слот сигнала
        self.titleBar.windowMinimumed.connect(self.showMinimized)
        self.titleBar.windowClosed.connect(self.close)
        self.titleBar.windowMoved.connect(self.move)

    def init_UI(self):
        self.mainMenu = Menu((self.width, self.height - 30), 30, 200, 60, self._widget)

        self.mainMenu.PlayBtn1.clicked.connect(self.start_1P_game)
        self.mainMenu.PlayBtn2.clicked.connect(self.start_2P_game)
        self.mainMenu.SettingsBtn.clicked.connect(self.show_settings)

        self.settingsFrame = Settings((self.width, self.height - 30), self._widget)

        self.settingsFrame.backBtn.clicked.connect(self.go_to_menu)
        self.settingsFrame.audio_settings.SoundVolume.valueChanged.connect(
            self.soundScrollChanged)
        self.settingsFrame.audio_settings.soundCheckBox.stateChanged.connect(
            self.setSoundPanelVisible)
        self.settingsFrame.audio_settings.MusicVolume.valueChanged.connect(
            self.musicScrollChanged)
        self.settingsFrame.audio_settings.musicCheckBox.stateChanged.connect(
            self.setMusicPanelVisible)

        self.settingsFrame.hide()

        self.game_frame = QFrame(self._widget)
        self.game_frame.setGeometry(0, 0, self.width, self.height - 30)
        self.game_frame.hide()

        self.game_surface = pygame.Surface((self.width, self.height - 30))
        self.game = Game(self.game_surface, self.config)

        self.img = ImageWidget(self.game_surface, self.game_frame)

        self.btn_back = BackBtn('', self.game_frame)
        self.btn_back.setGeometry(self.width - 80, 10, 70, 70)
        self.btn_back.clicked.connect(self.go_to_menu)

        self.btn_restart = RestartBtn('', self.game_frame)
        self.btn_restart.setGeometry(self.width - 160, 10, 70, 70)
        self.btn_restart.clicked.connect(self.restart_game)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)

    def setAudioVolume(self):
        self.mainMenu.PlayBtn1.setVolume(self.appSoundsVolume)
        self.mainMenu.PlayBtn2.setVolume(self.appSoundsVolume)
        self.mainMenu.SettingsBtn.setVolume(self.appSoundsVolume)

        self.settingsFrame.backBtn.setVolume(self.appSoundsVolume)
        self.settingsFrame.audio_settings.SoundVolume.setVolume(
            self.appSoundsVolume)
        self.settingsFrame.audio_settings.soundCheckBox.setVolume(
            self.appSoundsVolume)
        self.settingsFrame.audio_settings.MusicVolume.setVolume(
            self.appSoundsVolume)
        self.settingsFrame.audio_settings.musicCheckBox.setVolume(
            self.appSoundsVolume)

        self.btn_back.setVolume(self.appSoundsVolume)
        self.btn_restart.setVolume(self.appSoundsVolume)

        self.game.set_volume(self.appSoundsVolume)

    def soundScrollChanged(self):
        self.appSoundsVolume = self.settingsFrame.audio_settings.SoundVolume.value() * 10
        self.setAudioVolume()

    def setSoundPanelVisible(self):
        if self.settingsFrame.audio_settings.soundCheckBox.isChecked():
            self.appSoundsVolume = self.settingsFrame.audio_settings.SoundVolume.value() * 10
        else:
            self.appSoundsVolume = 0
        self.setAudioVolume()

    def musicScrollChanged(self):
        self.appMusicVolume = self.settingsFrame.audio_settings.MusicVolume.value() * 10
        self.musicPlayer.setVolume(self.appMusicVolume)

    def setMusicPanelVisible(self):
        if self.settingsFrame.audio_settings.musicCheckBox.isChecked():
            self.appMusicVolume = self.settingsFrame.audio_settings.MusicVolume.value() * 10
            self.musicPlayer.setVolume(self.appMusicVolume)
        else:
            self.appMusicVolume = 0
            self.musicPlayer.setVolume(0)

    def loopMusic(self):
        if not self.musicPlayer.state():
            self.musicPlayer.play()

    def move(self, pos):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # Максимизировать или полноэкранный режим не допускается
            return
        super(MainWindow, self).move(pos)

    def mousePressEvent(self, event):
        """ Событие клика мыши """
        super(MainWindow, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._mpos = event.pos()
            self._pressed = True

    def mouseReleaseEvent(self, event):
        ''' Событие отказов мыши '''
        super(MainWindow, self).mouseReleaseEvent(event)
        self._pressed = False
        self.Direction = None

    def start_1P_game(self, event):
        self.mainMenu.hide()

        self.game_frame.show()

        self.game.numderOfPlayers = 1

        self.startTimer()

    def start_2P_game(self, event):
        self.mainMenu.hide()

        self.game_frame.show()

        self.game.numderOfPlayers = 2

        self.startTimer()

    def go_to_menu(self, event):
        self.game_frame.hide()
        self.settingsFrame.hide()

        self.mainMenu.show()
        self.game.setup_settings()

        self.stopTimer()

    def restart_game(self):
        self.game.setup_settings()

    def show_settings(self, event):
        self.mainMenu.hide()

        self.settingsFrame.show()

    def update_game(self):
        self.img.update(self.game.rend_display())
        self.game_frame.update()

        if self.game.firstPlayerScore == self.winScore:
            self.game_result_dialog.setup(
                self.game.firstPlayerScore, self.game.secondPlayerScore)
            self.stopTimer()
            self.img.update(self.game.rend_display())
            self.game_frame.update()
            self.game_result_dialog.exec_()
        elif self.game.secondPlayerScore == self.winScore:
            self.game_result_dialog.setup(
                self.game.firstPlayerScore, self.game.secondPlayerScore)
            self.stopTimer()
            self.img.update(self.game.rend_display())
            self.game_frame.update()
            self.game_result_dialog.exec_()

    def restart_by_modal(self):
        self.game_result_dialog.close()
        self.startTimer()
        self.restart_game()

    def startTimer(self):
        self.timer.start(1000 // self.FPS)

    def stopTimer(self):
        self.timer.stop()

    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            if event.key() == QtCore.Qt.Key_Down:
                self.game.keys['IS_KEY_DOWN_DOWN'] = True
            if event.key() == QtCore.Qt.Key_Up:
                self.game.keys['IS_KEY_UP_DOWN'] = True
            if event.nativeVirtualKey() == QtCore.Qt.Key_W:
                self.game.keys['IS_KEY_W_DOWN'] = True
            if event.nativeVirtualKey() == QtCore.Qt.Key_S:
                self.game.keys['IS_KEY_S_DOWN'] = True

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            if event.key() == QtCore.Qt.Key_Down:
                self.game.keys['IS_KEY_DOWN_DOWN'] = False
            if event.key() == QtCore.Qt.Key_Up:
                self.game.keys['IS_KEY_UP_DOWN'] = False
            if event.nativeVirtualKey() == QtCore.Qt.Key_W:
                self.game.keys['IS_KEY_W_DOWN'] = False
            if event.nativeVirtualKey() == QtCore.Qt.Key_S:
                self.game.keys['IS_KEY_S_DOWN'] = False
