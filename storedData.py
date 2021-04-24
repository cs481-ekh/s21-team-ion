import numpy as np
from scipy import stats


class StoredData:
    voltages = None  # 1d np array
    currents = None  # 1d np array
    regression_min = None  # float
    regression_max = None  # float
    vertical_regression_line_points = None  # 1d np array
    regr_calc_start = None  # int, array index

    # regr_calc_end = None  # int, array indexgit 
    regr_calc_end = None  # int, arragit y index
    regression_plot_data = None
    stats_regression = None
    open_prob_vals = None  # dict containing pos voltages for x and OP for y

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
        regression = None
        if self.regr_calc_start is not None:
            lr_x = self.voltages[self.regr_calc_start:self.regr_calc_end, ]
            lr_y = self.currents[self.regr_calc_start:self.regr_calc_end, ]
            if not lr_x.size == 0:
                regression = stats.linregress(lr_x, lr_y)
            else:
                regression = stats.linregress(self.voltages, self.currents)

            self.regression_plot_data = {"x": self.voltages, "y": regression.intercept + regression.slope *
                                                                  self.voltages}
            self.stats_regression = regression

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

    def __calc_open_probability(self):
        # get positive voltage and current values
        pos_vals = self.__get_pos_vals()
        pos_volts = pos_vals["v"]
        pos_currents = pos_vals["i"]

        # ensure pos_volts and pos_currents are the same length
        if len(pos_currents) > len(pos_volts):
            pos_currents = pos_currents[:len(pos_volts)]
        elif len(pos_volts) > len(pos_currents):
            pos_volts = pos_volts[:len(pos_currents)]

        # get regression data
        reg_data = self.stats_regression
        m = reg_data.slope
        b = reg_data.intercept

        # use slope and intercept to get positive regression values
        regression_vals = np.array([(m * x + b) if x > 0 else 1 for x in pos_volts])

        open_probability = pos_currents

        for index, curr in enumerate(pos_currents):
            if curr <= regression_vals[index]:
                open_probability[index] = curr / regression_vals[index]
            else:
                open_probability[index] = 1

        self.open_prob_vals = {"x": pos_volts, "y": open_probability}

    def get_open_probability(self):
        self.__calc_open_probability()
        return self.open_prob_vals

    def __get_pos_vals(self):
        pos_volts = np.array([x for x in self.voltages if x >= 0])
        pos_curr = np.array([x for x in self.currents if x >= 0])
        return {"v": pos_volts, "i": pos_curr}

    def get_op_for_saving(self):
        self.get_open_probability()
        self.__calc_open_probability()
        op_data = np.copy(self.open_prob_vals["y"], subok=True)
        while len(op_data) < len(self.regression_plot_data["x"]):
            op_data = np.insert(op_data, 0, 1, axis=0)

        return op_data
