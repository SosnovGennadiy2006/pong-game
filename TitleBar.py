from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel,
                             QSpacerItem, QSizePolicy, QPushButton)

class TitleBar(QWidget):
    # Сигнал минимизации окна
    windowMinimumed = pyqtSignal()
    # сигнал закрытия окна
    windowClosed = pyqtSignal()
    # Окно мобильных
    windowMoved = pyqtSignal(QPoint)

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        # Поддержка настройки фона qss
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background: #3c3c3c;')
        self.mPos = None
        self.iconSize = 20 # Размер значка по умолчанию

        # Установите цвет фона по умолчанию, иначе он будет прозрачным из-за влияния родительского окна
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QColor(60, 60, 60))
        self.setPalette(palette)

        # макет
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(4, 0, 0, 0)

        # значок окна
        self.iconLabel = QLabel(self)
        layout.addWidget(self.iconLabel)

        # название окна
        self.titleLabel = QLabel(self)
        self.titleLabel.setMargin(2)
        self.titleLabel.setStyleSheet('color: #cccccc;')
        layout.addWidget(self.titleLabel)

        # Использовать шрифты Webdings для отображения значков
        font = self.font() or QFont()
        font.setFamily('Webdings')
        font.setPixelSize(14)

        # Свернуть кнопку
        self.buttonMinimum = QPushButton(
            '0', self, clicked=self.windowMinimumed.emit, font=font, objectName='buttonMinimum')
        self.buttonMinimum.setFocusPolicy(Qt.NoFocus)
        self.buttonMinimum.setStyleSheet(
            "#buttonMinimum{\n"
            "   border: none;\n"
            "   background: #3c3c3c;\n"
            "   color: #ccc;\n"
            "}\n"
            "#buttonMinimum:hover{\n"
            "   background: #777;\n"
            "}\n"
        )
        layout.addWidget(self.buttonMinimum)

        # Кнопка закрытия
        self.buttonClose = QPushButton(
            'r', self, clicked=self.windowClosed.emit, font=font, objectName='buttonClose')
        self.buttonClose.setFocusPolicy(Qt.NoFocus)
        self.buttonClose.setStyleSheet(
            "#buttonClose{\n"
            "   border: none;\n"
            "   background: #3c3c3c;\n"
            "   color: #ccc;\n"
            "}\n"
            "#buttonClose:hover{\n"
            "   background: rgb(232, 17, 35);\n"
            "}\n"
        )
        layout.addWidget(self.buttonClose)

        # начальная высота
        self.setHeight()

    def setHeight(self, height=30):
        """ Установка высоты строки заголовка """
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # Задайте размер правой кнопки  ?
        self.buttonMinimum.setMinimumSize(height*1.5, height)
        self.buttonMinimum.setMaximumSize(height*1.5, height)
        self.buttonClose.setMinimumSize(height*1.5, height)
        self.buttonClose.setMaximumSize(height*1.5, height)

    def setTitle(self, title):
        """ Установить заголовок """
        self.titleLabel.setText(title)

    def setIcon(self, icon):
        """ настройки значокa """
        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size):
        """ Установить размер значка """
        self.iconSize = size

    def enterEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super(TitleBar, self).enterEvent(event)

    def mousePressEvent(self, event):
        """ Событие клика мыши """
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        ''' Событие отказов мыши '''
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()
