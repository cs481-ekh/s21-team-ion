import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib as mpl
from tkinter import filedialog
# from xvfbwrapper import Xvfb


class PlotGUI:
    def __init__(self):
        pass

    # Function for opening the file explorer window
    def browseFiles(self):
        return filedialog.askopenfilename(initialdir="~", title="Select a File",
                                          filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        # label_file_explorer.configure(text="File opened: "+filename)

    # @ staticmethod
    def plot_data(self, stored_data):
        # fig, ax = plt.subplots()
        # ax.plot(stored_data.voltages, stored_data.currents, '-', lw=1, label='raw data')
        # regression_xmin = np.full((len(stored_data.vertical_regression_line_points)), stored_data.regression_min)
        # regression_xmax = np.full((len(stored_data.vertical_regression_line_points)), stored_data.regression_max)
        # ax.plot(regression_xmin, stored_data.vertical_regression_line_points)
        # ax.plot(regression_xmax, stored_data.vertical_regression_line_points)
        #
        # linregression = stored_data.compute_linear_regression()
        # ax.plot(stored_data.voltages, linregression.intercept + linregression.slope*stored_data.voltages, label='I_max')
        # ax.legend(loc='upper right')
        #
        # ax.set(xlabel='voltage (mV)', ylabel='current (nA)',
        #        title='I-V plot')
        # ax.grid()
        #
        # fig.savefig("test.png")
        # plt.show()
        # if os.environ.get('DISPLAY', '') == '':
        # print('no display found. Using non-interactive Agg backend')
        # mpl.use('Agg')
        # vdisplay = Xvfb()
        # vdisplay.start()

        root = tkinter.Tk()
        root.wm_title("Embedding in Tk")

        fig = Figure(figsize=(5, 4), dpi=100)
        x = stored_data.voltages
        y = stored_data.currents
        fig.add_subplot(111).plot(x, )

        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()

        # pack_toolbar=False will make it easier to use a layout manager later on.
        toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
        toolbar.update()

        canvas.mpl_connect(
            "key_press_event", lambda event: print(f"you pressed {event.key}"))
        canvas.mpl_connect("key_press_event", key_press_handler)

        button = tkinter.Button(master=root, text="Quit", command=root.quit)
        button2 = tkinter.Button(master=root, text="Browse", command=lambda: self.browseFiles())

        # Packing order is important. Widgets are processed sequentially and if there
        # is no space left, because the window is too small, they are not displayed.
        # The canvas is rather flexible in its size, so we pack it last which makes
        # sure the UI controls are displayed as long as possible.
        button.pack(side=tkinter.BOTTOM)
        toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        button2.pack(side=tkinter.TOP)
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        tkinter.mainloop()
