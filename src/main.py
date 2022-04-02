#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow
import sys

# Created on 16.08.2021
# author: Gennady Sosnov
# site: -
# email: gena.06.08@yandex.ru
# file: main
# description:
__Author__ = """By: Gennady Sosnov
Email: gena.06.08@yandex.ru"""
__Copyright__ = 'Copyright (c) 2021 Gennady Sosnov'
__Version__ = 1.1

config = {
    'WIDTH': 960,
    'HEIGHT': 540,
    'FPS': 60,
    'PLATFORM_HEIGHT': 108,
    'PLATFORM_WIDTH': 5,
    'TEXT_SIZE': 64,
    'WIN_SCORE': 10
}

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow(config)
    w.show()

    sys.exit(app.exec())