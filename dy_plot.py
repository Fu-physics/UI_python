import numpy as np
from numpy import arange, sin, pi

import matplotlib
# Make sure that we are using QT5BB
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import matplotlib.animation as animation


class UI_figure:    
    def __init__(self, figure):
        self.figure = figure
        self.ax = figure.add_subplot(111)                       # a figure instance to plot on
        plt.ion()
    
    def UI_plot(self):
        ''' plot some random stuff '''
        

        self.line, = self.ax.plot([], [], animated=True)  
        #import to use "self.ax.plot" not "plt.plot" that will mix two figures
        
        self.xdata, self.ydata = [], []
        self.line.set_data(self.xdata, self.ydata) 
        self.ax.set_ylim(-2, 2)
        self.ax.set_xlim(0, 10)
        ani = animation.FuncAnimation(self.figure, self.update, self.data_gen, blit=True, interval=1,
                              repeat=True)
        # refresh canvas
        self.ax.figure.canvas.draw()
        
    def update(self, data):
        x, y = data
        self.xdata.append(x)
        self.ydata.append(y)
        xmin, xmax = self.ax.get_xlim()
        #print("x = ", x,"        ", "y =" , y)
        if x >= xmax:
        
            self.ax.set_xlim(0, 2*xmax)
            #plt.draw()
            self.ax.figure.canvas.draw()

            print("figure_axes changed")

        self.line.set_data(self.xdata, self.ydata)
        return self.line,

    def data_gen(self, t=0):
        cnt = 0
        while cnt < 1000:
            cnt += 1
            t += 0.1
            yield t, np.sin(t)
        self.line, = self.ax.plot([], [])  
        #import to use "self.ax_L.plot" not "plt.plot" that will mix two figures
        x = np.arange(0.0, 10.0, 0.1)
        y = sin(x)
        '''
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
            while cnt<1000:            
                data = task.read(number_of_samples_per_channel = 1)
                data_np = self.amp * np.asarray(data)
                cnt +=1
                t +=0.1
                yield t, data_np
        '''


        
    def UI_print(self):
        print("-----   Successful import UI_plot !  -------")