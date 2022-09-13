
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

from controll import Controller

import sys
import threading


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://localhost:8000/"))

        self.setCentralWidget(self.browser)

        self.show()

Controller.init("192.168.0.108", 55573)
controller_thread = threading.Thread(target=Controller.controller_thread)
controller_thread.start()

app = QApplication(sys.argv)
window = MainWindow()
window.resize(1200, 700)

app.exec_()