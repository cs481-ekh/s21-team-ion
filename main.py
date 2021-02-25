"""test docstring please ignore"""
import csv
import tkinter
import storedData
import plotGUI
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter import filedialog


class GUIHandler:
    def __init__(self):
        root = tkinter.Tk()
        root.wm_title("Embedding in Tk")
        menu_bar = tkinter.Menu(root)
        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import", command=self.browseFiles)
        menu_bar.add_cascade(label="File", menu=file_menu)

        data_file = open('rawData/Book2-1.csv', 'r', newline='', encoding='utf-8-sig')
        v_raw, c_raw = self.read_csv(data_file)

        data_store = storedData.StoredData(v_raw, c_raw)
        # dataStore.set_regression_bounds()

        # create figure inside tkinter window and create axes that all plots can use
        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.

        # pack_toolbar=False will make it easier to use a layout manager later on.
        toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
        toolbar.update()

        gui = plotGUI.PlotGUI(data_store)
        gui.plot_data(fig, canvas)

        button = tkinter.Button(master=root, text="Quit", command=root.quit)

        # Packing order is important. Widgets are processed sequentially and if there
        # is no space left, because the window is too small, they are not displayed.
        # The canvas is rather flexible in its size, so we pack it last which makes
        # sure the UI controls are displayed as long as possible.
        button.pack(side=tkinter.BOTTOM)
        toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        root.config(menu=menu_bar)
        tkinter.mainloop()

        data_file.close()

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

    def read_csv(self, file):
        """test function docstring please ignore"""
        raw_data = csv.reader(file)
        voltage_list = []
        current_list = []
        for row in raw_data:
            voltage_list.append(float(row[0]))
            current_list.append(float(row[1]) / 1000.0)
        return [voltage_list, current_list]

    # Function for opening the file explorer window
    def browseFiles(self):
        filedialog.askopenfilename(initialdir="~", title="Select a File",
                                          filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        # label_file_explorer.configure(text="File opened: "+filename)


def do_nothing():
    x = 0


if __name__ == "__main__":
    gui = GUIHandler()
