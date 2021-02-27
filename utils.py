import tkinter as tk
from tkinter import filedialog


class Callbacks:
    __file_str = None

    def __init__(self):
        pass

    def browse_files(self):
        self.__file_str = filedialog.askopenfilename(initialdir="~", title="Select a File",
                                          filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))

    def get_file(self):
        return self.__file_str
