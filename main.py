import math
import time
import serial
import serial.tools.list_ports
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

import sys
from PyQt5.QtWidgets import QApplication
from TrayApp import TrayApp

BAUDRATE = 9600
arduino = None

# Получение громкости звука
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
############

#Установка громкости
def SetVolume(percent):
    volume.SetMasterVolumeLevelScalar(percent/100, None)

#Получение громкости
def GetVolume():
    level = volume.GetMasterVolumeLevelScalar()
    return int(round(level * 100))

#Выключение звука
def ToggleMute():
    volume.SetMute(not volume.GetMute(), None)

#Получение mute звука
#return bool
def GetMute():
    return volume.GetMute()

#Поиск ардуино
def ConnectArduino(port, baudrate):
    try:
        return serial.Serial(port, baudrate, timeout=1)
    except serial.SerialException:
        return None

#Отключение ардуино
def ArduinoClose():
    if arduino:
        try:
            arduino.close()
        except:
            pass

try:
    while True:
        if arduino is None or not arduino.is_open:
            print("\nОжидание Arduino...")
            while arduino is None:
                arduino = ConnectArduino("COM14", BAUDRATE)
                time.sleep(2)
            print("Arduino подключено!")

        try:
            if arduino.in_waiting:
                cmd = arduino.readline().decode().strip()
                vol = GetVolume()
                if cmd == 'UP':
                    vol = min(100, vol + 2)
                    SetVolume(vol)
                elif cmd == "DOWN":
                    vol = max(0, vol - 2)
                    SetVolume(vol)
                elif cmd == "MUTE":
                    ToggleMute()

            if GetMute():
                arduino.write(b"MUTE\n")
            else:
                arduino.write(f"{GetVolume()}\n".encode())
            time.sleep(0.1)

        except (serial.SerialException, OSError):
            print("Потеряно соединение с Arduino.")
            ArduinoClose()
            arduino = None  # снова ждать подключения

except KeyboardInterrupt:
    ArduinoClose()
    print("\nThe program was stopped by the user.")