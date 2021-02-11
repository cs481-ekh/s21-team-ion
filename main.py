import csv
import storedData
from plotGUI import PlotGUI
if os.environ.get('DISPLAY','') == '':
   print('no display found. Using non-interactive Agg backend')
   mpl.use('Agg')


def read_csv(file):
    raw_data = csv.reader(file)
    voltage_list = []
    current_list = []
    for row in raw_data:
        voltage_list.append(float(row[0]))
        current_list.append(float(row[1]) / 1000.0)
    return [voltage_list, current_list]


if __name__ == "__main__":
    data_file = open('rawData/Book2-1.csv', 'r', newline='', encoding='utf-8-sig')
    v_raw, c_raw = read_csv(data_file)
    dataStore = storedData.StoredData(v_raw, c_raw)
    # dataStore.set_regression_bounds()

    PlotGUI.plot_data(dataStore)
    data_file.close()
