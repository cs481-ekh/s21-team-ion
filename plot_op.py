from matplotlib.backend_bases import key_press_handler
import numpy as np
import tkinter  # this is for the tkinter.END variable


class PlotOp:
    stored_data = None  # instance of StoredData class (storedData.py)
    figure = None  # instance of mpl.Figure class
    ax = None  # instead of mpl.Axes class
    canvas = None

    def __init__(self, data):
        self.stored_data = data

    def plot_data(self, fig, canvas, tkroot):
        """
        Updates the graph with the most recent data to plot open probability

        :param fig: the matplotlib Figure being updated
        :param canvas: the tkinter Canvas that contains the matplotlib Figure
        :param tkroot: tk root class.  Only used for passing to event handlers
        """
        fig.clear()
        self.figure = fig
        self.ax = fig.subplots()
        self.ax.set_title("Open Probability")
        self.ax.set_ylabel("Probability")
        self.ax.set_xlabel("Voltage (mV)")
        self.canvas = canvas

        # get positive voltage and current values
        op_vals = self.stored_data.get_open_probability()
        pos_volts, open_probability = op_vals["x"], op_vals["y"]

        self.ax.plot(pos_volts, open_probability)

        canvas.draw()

    def get_pos_volts(self):
        all_volts = self.stored_data.voltages
        return np.array([x for x in all_volts if x >= 0])

    def get_pos_currs(self):
        all_currs = self.stored_data.currents
        return np.array([x for x in all_currs if x >= 0])
