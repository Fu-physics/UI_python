import matplotlib.pyplot as plt    

import numpy as np
from numpy import arange, sin, pi



class UI_figure:    
    def __init__(self, figure):
        self.ax = figure.add_subplot(111)                       # a figure instance to plot on
    
    def UI_plot(self):
        ''' plot some random stuff '''

        self.line, = self.ax.plot([], [])  
        #import to use "self.ax_L.plot" not "plt.plot" that will mix two figures
        x = np.arange(0.0, 10.0, 0.1)
        y = sin(x)

        self.line.set_data(x, y) 
        self.ax.relim()
        self.ax.autoscale_view(True,True,True)
        self.ax.figure.canvas.draw()
         # refresh canvas
        #self.ax.figure.canvas.draw()
        
    def UI_print(self):
        print("-----   Successful import UI_plot !  -------")