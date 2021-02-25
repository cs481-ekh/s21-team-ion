"""test docstring please ignore"""
import csv
import tkinter
import storedData
import plotGUI


def read_csv(file):
    """test function docstring please ignore"""
    raw_data = csv.reader(file)
    voltage_list = []
    current_list = []
    for row in raw_data:
        voltage_list.append(float(row[0]))
        current_list.append(float(row[1]) / 1000.0)
    return [voltage_list, current_list]


def do_nothing():
    x = 0


if __name__ == "__main__":
    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")
    menu_bar = tkinter.Menu(root)
    file_menu = tkinter.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Import", command=do_nothing)
    menu_bar.add_cascade(label="File", menu=file_menu)

    data_file = open('rawData/Book2-1.csv', 'r', newline='', encoding='utf-8-sig')
    v_raw, c_raw = read_csv(data_file)

    dataStore = storedData.StoredData(v_raw, c_raw)
    # dataStore.set_regression_bounds()

    gui = plotGUI.PlotGUI(dataStore)
    gui.plot_data(root)

    root.config(menu=menu_bar)
    tkinter.mainloop()

    data_file.close()
