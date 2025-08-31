import time
import threading

import serial
import serial.tools.list_ports
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

class ArduinoWorker:
    def __init__(self, port="COM14", baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.arduino = None
        self.running = threading.Event()
        self.thread = None

        # Получение громкости звука из системы
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = interface.QueryInterface(IAudioEndpointVolume)
        ############

    def GetPort(self) -> str:
        return self.port
    def GetBaudrate(self) -> int:
        return self.baudrate

    @staticmethod
    def GetPorts() -> list[str]:
        return [p.device for p in serial.tools.list_ports.comports()]

    #Установка громкости
    def SetVolume(self, percent: int):
        self.volume.SetMasterVolumeLevelScalar(percent/100, None)

    #Получение громкости
    def GetVolume(self) -> int:
        level = self.volume.GetMasterVolumeLevelScalar()
        return int(round(level * 100))

    #Выключение звука
    def ToggleMute(self):
        self.volume.SetMute(not self.volume.GetMute(), None)

    #Получение mute звука
    #return bool
    def GetMute(self) -> bool:
        return self.volume.GetMute()

    #Поиск ардуино
    def ConnectArduino(self):
        try:
            return serial.Serial(self.port, self.baudrate, timeout=1)
        except serial.SerialException:
            return None

    #Отключение ардуино
    def ArduinoClose(self):
        if self.arduino:
            try:
                self.arduino.close()
            except:
                pass
            self.arduino = None

    def WorkerLoop(self):
        try:
            while self.running.is_set():
                if self.arduino is None or not self.arduino.is_open:
                    print(f"\nОжидание Arduino!... Порт:{self.port} Baud: {self.baudrate}")
                    while self.running.is_set() and self.arduino is None:
                        self.arduino = self.ConnectArduino()
                        time.sleep(2)

                    if self.arduino: print(f"Arduino подключено! Порт:{self.port} Baud: {self.baudrate}")

                try:
                    if self.arduino and self.arduino.in_waiting:
                        cmd = self.arduino.readline().decode().strip()
                        vol = self.GetVolume()
                        if cmd == 'UP':
                            vol = min(100, vol + 2)
                            self.SetVolume(vol)
                        elif cmd == "DOWN":
                            vol = max(0, vol - 2)
                            self.SetVolume(vol)
                        elif cmd == "MUTE":
                            self.ToggleMute()

                    if self.arduino:
                        if self.GetMute():
                            self.arduino.write(b"MUTE\n")
                        else:
                            self.arduino.write(f"{self.GetVolume()}\n".encode())
                    time.sleep(0.1)

                except (serial.SerialException, OSError):
                    print("Потеряно соединение с Arduino.")
                    self.ArduinoClose()
        finally:
            self.ArduinoClose()
            print("ArduinoWorker остановлен.")

    def Reconnect(self, port: str, baudrate: int):
        self.Stop()
        self.port = port
        self.baudrate = baudrate
        self.Start()

    # Управление потоком
    def Start(self):
        if self.thread and self.thread.is_alive():
            return  # уже запущен
        print("Запуск ArduinoWorker...")
        self.running.set()
        self.thread = threading.Thread(target=self.WorkerLoop, daemon=True)
        self.thread.start()

    def Stop(self):
        print("Остановка ArduinoWorker...")
        self.running.clear()
        if self.thread:
            self.thread.join()
    #-------------------------