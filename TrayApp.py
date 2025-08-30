import sys
import os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

ICON_PATH = "trayicon.ico"

class TrayApp:
    def __init__(self, app: QApplication):
        self.app = app
        self.app.setQuitOnLastWindowClosed(False)

        pathIcon = os.path.abspath(ICON_PATH)

        self.trayIcon = QSystemTrayIcon(QIcon(pathIcon), self.app)
        self.trayIcon.setToolTip("Моё приложение в трее")

        self.trayMenu = QMenu()
        self.CreateMenu()

    def CreateMenu(self):
        actionShow = QAction("Показать", self)
        actionExit = QAction("Выход", self)

        actionShow.triggered.connect(self.ShowWindow())
        actionExit.triggered.connect(self.ExitApp())

        self.trayMenu.addAction(actionShow)
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(actionExit)

    def ShowWindow(self):
        # Здесь код для показа основного окна, если оно есть
        print("Показываем окно")

    def ExitApp(self):
        # Здесь код для корректного завершения программы
        self.app.quit()

    def Run(self):
        sys.exit(self.app.exec_())