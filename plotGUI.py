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
    stored_data = None  # instance of StoredData class (storedData.py)

    def __init__(self, data):
        self.stored_data = data

    # Function for opening the file explorer window
    def browseFiles(self):
        return filedialog.askopenfilename(initialdir="~", title="Select a File",
                                          filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        # label_file_explorer.configure(text="File opened: "+filename)

    # function to save currently plotted graph to a new csv file
    def save(self):
        pass
        # plt.savefig('new_graph.png') #placeholder: user should be able to name their own file (input)
        # pop = Tk()

        # fig, ax = plt.subplots()
        # ax.plot(np.arange(1,10,5), np.arange(1,10,5))

        # plot_canvas = FigureCanvasTkAgg(fig, master=pop)
        # plot_canvas.draw()

        # toolbar = NavigationToolbar2Tk(plot_canvas, pop)
        # toolbar.update()
        # plot_canvas.get_tk_widget().pack(side=TOP, fill=Y)

    # @ staticmethod
    def plot_data(self):
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

        # create figure inside tkinter window and create axes that all plots can use
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # get the raw data in a form that is easy to plot
        raw_data_plot = self.__raw_data_plot()

        # get the upper and lower regression boundary lines (vertical lines on either side of the graph)
        regression_bounds = self.__regression_bounds_plots()

        # get the simple linear regression for plotting
        regression_plot = self.__regression_plot()

        # plot raw data, regression boundaries, and regression
        ax.plot(raw_data_plot["x"], raw_data_plot["y"])
        ax.plot(regression_bounds["lower"], regression_bounds["y"])
        ax.plot(regression_bounds["upper"], regression_bounds["y"])
        ax.plot(regression_plot["x"], regression_plot["y"], label='I_max')

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
        save_button = tkinter.Button(master=root, text="Save", command=lambda: self.save())

        # Packing order is important. Widgets are processed sequentially and if there
        # is no space left, because the window is too small, they are not displayed.
        # The canvas is rather flexible in its size, so we pack it last which makes
        # sure the UI controls are displayed as long as possible.
        button.pack(side=tkinter.BOTTOM)
        toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        button2.pack(side=tkinter.TOP)
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        tkinter.mainloop()

    def __raw_data_plot(self):
        """Helper method that returns the raw x/y data stored as a dictionary.  Makes plotting the data in plot_data()
        a single line of easy-to-read code.

        Returns
        -------
        dict
            ["x"] the x-values of the raw data on a cartesian plane
            ["y"] the y-values of the raw data on a cartesian plane
        """
        return {"x": self.stored_data.voltages, "y": self.stored_data.currents}

    def __regression_bounds_plots(self):
        """Helper method that returns the upper and lower boundaries of the linear regression, stored as a dictionary.
        Makes plotting these lines in plot_data() a single line of easy-to-read code.

        Returns
        -------
        dict
            ["lower"] the x-values of the lower boundary of the linear regression on a cartesian plane
            ["upper"] the x-values of the upper boundary of the linear regression on a cartesian plane
            ["y"] the y-values of the boundaries of the linear regression on a cartesian plane (same values for both
                    lower and upper boundaries)
        """
        return {"lower": np.full((len(self.stored_data.vertical_regression_line_points)),
                                 self.stored_data.regression_min),
                "upper": np.full((len(self.stored_data.vertical_regression_line_points)),
                                 self.stored_data.regression_max),
                "y": self.stored_data.vertical_regression_line_points}

    def __regression_plot(self):
        """Helper method that returns the linear regression in a form that can be plotted, stored as a dictionary.
        Makes plotting this lines in plot_data() a single line of easy-to-read code.

        Returns
        -------
        dict
            ["x"] the x-values of the linear regression on a cartesian plane
            ["y"] the y-values of the linear regression on a cartesian plane
        """
        linregression = self.stored_data.compute_linear_regression()
        return {"x": self.stored_data.voltages, "y": linregression.intercept + linregression.slope *
                                                     self.stored_data.voltages}
