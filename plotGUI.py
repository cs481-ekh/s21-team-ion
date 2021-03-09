from matplotlib.backend_bases import key_press_handler
import numpy as np
# from xvfbwrapper import Xvfb


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

    def __init__(self, data):
        self.stored_data = data
        self.cursor_boundary_extent = self.default_extent

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

        # get the raw data in a form that is easy to plot
        raw_data_plot = self.__raw_data_plot()

        # get the upper and lower regression boundary lines (vertical lines on either side of the graph)
        regression_bounds = self.__regression_bounds_plots()

        # get the simple linear regression for plotting
        regression_plot = self.__regression_plot()

        # plot raw data, regression boundaries, and regression
        self.ax.plot(raw_data_plot["x"], raw_data_plot["y"], label="raw data")
        self.ax.plot(regression_bounds["lower"], regression_bounds["y"], label="regression lower bound")
        self.ax.plot(regression_bounds["upper"], regression_bounds["y"], label="regression upper bound")
        self.ax.plot(regression_plot["x"], regression_plot["y"], label='I_max')

        canvas.draw()

        canvas.mpl_connect(
            "key_press_event", lambda event: print(f"you pressed {event.key}"))
        canvas.mpl_connect("key_press_event", key_press_handler)

        canvas.mpl_connect('button_press_event', self.__onclick)
        canvas.mpl_connect('button_release_event', self.__onrelease)
        canvas.mpl_connect('motion_notify_event', lambda event: self.__on_mouse_move(event, tkroot))

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

    def __onclick(self, event):
        self.is_dragging = True

    def __onrelease(self, event):
        self.is_dragging = False
        self.lower_dragging = False
        self.upper_dragging = False
        self.cursor_boundary_extent = self.default_extent

    def __on_mouse_move(self, event, tkroot):
        if self.stored_data.vertical_regression_line_points.any():
            if event.xdata:
                rgrmax_mouse_lower_bound = self.stored_data.regression_max - self.cursor_boundary_extent
                rgrmax_mouse_upper_bound = self.stored_data.regression_max + self.cursor_boundary_extent
                rgrmin_mouse_lower_bound = self.stored_data.regression_min - self.cursor_boundary_extent
                rgrmin_mouse_upper_bound = self.stored_data.regression_min + self.cursor_boundary_extent

                if rgrmax_mouse_lower_bound < event.xdata < rgrmax_mouse_upper_bound:
                    tkroot.config(cursor='size_we')
                    if self.is_dragging and not self.lower_dragging:
                        self.upper_dragging = True
                        self.__replot_boundary_line("max", event.xdata)
                        self.cursor_boundary_extent = self.drag_extent

                if rgrmin_mouse_lower_bound < event.xdata < rgrmin_mouse_upper_bound:
                    tkroot.config(cursor='size_we')
                    if self.is_dragging and not self.upper_dragging:
                        self.lower_dragging = True
                        self.__replot_boundary_line("min", event.xdata)
                        self.cursor_boundary_extent = self.drag_extent

                if not rgrmax_mouse_lower_bound < event.xdata < rgrmax_mouse_upper_bound and \
                   not rgrmin_mouse_lower_bound < event.xdata < rgrmin_mouse_upper_bound:
                    tkroot.config(cursor='arrow')

    def __replot_boundary_line(self, line, new_loc):
        if line == "max":
            if new_loc >= np.max(self.stored_data.voltages):
                new_loc = np.max(self.stored_data.voltages)
            elif new_loc <= self.stored_data.regression_min:
                new_loc = self.stored_data.regression_min + 1.0

            all_lines = self.ax.lines
            for l in all_lines:
                # find the upper boundary line in the collections, remove it, add the new boundary line, and redraw the canvas
                if l.get_label() == "regression upper bound":
                    l.remove()
                    regression_bounds = self.__regression_bounds_plots()
                    self.ax.plot(regression_bounds["upper"], regression_bounds["y"], label="regression upper bound")
                    self.stored_data.regression_max = new_loc
                    self.canvas.draw()
        elif line == "min":
            # if the new lower boundary line is greater than the upper boundary line, stop that from happening
            if new_loc >= self.stored_data.regression_max:
                new_loc = self.stored_data.regression_max - 1.0
            # if the new lower boundary line is less than the data, stop that from happening
            elif new_loc < np.min(self.stored_data.voltages):
                new_loc = np.min(self.stored_data.voltages)

            all_lines = self.ax.lines
            for l in all_lines:
                # find the lower boundary line in the collections, remove it, add the new boundary line, and redraw the canvas
                if l.get_label() == "regression lower bound":
                    l.remove()
                    regression_bounds = self.__regression_bounds_plots()
                    self.ax.plot(regression_bounds["lower"], regression_bounds["y"], label="regression lower bound")
                    self.stored_data.regression_min = new_loc
                    self.canvas.draw()

