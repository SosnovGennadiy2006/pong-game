from PyQt5 import QtCore, QtWidgets
from buttonClasses import CustomButton

class Menu(QtWidgets.QFrame):
    def __init__(self, size, margin=10, btn_width = 200, btn_height = 60, parent=None):
        super(Menu, self).__init__(parent)
        self.width = size[0]
        self.height = size[1]
        self.margin = margin
        self.btn_width = btn_width
        self.btn_height = btn_height
        self.setGeometry(0, 0, self.width, self.height)

        self.init_menu()

    def init_menu(self):
        self.setObjectName("menu")
        self.setStyleSheet("background: #000;")
        self.PlayBtn1 = CustomButton("1 Player", self)
        self.PlayBtn1.setGeometry(QtCore.QRect(self.width / 2 - self.btn_width - self.margin / 2, 40, self.btn_width, self.btn_height))
        self.PlayBtn1.setObjectName("PlayBtn1")

        self.PlayBtn2 = CustomButton("2 Players", self)
        self.PlayBtn2.setGeometry(QtCore.QRect(self.width / 2 + self.margin / 2, 40, self.btn_width, self.btn_height))
        self.PlayBtn2.setObjectName("PlayBtn2")

        self.SettingsBtn = CustomButton("Settings", self)
        self.SettingsBtn.setGeometry(QtCore.QRect(self.width / 2 - self.btn_width / 2, 40 + self.btn_height + self.margin, self.btn_width, self.btn_height))
        self.SettingsBtn.setObjectName("SettingsBtn")