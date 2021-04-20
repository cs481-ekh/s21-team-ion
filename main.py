"""test docstring please ignore"""
import csv
import tkinter
from tkinter import messagebox
from storedData import StoredData
from plotGUI import PlotGUI
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib as mpl
from matplotlib.figure import Figure
from tkinter import filedialog
from utils import Callbacks
from pathlib import Path
from plot_op import PlotOp


class GUIHandler:
    root = None  # instance of Tk class
    cb = None  # instance of Callback class
    browse_was_called = None  # bool
    csv_was_called = None  # bool
    voltage_list = None  # list
    current_list = None  # list
    data_store = None  # instance of StoredData class
    plot = None  # instance of PlotGUI class
    open_prob_plot = None  # another instance of PlotGUI class
    open_prob_figure = None
    open_prob_canvas = None

    # testing these as global and sending them to plotgui
    # leftEntry = None
    # rightEntry = None

    def __init__(self):
        self.cb = Callbacks()
        self.browse_was_called = False
        self.csv_was_called = False
        self.voltage_list = []
        self.current_list = []

        self.root = tkinter.Tk()
        self.root.wm_title("Open Probability of Ion Channels")
        menu_bar = tkinter.Menu(self.root)

        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import", command=self.browse_files)
        file_menu.add_command(label="Export", command=self.save)  # need to add implementation first
        file_menu.add_command(label="Exit", command=self.root.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)

        # create figure inside tkinter window and create axes that all plots can use
        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.

        # create our own toolbar, then remove all the buttons from it / gui objects from it
        toolbar = NavigationToolbar2Tk(canvas, self.root, pack_toolbar=False)
        for item in toolbar.children:
            if type(toolbar.children[item]) in (tkinter.Button, tkinter.Frame, tkinter.Checkbutton):
                toolbar.children[item].pack_forget()
        toolbar.update()

        self.open_prob_figure = Figure(figsize=(5, 4), dpi=100)
        self.open_prob_canvas = FigureCanvasTkAgg(self.open_prob_figure, master=self.root)

        # open_prob_toolbar = NavigationToolbar2Tk(self.open_prob_canvas, self.root, pack_toolbar=False)
        # open_prob_toolbar.update()

        # bottom frame
        frame = tkinter.Frame(self.root)
        self.leftEntry = tkinter.Entry(frame, width=10, borderwidth=2)
        self.leftEntry.insert(0, 'min')
        self.leftEntry.pack(side=tkinter.LEFT)
        self.rightEntry = tkinter.Entry(frame, text='right', width=10, borderwidth=2)
        self.rightEntry.insert(0, 'max')
        self.rightEntry.pack(side=tkinter.LEFT)
        range_button = tkinter.Button(frame, text="Update Range",
                                      command=self.update_button_press)
        range_button.pack(side=tkinter.RIGHT)
        frame.pack(side=tkinter.BOTTOM)

        # Packing order is important. Widgets are processed sequentially and if there
        # is no space left, because the window is too small, they are not displayed.
        # The canvas is rather flexible in its size, so we pack it last which makes
        # sure the UI controls are displayed as long as possible.
        toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        # toolbar2.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.open_prob_canvas.get_tk_widget().pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=1)

        self.root.after(100, self.update_graph, fig, canvas)

        self.root.config(menu=menu_bar)

        # generate empty plot, but keep bool to save on CPU usage
        self.csv_was_called = True

        # must call update_graph() before update_op_graph()
        self.update_graph(fig, canvas)
        self.plot.plot_data(fig, canvas, self.root)

        self.update_op_graph(self.open_prob_figure, self.open_prob_canvas)
        self.open_prob_plot.plot_data(self.open_prob_figure, self.open_prob_canvas, self.root)

        self.root.mainloop()

        # data_file.close()

    # function to save currently plotted graph to a new csv file
    def save(self):
        # gives user a choice between saving as .csv file or .txt file
        
        file_name = filedialog.asksaveasfile(defaultextension='.csv',
                                        filetypes=[("CSV file (.csv)", ".csv"), ("Text file (.txt)", ".txt")])
        if file_name is not None:
            file = open(file_name.name, 'w')
           
            regr_data = self.data_store.get_regression_data()
            file_data = [regr_data['x'], regr_data['y']]
            # file_writer = csv.writer(file, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            file_writer = csv.writer(file)
            file_writer.writerow(file_data)
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
        self.plot = PlotGUI(self.data_store, self.leftEntry, self.rightEntry)
        self.plot.plot_data(fig, canvas, self.root)

    def update_op_graph(self, fig, canvas):
        self.root.after(100, self.update_op_graph, fig, canvas)
        if not self.csv_was_called:
            return

        self.open_prob_plot = PlotOp(self.data_store)
        self.open_prob_plot.plot_data(fig, canvas, self.root)
        self.csv_was_called = False

    def update_button_press(self):
        min_val = self.leftEntry.get()
        max_val = self.rightEntry.get()

        try:
            min_val = float(min_val)
            self.plot.update_from_textbox("min", min_val)
        except ValueError:
            print("min input not a float")

        try:
            max_val = float(max_val)
            self.plot.update_from_textbox("max", max_val)
        except ValueError:
            print("max input not a float")

        self.update_op_graph(self.open_prob_figure, self.open_prob_canvas)
        self.open_prob_plot.plot_data(self.open_prob_figure, self.open_prob_canvas, self.root)

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
                msg = "Data in row {} does not appear to be a floating point number".format(
                    current_row)
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
