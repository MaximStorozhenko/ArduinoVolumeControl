import pystray, PIL.Image
import tkinter as tk
from tkinter import ttk
import threading
from ArduinoWorker import ArduinoWorker

class TrayIcon:
    def __init__(self, worker, onQuitCallback):
        self.worker = worker
        self.onQuitCallback = onQuitCallback
        self.image = PIL.Image.open("trayicon.ico")
        self.trayIcon = pystray.Icon(
            "ChangeVolumeArduino", self.image, "Arduino громкость", menu=pystray.Menu(
                pystray.MenuItem("Настройки", self.OpenSettingsWindow),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Выход", self.Exit),
            ))

    def Run(self):
        self.trayIcon.run()

    def Exit(self):
        self.onQuitCallback()
        self.trayIcon.stop()

    def OpenSettingsWindow(self):
        def Run():
            win = tk.Tk()
            win.title("Настройки")

            windowWidth = 300
            windowHeight = 150
            win.geometry(f"{windowWidth}x{windowHeight}")

            screenWidth = win.winfo_screenwidth()
            screenHeight = win.winfo_screenheight()

            centerX = int(screenWidth / 2 - windowWidth / 2)
            centerY = int(screenHeight / 2 - windowHeight / 2)

            win.geometry(f"+{centerX}+{centerY}")

            # COM порты
            tk.Label(win, text="COM порт:").pack(pady=5)
            ports = ArduinoWorker.GetPorts()
            selectedPort = self.worker.GetSelectedPort()
            portVar = tk.StringVar(value=selectedPort if ports else "")
            portBox = ttk.Combobox(win, textvariable=portVar, values=ports)
            portBox.pack()

            # Baudrate
            tk.Label(win, text="Скорость:").pack(pady=5)
            baudVar = tk.StringVar(value="9600")
            baudBox = ttk.Combobox(win, textvariable=baudVar,
                                    values=["9600", "19200", "38400", "57600", "115200"])
            baudBox.pack()

            def Apply():
                port = portVar.get()
                baud = int(baudVar.get())
                self.worker.reconnect(port, baud)
                win.destroy()

            ttk.Button(win, text="Применить", command=Apply).pack(pady=10)
            win.mainloop()

        threading.Thread(target=Run, daemon=True).start()