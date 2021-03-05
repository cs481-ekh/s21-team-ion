from matplotlib.backend_bases import key_press_handler
import numpy as np
# from xvfbwrapper import Xvfb


class PlotGUI:
    stored_data = None  # instance of StoredData class (storedData.py)

    def __init__(self, data):
        self.stored_data = data

    # @ staticmethod
    def plot_data(self, fig, canvas):
        """
        Updates the graph with the most recent data to plot.  Will plot the raw data (from the selected csv file),
        the linear regression of that data, and the min/max boundaries of the linear regression (which the user
        will be able to modify)

        :param fig: the matplotlib Figure being updated
        :param canvas: the tkinter Canvas that contains the matplotlib Figure
        """
        fig.clear()
        ax = fig.subplots()

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

        canvas.draw()

        canvas.mpl_connect(
            "key_press_event", lambda event: print(f"you pressed {event.key}"))
        canvas.mpl_connect("key_press_event", key_press_handler)

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
