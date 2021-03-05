"""test docstring please ignore"""
import csv
import tkinter
from tkinter import messagebox
from storedData import StoredData
from plotGUI import PlotGUI
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter import filedialog
from utils import Callbacks
from pathlib import Path


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
        self.voltage_list = []
        self.current_list = []

        self.root = tkinter.Tk()
        self.root.wm_title("Embedding in Tk")
        menu_bar = tkinter.Menu(self.root)

        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import", command=self.browse_files)
        file_menu.add_command(label="Export", command=self.save)  # need to add implementation first
        file_menu.add_command(label="Exit", command=self.root.quit)

        # data_file = open('rawData/Book2-1.csv', 'r', newline='', encoding='utf-8-sig')
        # v_raw, c_raw = self.read_csv(data_file)

        # data_store = storedData.StoredData(v_raw, c_raw)
        menu_bar.add_cascade(label="File", menu=file_menu)

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

        self.root.after(0, self.update_graph, fig, canvas)

        self.root.config(menu=menu_bar)

        # generate empty plot, but keep bool to save on CPU usage
        self.csv_was_called = True
        self.update_graph(fig, canvas)

        self.plot.plot_data(fig, canvas)
        self.root.mainloop()

        # data_file.close()

    # function to save currently plotted graph to a new csv file
    def save(self):
        # gives user a choice between saving as .csv file or .txt file
        file = filedialog.asksaveasfile(defaultextension='.csv',
                                        filetypes=[("CSV file (.csv)", ".csv"), ("Text file (.txt)", ".txt")])
        file.close()

        # pass
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
        """
        Reads a .csv file that the user selected in browse_files().
        Checks if browse_files() was called (since this function is polled)
        Then, checks if the file exists.
        If the file exists, it reads in the data and stores it in memory in an instance of a StoredData class

        TODO: make sure the the file is a valid csv file
        """
        file_str = self.cb.get_file()
        file_path = Path(file_str)
        if file_path.is_file():
            file = open(file_str, 'r', newline='', encoding='utf-8-sig')
            raw_data = csv.reader(file)
            self.__store_data_from_csv(raw_data)
            file.close()

        self.browse_was_called = False
        self.csv_was_called = True

    # Function for opening the file explorer window
    def browse_files(self):
        self.cb.browse_files()
        self.read_csv()
        self.browse_was_called = True

    def update_graph(self, fig, canvas):
        self.root.after(100, self.update_graph, fig, canvas)
        if not self.csv_was_called:
            return

        self.data_store = StoredData(self.voltage_list, self.current_list)
        self.plot = PlotGUI(self.data_store)
        self.plot.plot_data(fig, canvas)
        self.csv_was_called = False

    def __store_data_from_csv(self, data):
        self.voltage_list = []
        self.current_list = []
        current_row = 1
        valid_file = True
        msg = None
        label = None
        for row in data:
            if len(row) < 2:
                valid_file = False
                label = "Data missing in CSV"
                msg = "Missing data on row {}".format(current_row)
                break

            try:
                float(row[0])
                float(row[1])
            except ValueError:
                valid_file = False
                label = "Invalid data"
                msg = "Data in row {} does not appear to be a floating point number".format(current_row)
                break

            self.voltage_list.append(float(row[0]))
            self.current_list.append(float(row[1]) / 1000.0)
            current_row = current_row + 1

        if not valid_file:
            self.voltage_list = []
            self.current_list = []

            messagebox.showerror(label, msg)
            self.root.update()


if __name__ == "__main__":
    gui = GUIHandler()
