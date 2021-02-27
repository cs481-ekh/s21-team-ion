"""test docstring please ignore"""
import csv
import tkinter
from storedData import StoredData
from plotGUI import PlotGUI
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter import filedialog
from utils import Callbacks


class GUIHandler:
    root = None  # instance of Tk class
    cb = None  # instance of Callback class
    browse_was_called = None  # bool
    csv_was_called = None  # bool
    voltage_list = None  # list
    current_list = None  # list
    data_store = None  # instance of StoredData class
    plot = None  # instance of PlotGUI class

    def __init__(self):
        self.cb = Callbacks()
        self.browse_was_called = False
        self.csv_was_called = False

        self.root = tkinter.Tk()
        self.root.wm_title("Embedding in Tk")
        menu_bar = tkinter.Menu(self.root)

        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import", command=self.browseFiles)
        file_menu.add_command(label="Exit", command=self.root.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)

        # data_file = open('rawData/Book2-1.csv', 'r', newline='', encoding='utf-8-sig')
        # v_raw, c_raw = self.read_csv(data_file)

        # data_store = storedData.StoredData(v_raw, c_raw)
        # dataStore.set_regression_bounds()

        # create figure inside tkinter window and create axes that all plots can use
        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.

        # pack_toolbar=False will make it easier to use a layout manager later on.
        toolbar = NavigationToolbar2Tk(canvas, self.root, pack_toolbar=False)
        toolbar.update()

        # gui = plotGUI.PlotGUI(data_store)
        # gui.plot_data(fig, canvas)

        # Packing order is important. Widgets are processed sequentially and if there
        # is no space left, because the window is too small, they are not displayed.
        # The canvas is rather flexible in its size, so we pack it last which makes
        # sure the UI controls are displayed as long as possible.
        toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.root.after(0, self.read_csv)
        self.root.after(0, self.update_graph, fig, canvas)

        self.root.config(menu=menu_bar)
        self.root.mainloop()

        # data_file.close()

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

    def read_csv(self):
        """test function docstring please ignore"""
        self.root.after(100, self.read_csv)
        if not self.browse_was_called:
            return

        self.csv_was_called = True

        file_str = self.cb.get_file()
        file = open(file_str, 'r', newline='', encoding='utf-8-sig')
        raw_data = csv.reader(file)
        self.voltage_list = []
        self.current_list = []
        for row in raw_data:
            self.voltage_list.append(float(row[0]))
            self.current_list.append(float(row[1]) / 1000.0)

        self.browse_was_called = False
        file.close()

    # Function for opening the file explorer window
    def browseFiles(self):
        self.cb.browse_files()
        self.browse_was_called = True

    def update_graph(self, fig, canvas):
        self.root.after(100, self.update_graph, fig, canvas)
        if not self.csv_was_called:
            return

        self.data_store = StoredData(self.voltage_list, self.current_list)
        self.plot = PlotGUI(self.data_store)
        self.plot.plot_data(fig, canvas)
        self.csv_was_called = False


def do_nothing():
    x = 0


if __name__ == "__main__":
    gui = GUIHandler()
