import numpy as np
from numpy import arange, sin, pi

import matplotlib
# Make sure that we are using QT5BB
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import matplotlib.animation as animation

import nidaqmx
import time

class UI_figure:    
    def __init__(self, figure):
        self.sample_num = 500
        self.figure = figure
        self.ax = figure.add_subplot(111)                       # a figure instance to plot on
        
        plt.ion()
    
    def UI_plot(self):
        ''' plot some random stuff '''
        

        self.line, = self.ax.plot([], [], animated=True)  
        #import to use "self.ax.plot" not "plt.plot" that will mix two figures
        
        self.xdata, self.ydata = [], []
        self.line.set_data(self.xdata, self.ydata) 
        self.ax.set_ylim(-10, 10)
        self.ax.set_xlim(0, 5 * self.sample_num)
        ani = animation.FuncAnimation(self.figure, self.update, self.data_gen, blit=True, interval=1,
                              repeat=True)
        # refresh canvas
        self.ax.figure.canvas.draw()
        
    def update(self, data):
        x, y = data
        self.xdata.append(x)
        self.ydata.append(y)
        #print(self.xdata[-1])
        xmin, xmax = self.ax.get_xlim()
        #print("x = ", x,"        ", "y =" , y)
        #print(x[self.sample_num - 1])
        if x[self.sample_num - 1] >= xmax:
        
            self.ax.set_xlim(xmax, xmax + self.sample_num)
            #plt.draw()
            self.ax.figure.canvas.draw()

            print("figure_axes changed")

        self.line.set_data(self.xdata[-self.sample_num:], self.ydata[-self.sample_num:])
        return self.line,

    def data_gen(self, t=0):
        cnt = 0
        '''
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
            now = time.clock()
            task.ai_channels.add_ai_voltage_chan("Dev1/ai15")
            print ("\n\nIt took " + str(time.clock() - now) + "to connected with NI device")
            while cnt< 100*self.sample_num: 
                #now = time.clock()
                data = task.read(number_of_samples_per_channel = self.sample_num)
                #print ("\n\nIt took " + str(time.clock() - now) + " seconds to read the datas")
                
                data_np = np.asarray(data)
                t = cnt*self.sample_num + np.linspace(0,self.sample_num-1,self.sample_num)
                cnt +=1
                yield t, data_np


        
    def UI_print(self):
        print("-----   Successful import UI_plot !  -------")