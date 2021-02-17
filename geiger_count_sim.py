import sys
import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)
        self.samprate = 200 # milliseconds, set the sampling rate 
        self.distance = 4 # set at 1 gives a mu of 25 at 200 msec sampling rate
        self.mu = round(self.samprate/(200*(0.2*self.distance)**2))
        self.std = np.sqrt(self.mu) # standard deviation for gaussian, can be set at other values
        self.ydata = [round(np.random.poisson(self.mu))] # use this for poisson
        #self.ydata = [max(0, round(np.random.normal(self.mu, self.std)))] # use this for gaussian    
        self.numdata = 20 # how many data points are needed based on sampling rate and runtime
        
        self.update_plot()
        self.show()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.samprate) 
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        self.ydata = self.ydata + [round(np.random.poisson(self.mu))] # use this for poisson
        #self.ydata = self.ydata + [max(0, round(np.random.normal(self.mu, self.std)))] # use this for gaussian
        self.canvas.axes.cla()  
        self.canvas.axes.hist(self.ydata, bins = [int(i) for i in range(max(self.ydata)+2)])
        self.canvas.axes.set_ylabel('Occurrences')
        self.canvas.axes.set_xlabel('Counts per time bin')
        self.canvas.axes.set_title('Geiger counter plotting simulator')
        self.counts = self.ydata
        self.canvas.draw()
        if len(self.ydata) == self.numdata:
            self.close()

    def closeEvent(self, event):
        super().closeEvent(event)
        print('Counts:', self.counts)

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
