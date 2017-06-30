from __future__ import unicode_literals
import sys
import os
import random

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QPushButton, QMainWindow, QApplication
from PyQt5.QtWidgets import QWidget, QAction, QTabWidget,QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import numpy as np
from numpy import arange, sin, pi

import matplotlib
# Make sure that we are using QT5BB
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import nidaqmx

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 800
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.table_widget = MyTableWidget(self)   # creat a Widgat.
        self.setCentralWidget(self.table_widget)  # set the Widget to be CentralWidget of QMainWindow.
 
        self.show()
 
class MyTableWidget(QWidget):        
 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)

        self.amp = 1.0
        self.t=0
        self.cnt = 0

        self.layout = QVBoxLayout(self)           # create a Layout, which will be setted for self

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()   
        self.tab2 = QWidget()
        #self.tabs.resize(800,600) 
        
        self.tabs.addTab(self.tab1,"Tab 1")       # Add tabs
        self.tabs.addTab(self.tab2,"Tab 2")
 
        self.layout.addWidget(self.tabs)          # Add tabs to widget

        self.setLayout(self.layout)

        self.initalUI_tab_1()
        self.initalUI_tab_2()

    def initalUI_tab_1(self):
                                                         # Create first tab
        self.tab1_layout = QHBoxLayout(self)             # create a Layout, which will be setted for tab1

        self.tab1_layout_R = QVBoxLayout(self)
        self.btn = QPushButton('getInteger', self)
        self.btn.clicked.connect(self.getInteger)
        self.pushButton1 = QPushButton("PyQt5 button")
        self.tab1_layout_R.addWidget(self.btn)             # add buttons onto tabl1.layout
        self.tab1_layout_R.addWidget(self.pushButton1)

        self.tab1_layout.addStretch()                     # put the plot_layout right side
        self.tab1_layout.addLayout(self.tab1_layout_R)    # here is "addLayout" not "addWedget"
        self.tab1.setLayout(self.tab1_layout)             # set tab1.layout to be the layout of tabl1       

    def initalUI_tab_2(self):

        #################### Create Plot cavas widget ###################################################
                                                         # Create first tab
        self.tab2_layout = QHBoxLayout(self)             # create a Layout, which will be setted for tab_2
        
        self.tab2_layout_R = QVBoxLayout(self)
        self.figure_R = plt.figure()
        #self.figure_R, self.ax_R = plt.subplots()                       # a figure instance to plot on
        # this is the Canvas Widget that displays the `figure`, it takes the `figure` instance as a parameter to __init__
        self.canvas_R = FigureCanvas(self.figure_R)
        self.toolbar_R = NavigationToolbar(self.canvas_R, self) # this is the Navigation widget, it takes the Canvas widget and a parent
        self.button_plot_R = QPushButton('Plot')           # Just some button connected to `plot` method
        self.button_plot_R.clicked.connect(self.plot_R)      
        self.tab2_layout_R.addWidget(self.toolbar_R)         # this also needed to show the Navigation of plot
        self.tab2_layout_R.addWidget(self.canvas_R)          # add Canvas Widget(plot widget) onto tab_2
        self.tab2_layout_R.addWidget(self.button_plot_R)

        self.tab2_layout_L = QVBoxLayout(self)
        self.figure_L = plt.figure()
        #self.figure_R, self.ax_R = plt.subplots()                       # a figure instance to plot on
        # this is the Canvas Widget that displays the `figure`, it takes the `figure` instance as a parameter to __init__
        self.canvas_L = FigureCanvas(self.figure_L)
        self.toolbar_L = NavigationToolbar(self.canvas_L, self) # this is the Navigation widget, it takes the Canvas widget and a parent
        self.button_plot_L = QPushButton('Plot')           # Just some button connected to `plot` method
        self.button_plot_L.clicked.connect(self.plot_L)      
        self.tab2_layout_L.addWidget(self.toolbar_L)         # this also needed to show the Navigation of plot
        self.tab2_layout_L.addWidget(self.canvas_L)          # add Canvas Widget(plot widget) onto tab_2
        self.tab2_layout_L.addWidget(self.button_plot_L)



        self.tab2_layout.addLayout(self.tab2_layout_L)
        self.tab2_layout.addStretch()                      # put the plot_layout right side
        self.tab2_layout.addLayout(self.tab2_layout_R)
        ############################################################################################

        self.tab2.setLayout(self.tab2_layout)            # set tab2.layout to be the layout of tab_2       


    def plot_L(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # instead of ax.hold(False)
        self.figure_L.clear()

        # create an axis
        ax_L = self.figure_L.add_subplot(111)

        # plot data
        ax_L.plot(data, '*-')

        # refresh canvas
        self.canvas_L.draw()

        

    def getInteger(self):
        i, okPressed = QInputDialog.getInt(self, "Get integer","Percentage:", 28, 0, 100, 1)
        print(okPressed)
        if okPressed:
            self.amp = i 
            print(i)
            print("amp = ", self.amp)
    
    def plot_R(self):
        ''' plot some random stuff '''
        self.ax_R = self.figure_R.add_subplot(111)

        self.line_R, = self.ax_R.plot([], [], animated=True)  
        #import to use "self.ax_R.plot" not "plt.plot" that will mix two figures
        
        self.xdata_R, self.ydata_R = [], []
        self.line_R.set_data(self.xdata_R, self.ydata_R) 
        self.ax_R.set_ylim(-2, 2)
        self.ax_R.set_xlim(0, 10)
        
        ani = animation.FuncAnimation(self.figure_R, self.update, self.data_gen, blit=True, interval=1,
                              repeat=True)
        #self.figure_R.show()
        # refresh canvas
        #self.figure_R.canvas.draw()
        self.ax_R.figure.canvas.draw()


    def update(self, data):
        x, y = data
        self.xdata_R.append(x)
        self.ydata_R.append(y)
        xmin, xmax = self.ax_R.get_xlim()
        #print("x = ", x,"        ", "y =" , y)
        if x >= xmax:
            self.ax_R.set_xlim(0, 2*xmax)
            self.ax_R.figure.canvas.draw()
            #self.canvas_R.draw()
            print("figure_axes changed")

        self.line_R.set_data(self.xdata_R, self.ydata_R)
        return self.line_R,

    def data_gen(self, t=0):
        cnt = 0
        while cnt < 1000:
            cnt += 1
            t += 0.1
            yield t, np.sin(t)
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

 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    print("the last step!")
    sys.exit(app.exec_())