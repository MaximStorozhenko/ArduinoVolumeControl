import sys
import ctypes
from tkinter import messagebox, Tk

class SingleInstance:
    def __init__(self, name: str):
        self.mutex = ctypes.windll.kernel32.CreateMutexW(None, False, name)

        error = ctypes.windll.kernel32.GetLastError()
        if error == 183:
            root = Tk()
            root.withdraw()
            messagebox.showerror("Ошибка", "Программа уже запущена!")
            sys.exit(0)