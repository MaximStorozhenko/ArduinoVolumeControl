from ArduinoWorker import ArduinoWorker
from TrayApp import TrayIcon
import ConfigManager
from SingleInstance import SingleInstance
import sys

def main():
    SingleInstance("ArduinoVolumeControl")

    config = ConfigManager.LoadConfig()
    port = config.get("port", "COM55")
    baudrate = config.get("baudrate", 9600)

    worker = ArduinoWorker(port, baudrate)
    worker.Start()

    def ExitProgram():
        print("Выход из программы...")
        worker.Stop()

    tray = TrayIcon(worker, ExitProgram)
    tray.Run()

    print("Программа завершена.")

if __name__ == "__main__":
    main()
    sys.exit(0)