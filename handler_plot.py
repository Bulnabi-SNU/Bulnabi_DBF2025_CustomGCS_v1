import pyqtgraph as pg

class HandlerPlot:
    def __init__(self, plot_widget, title, unit=None, window=100):
        self.window = window
        
        self.plot_widget = plot_widget
        self.plot_widget.setBackground('w')

        self.axis_left = pg.AxisItem(orientation='left')
        self.axis_left.setLabel(title, units=unit)
        self.axis_left.enableAutoSIPrefix(False)

        self.plot_widget.setAxisItems({'left': self.axis_left})
        self.plot_widget.setLabel('bottom', 'Samples')
        self.plot_widget.showGrid(x=True, y=True)
        # self.plot_widget.setYRange(-45, 45)

        self.curve = self.plot_widget.plot(pen='b')
        self.data_idx = 0
        self.list_index = []
        self.list_data = []

    def update_plot(self, data):
        self.list_index.append(self.data_idx)
        if len(self.list_index) > self.window:
            self.list_index.pop(0)
        self.data_idx += 1

        self.list_data.append(data)
        if len(self.list_data) > self.window:
            self.list_data.pop(0)

        self.curve.setData(self.list_index, self.list_data)
# TODO : plot clear method