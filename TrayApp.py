import pystray, PIL.Image

class TrayIcon:
    def __init__(self, onQuitCallback):
        self.onQuitCallback = onQuitCallback
        self.image = PIL.Image.open("trayicon.ico")
        self.trayIcon = pystray.Icon(
            "ChangeVolumeArduino", self.image, "Arduino громкость", menu=pystray.Menu(
                pystray.MenuItem("Настройки", self.Exit),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Выход", self.Exit),
            ))

    def Run(self):
        self.trayIcon.run()

    def Exit(self):
        self.onQuitCallback()
        self.trayIcon.stop()