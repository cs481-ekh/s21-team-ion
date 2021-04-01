import numpy as np
from scipy import stats


class StoredData:
    voltages = None  # 1d np array
    currents = None  # 1d np array
    regression_min = None  # float
    regression_max = None  # float
    vertical_regression_line_points = None  # 1d np array
    regr_calc_start = None  # int, array index
<<<<<<< HEAD
    regr_calc_end = None  # int, array indexgit 
=======
    regr_calc_end = None  # int, array index
    regression_plot_data = None
>>>>>>> 93072bcb0d3194ef15fb388105629f70d8cd8504

    def __init__(self, v_raw, c_raw):
        if len(v_raw) == 0:
            self.voltages = np.array([0, 1])
            self.currents = np.array([0, 1])
            self.regression_min = 0
            self.regression_max = 0
            self.compute_regression_boundary_lines()
        else:
            self.voltages = np.array(v_raw)
            self.currents = np.array(c_raw)
            self.regression_min = np.min(self.voltages)
            self.regression_max = np.max(self.voltages)
            self.compute_regression_boundary_lines()

    def compute_regression_boundary_lines(self):
        current_min = np.min(self.currents)
        current_max = np.max(self.currents)
        delta_list = []
        for i in range(len(self.currents) - 1):
            delta = np.abs(self.currents[i + 1] - self.currents[i])
            delta_list.append(delta)
        average_current_delta = np.average(delta_list)
        if current_min == current_max == 0.0:
            self.vertical_regression_line_points = np.zeros(2)
        else:
            self.vertical_regression_line_points = np.arange(start=current_min,
                                                             stop=current_max,
                                                             step=average_current_delta)

            self.__compute_linear_regression()

    def __compute_linear_regression(self):
        tolerance = 0.02  # empirically derived from data in csv.  Each step in x is approx. 0.026

        # find the index of the first instance of the minimum and maximum regression boundary lines on the x-axis
        try:
            self.regr_calc_start = next(i for i, _ in enumerate(self.voltages) if np.isclose(_, self.regression_min, tolerance))
            self.regr_calc_end = next(i for i, _ in enumerate(self.voltages) if np.isclose(_, self.regression_max, tolerance))
        except StopIteration:
            pass
        except IndexError:
            self.regr_calc_start = None

        lr_x = None
        lr_y = None
        if self.regr_calc_start is not None:
            lr_x = self.voltages[self.regr_calc_start:self.regr_calc_end, ]
            lr_y = self.currents[self.regr_calc_start:self.regr_calc_end, ]
            if not lr_x.size == 0:
                self.regression_plot_data = stats.linregress(lr_x, lr_y)
            else:
                self.regression_plot_data = stats.linregress(self.voltages, self.currents)

    def __find_index(self, array, value, tolerance):
        retVal = None
        i = 0
        for item in array:
            if item - tolerance <= value <= item + tolerance:
                retVal = i
                break
            i = i + 1

        return retVal

    def get_regression_data(self):
        self.__compute_linear_regression()
        return self.regression_plot_data
