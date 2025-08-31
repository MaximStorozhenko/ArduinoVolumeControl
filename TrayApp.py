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
                pystray.MenuItem("О программе", self.OpenAboutWindow),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Выход", self.Exit),
            ))

    def Run(self):
        self.trayIcon.run()

    def Exit(self):
        self.onQuitCallback()
        self.trayIcon.stop()

    #Создание окна по размерам и установка по центру экрана
    def CreateWindow(self, win, winWidth, winHeight):
        win.geometry(f"{winWidth}x{winHeight}")
        screenWidth = win.winfo_screenwidth()
        screenHeight = win.winfo_screenheight()
        centerX = int(screenWidth / 2 - winWidth / 2)
        centerY = int(screenHeight / 2 - winHeight / 2)
        win.geometry(f"+{centerX}+{centerY}")

    def OpenSettingsWindow(self):
        def Run():
            win = tk.Tk()
            win.title("Настройки")
            win.resizable(False, False)  #Запрет на изменение размера

            windowWidth = 300
            windowHeight = 150
            self.CreateWindow(win, windowWidth, windowHeight)

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
                print(f"port: {port}, baud: {baud}")
                self.worker.Reconnect(port, baud)
                win.destroy()

            ttk.Button(win, text="Применить", command=Apply).pack(pady=10)
            win.mainloop()

        threading.Thread(target=Run, daemon=True).start()

    def OpenAboutWindow(self):
        def Run():
            win = tk.Tk()
            win.title("О программе")
            win.resizable(False, False)  #Запрет на изменение размера
            win.overrideredirect(True)  #Убрал заголок окна

            windowWidth = 300
            windowHeight = 200
            self.CreateWindow(win, windowWidth, windowHeight)

            # --- таблица из 2 строк: верх - контент, низ - кнопка ---
            win.rowconfigure(0, weight=1)  # контент растягивается
            win.rowconfigure(1, weight=0)  # кнопка фиксирована
            win.columnconfigure(0, weight=1)

            # Контент
            frame = tk.Frame(win, padx=10, pady=10)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.columnconfigure(0, weight=1)

            def StartMove(event):
                event.widget.startX = event.x
                event.widget.startY = event.y

            def DoMove(event):
                dx = event.x - event.widget.startX
                dy = event.y - event.widget.startY
                x = win.winfo_x() + dx
                y = win.winfo_y() + dy
                win.geometry(f"+{x}+{y}")

            frame.bind("<Button-1>", StartMove)  # запоминаем точку клика
            frame.bind("<B1-Motion>", DoMove)  # двигаем окно при движении

            tk.Label(frame, text="Arduino Volume Control", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="ew", pady=5)
            tk.Label(frame, text="Версия 1.0").grid(row=1, column=0, sticky="ew", pady=2)
            tk.Label(frame, text="Автор: Максим Стороженко").grid(row=2, column=0, sticky="ew", pady=2)

            for child in frame.winfo_children():
                child.bind("<Button-1>", StartMove)
                child.bind("<B1-Motion>", DoMove)

            ttk.Button(win, text="OK", command=win.destroy).grid(row=1, column=0, padx=10, pady=10)
            win.mainloop()

        threading.Thread(target=Run, daemon=True).start()