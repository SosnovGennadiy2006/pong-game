from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QSizePolicy,
    QTabWidget, QWidget, QGridLayout, QSpacerItem)
from PyQt5.QtGui import QFont
from buttonClasses import BackBtn, CustomCheckBox, CustomSlider
from PyQt5.QtCore import Qt, QRect

class AudioSettings(QWidget):
    def __init__(self, w, parent=None):
        super(AudioSettings, self).__init__(parent)
        self.font = QFont('Bahnschrift SemiLight SemiConde')
        self.width = w

        self.init_UI()

    def init_UI(self):
        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(
            QRect(0, 0, self.width, 200))

        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayoutWidget.setContentsMargins(10, 10, 10, 10)

        #Настройки для звука:

        self.label1 = QLabel(self.gridLayoutWidget)
        self.label1.setText('Play Sounds?')
        self.font.setPixelSize(16)
        self.label1.setFont(self.font)
        self.label1.setStyleSheet('color: #fff;')

        self.horizontalSpacer = QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.soundCheckBox = CustomCheckBox(self.gridLayoutWidget)
        self.soundCheckBox.setFont(self.font)

        self.gridLayout.addWidget(self.label1, 0, 0, 1, 1)
        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.soundCheckBox, 0, 2, 1, 1)

        self.label2 = QLabel(self.gridLayoutWidget)
        self.label2.setText('Volume: 5')
        self.font.setPixelSize(16)
        self.label2.setFont(self.font)
        self.label2.setStyleSheet('color: #fff;')

        self.SoundVolume = CustomSlider(self.gridLayoutWidget)
        self.SoundVolume.setMaximum(10)
        self.SoundVolume.setSliderPosition(5)

        self.gridLayout.addWidget(self.label2, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.SoundVolume, 1, 1, 1, 2)

        self.verticalSpacer1 = QSpacerItem(
            0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalSpacer1.changeSize(0, 24)

        self.gridLayout.addItem(self.verticalSpacer1, 2, 0, 1, 3)

        #Настройки для музыки:

        self.label3 = QLabel(self.gridLayoutWidget)
        self.label3.setText('Play Music?')
        self.font.setPixelSize(16)
        self.label3.setFont(self.font)
        self.label3.setStyleSheet('color: #fff;')

        self.musicCheckBox = CustomCheckBox(self.gridLayoutWidget)
        self.musicCheckBox.setFont(self.font)

        self.gridLayout.addWidget(self.label3, 3, 0, 1, 1)
        self.gridLayout.addItem(self.horizontalSpacer, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.musicCheckBox, 3, 2, 1, 1)

        self.label4 = QLabel(self.gridLayoutWidget)
        self.label4.setText('Volume: 5')
        self.font.setPixelSize(16)
        self.label4.setFont(self.font)
        self.label4.setStyleSheet('color: #fff;')

        self.MusicVolume = CustomSlider(self.gridLayoutWidget)
        self.MusicVolume.setMaximum(10)
        self.MusicVolume.setSliderPosition(5)

        self.gridLayout.addWidget(self.label4, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.MusicVolume, 4, 1, 1, 2)

        self.verticalSpacer3 = QSpacerItem(
            0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer3, 6, 0, 1, 3)

class Settings(QFrame):
    def __init__(self, size, parent=None):
        super(Settings, self).__init__(parent)
        self.width = size[0]
        self.height = size[1]
        self.setGeometry(0, 0, self.width, self.height)

        self.font = QFont('Bahnschrift SemiLight SemiConde')
        self.sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)

        self.init_UI()

    def init_UI(self):
        self.setStyleSheet('background: #000;')

        self.layout_widget = QFrame(self)
        self.layout_widget.setGeometry(QRect(0, 0, self.width, self.height))

        self.layout = QVBoxLayout(self.layout_widget)
        self.layout.setContentsMargins(10, 10, 10, 0)

        self.name = QLabel(self)
        self.name.setText('Settings')
        self.font.setPixelSize(34)
        self.name.setFont(self.font)
        self.name.setStyleSheet('color: #fff;')
        self.name.setSizePolicy(self.sizePolicy)
        self.name.setAlignment(Qt.AlignCenter)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setFixedWidth(self.layout_widget.width() - 20)
        self.audio_settings = AudioSettings(self.tabWidget.width())
        self.gameplay_settings = QWidget()
        self.grafics_settings = QWidget()
        self.tabWidget.addTab(self.audio_settings, 'Audios settings')
        self.tabWidget.addTab(self.gameplay_settings, 'Gameplay settings')
        self.tabWidget.addTab(self.grafics_settings, 'Grafics settings')
        self.font.setPixelSize(18)
        self.tabWidget.setFont(self.font)
        self.tabWidget.tabBar().setCursor(Qt.PointingHandCursor)
        self.tabWidget.setStyleSheet(
            'QTabWidget::pane {\n'
            '    border: 1px solid #fff;\n'
            '}\n'
            'QTabBar::tab {\n'
            '    border: 1px solid #fff;\n'
            '    border-bottom-color: #fff;\n'
            '    border-left-color: #222;\n'
            '    border-right-color: #222;\n'
            '    background: #fff;\n'
            '    margin-left: -1px;\n'
            '    margin-right: -1px;\n'
            '    color: #000;\n'
            '    padding: 0px 20px;\n'
            '}\n'
            'QTabBar::tab:first{\n'
            '    border-left-color: #fff;\n'
            '    margin: 0px;\n'
            '}\n'
            'QTabBar::tab:last{\n'
            '    border-right-color: #fff;\n'
            '    margin: 0px;\n'
            '}\n'
            'QTabBar::tab:hover{\n'
            '    background: #DDD;\n'
            '}\n'
            'QTabBar::tab:selected{\n'
            '    background: #000;\n'
            '    border-bottom-color: #000;\n'
            '    color: #fff;\n'
            '}\n'
            'QTabBar::tab:!selected {\n'
            '    margin-top: 2px; /* make non-selected tabs look smaller */\n'
            '}\n'
        )

        self.audio_settings.SoundVolume.valueChanged.connect(
            self.soundScrollChanged)
        self.audio_settings.soundCheckBox.stateChanged.connect(
            self.setSoundPanelVisible)
        self.audio_settings.MusicVolume.valueChanged.connect(
            self.musicScrollChanged)
        self.audio_settings.musicCheckBox.stateChanged.connect(
            self.setMusicPanelVisible)

        self.layout.addWidget(self.name)
        self.layout.addWidget(self.tabWidget)
        self.layout.addStretch()

        self.backBtn = BackBtn('', self)
        self.backBtn.setGeometry(self.width - 80, 10, 70, 70)

    def soundScrollChanged(self):
        self.audio_settings.label2.setText('Volume: ' + str(self.audio_settings.SoundVolume.value()))

    def setSoundPanelVisible(self):
        if self.audio_settings.soundCheckBox.isChecked():
            self.audio_settings.label2.show()
            self.audio_settings.SoundVolume.show()
        else:
            self.audio_settings.label2.hide()
            self.audio_settings.SoundVolume.hide()

    def musicScrollChanged(self):
        self.audio_settings.label4.setText(
            'Volume: ' + str(self.audio_settings.MusicVolume.value()))

    def setMusicPanelVisible(self):
        if self.audio_settings.musicCheckBox.isChecked():
            self.audio_settings.label4.show()
            self.audio_settings.MusicVolume.show()
        else:
            self.audio_settings.label4.hide()
            self.audio_settings.MusicVolume.hide()
