import numpy as np
from scipy import stats


class StoredData:
    voltages = None  # 1d np array
    currents = None  # 1d np array
    regression_min = None  # float
    regression_max = None  # float
    vertical_regression_line_points = None  # 1d np array

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

            self.compute_linear_regression()

    def compute_linear_regression(self):
        return stats.linregress(self.voltages, self.currents)
