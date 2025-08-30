from ArduinoWorker import ArduinoWorker

from TrayApp import TrayIcon

def main():
    worker = ArduinoWorker("COM14")
    worker.start()

    def ExitProgram():
        print("Выход из программы...")
        worker.stop()

    tray = TrayIcon(ExitProgram)
    tray.Run()

    print("Программа завершена.")

if __name__ == "__main__":
    main()