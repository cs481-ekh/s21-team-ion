from matplotlib.lines import Line2D
import numpy as np
import tkinter  # this is for the tkinter.END variable


class PlotGUI:
    stored_data = None  # instance of StoredData class (storedData.py)
    cursor_boundary_extent = None  # float
    default_extent = 5.0
    drag_extent = 10000.0
    cursor_xdata = None  # float
    cursor_ydata = None  # float
    is_dragging = None
    lower_dragging = None  # bool
    upper_dragging = None  # bool
    figure = None  # instance of mpl.Figure class
    ax = None  # instead of mpl.Axes class
    canvas = None
    lower_regression_boundary = None  # instance of Line2D class
    upper_regression_boundary = None  # instance of Line2D class
    linear_regression = None  # instance of Line2D class
    raw_data = None  # instance of Line2D class
    highest_ymax_seen = 0  # int, sets the y axis graph boundary

    def __init__(self, data, leftEntry, rightEntry):
        self.stored_data = data
        self.cursor_boundary_extent = self.default_extent
        self.leftEntry = leftEntry
        self.rightEntry = rightEntry

    def update_textbox(self):
        min_text = round(self.stored_data.regression_min, 3)
        max_text = round(self.stored_data.regression_max, 3)
        self.leftEntry.delete(0, tkinter.END)
        self.rightEntry.delete(0, tkinter.END)
        self.leftEntry.insert(0, min_text)
        self.rightEntry.insert(0, max_text)

    # @ staticmethod
    def plot_data(self, fig, canvas, tkroot):
        """
        Updates the graph with the most recent data to plot.  Will plot the raw data (from the selected csv file),
        the linear regression of that data, and the min/max boundaries of the linear regression (which the user
        will be able to modify)

        :param fig: the matplotlib Figure being updated
        :param canvas: the tkinter Canvas that contains the matplotlib Figure
        :param tkroot: tk root class.  Only used for passing to event handlers
        """
        fig.clear()
        self.figure = fig
        self.ax = fig.subplots()
        self.canvas = canvas
        self.ax.set_title('Raw Data')
        self.ax.set_ylabel('Current (nA)')
        self.ax.set_xlabel('Voltage (mV)')

        # get the raw data in a form that is easy to plot
        raw_data_plot = self.__raw_data_plot()

        # get the upper and lower regression boundary lines (vertical lines on either side of the graph)
        regression_bounds = self.__regression_bounds_plots()

        # get the simple linear regression for plotting
        regression_plot = self.__regression_plot()

        # plot raw data, regression boundaries, and regression
        self.raw_data = Line2D(raw_data_plot["x"], raw_data_plot["y"])
        self.raw_data.set_label("raw data")
        self.ax.add_line(self.raw_data)

        self.lower_regression_boundary = Line2D(regression_bounds["lower"], regression_bounds["y"], label="regression lower bound")
        self.lower_regression_boundary.set_color("black")
        self.ax.add_line(self.lower_regression_boundary)

        self.upper_regression_boundary = Line2D(regression_bounds["upper"], regression_bounds["y"], label="regression lower bound")
        self.upper_regression_boundary.set_color("gold")
        self.ax.add_line(self.upper_regression_boundary)

        self.linear_regression = Line2D(regression_plot["x"], regression_plot["y"], label="I_max")
        self.linear_regression.set_color("red")
        self.ax.add_line(self.linear_regression)

        self.recalc_axes()

        # self.figure.tight_layout()
        canvas.draw()

        canvas.mpl_connect('button_press_event', self.__onclick)
        canvas.mpl_connect('button_release_event', lambda event: self.__onrelease(event, tkroot))
        canvas.mpl_connect('motion_notify_event', lambda event: self.__on_mouse_move(event, tkroot))

    def update_from_textbox(self, line, val):
        self.__replot_boundary_line(line, val)

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
        return self.stored_data.get_regression_data()

    def __onclick(self, event):
        self.is_dragging = True

    def __onrelease(self, event, tkroot):
        self.is_dragging = False
        self.lower_dragging = False
        self.upper_dragging = False
        self.cursor_boundary_extent = self.default_extent
        tkroot.config(cursor='arrow')

    def __on_mouse_move(self, event, tkroot):
        if self.stored_data.vertical_regression_line_points.any():
            if event.xdata:
                rgrmax_mouse_lower_bound = self.stored_data.regression_max - self.cursor_boundary_extent
                rgrmax_mouse_upper_bound = self.stored_data.regression_max + self.cursor_boundary_extent
                rgrmin_mouse_lower_bound = self.stored_data.regression_min - self.cursor_boundary_extent
                rgrmin_mouse_upper_bound = self.stored_data.regression_min + self.cursor_boundary_extent

                if rgrmax_mouse_lower_bound < event.xdata < rgrmax_mouse_upper_bound:
                    tkroot.config(cursor='sb_h_double_arrow')
                    if self.is_dragging and not self.lower_dragging:
                        self.upper_dragging = True
                        self.__replot_boundary_line("max", event.xdata)
                        self.cursor_boundary_extent = self.drag_extent

                if rgrmin_mouse_lower_bound < event.xdata < rgrmin_mouse_upper_bound:
                    tkroot.config(cursor='sb_h_double_arrow')
                    if self.is_dragging and not self.upper_dragging:
                        self.lower_dragging = True
                        self.__replot_boundary_line("min", event.xdata)
                        self.cursor_boundary_extent = self.drag_extent

                if not rgrmax_mouse_lower_bound < event.xdata < rgrmax_mouse_upper_bound and \
                   not rgrmin_mouse_lower_bound < event.xdata < rgrmin_mouse_upper_bound:
                    tkroot.config(cursor='arrow')

    def __replot_boundary_line(self, line, new_loc):
        """
        Redraws the canvas with a new upper or lower boundary line (depending on which one is being modified
        on this tick).  Separate function from plot_gui() so that plot_gui() is not recursively called, leading to
        a stack overflow

        :param line: which regression boundary line that is being modified ("min" or "max")
        :param new_loc: the new x location of this boundary line (y-values are constant)
        """
        if line == "max":
            if new_loc >= np.max(self.stored_data.voltages):
                new_loc = np.max(self.stored_data.voltages)
            elif new_loc <= self.stored_data.regression_min:
                new_loc = self.stored_data.regression_min + 1.0

            self.stored_data.regression_max = new_loc
            regression_bounds = self.__regression_bounds_plots()
            self.upper_regression_boundary.set_data(regression_bounds["upper"], regression_bounds["y"])

        elif line == "min":
            # if the new lower boundary line is greater than the upper boundary line, stop that from happening
            if new_loc >= self.stored_data.regression_max:
                new_loc = self.stored_data.regression_max - 1.0
            # if the new lower boundary line is less than the data, stop that from happening
            elif new_loc < np.min(self.stored_data.voltages):
                new_loc = np.min(self.stored_data.voltages)

            self.stored_data.regression_min = new_loc
            regression_bounds = self.__regression_bounds_plots()
            self.lower_regression_boundary.set_data(regression_bounds["lower"], regression_bounds["y"])

        regression = self.__regression_plot()
        self.linear_regression.set_data(regression["x"], regression["y"])

        self.recalc_axes()
        self.canvas.draw()
        self.update_textbox()

    def recalc_axes(self):
        x_min = np.min(self.stored_data.voltages) - 3
        x_max = np.max(self.stored_data.voltages) + 3
        y_min = np.min(self.stored_data.currents) - 1

        curr_y_max = np.max(self.stored_data.currents)
        regr_y_max = np.max(self.stored_data.get_regression_data()["y"])
        y_max = None
        if curr_y_max > regr_y_max:
            y_max = curr_y_max
        else:
            y_max = regr_y_max

        if y_max > self.highest_ymax_seen:
            self.highest_ymax_seen = y_max
        else:
            y_max = self.highest_ymax_seen

        if y_max > self.highest_ymax_seen:
            self.highest_ymax_seen = y_max
        else:
            y_max = self.highest_ymax_seen

        y_max = y_max + 1
        self.ax.set_xlim([x_min, x_max])
        self.ax.set_ylim([y_min, y_max])
