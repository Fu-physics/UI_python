from __future__ import unicode_literals
import sys
import os
import random
import time

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

# from dy_plot import UI_figure
import Scope_data

from UI_figure_anim_plot import UI_figure

from Rigol import Rigol_app


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

        self.button_scope_pre = QPushButton("Connecte to Scope")
        self.button_scope_pre.clicked.connect(self.connect_Scope)


        self.button_scope = QPushButton("Get Scope Figure")
        self.button_scope.clicked.connect(self.get_Scope_fig)

        self.button_plot_tab1 = QPushButton('Plot')           # Just some button connected to `plot` method
        self.button_plot_tab1.clicked.connect(self.plot_tab1)

        self.tab1_layout_R.addWidget(self.btn)             # add buttons onto tabl1.layout
        self.tab1_layout_R.addWidget(self.button_scope_pre)
        self.tab1_layout_R.addWidget(self.button_scope)
        self.tab1_layout_R.addWidget(self.button_plot_tab1)

        self.tab1_layout.addStretch()                     # put the plot_layout right side
        self.tab1_layout.addLayout(self.tab1_layout_R)    # here is "addLayout" not "addWedget"
        self.tab1.setLayout(self.tab1_layout)             # set tab1.layout to be the layout of tabl1       

    def initalUI_tab_2(self):

        #################### Create Plot cavas widget ###################################################
                                                         # Create first tab
        self.tab2_layout = QHBoxLayout(self)             # create a Layout, which will be setted for tab_2
        
        self.tab2_layout_R = QVBoxLayout(self)
        #self.figure_R =  plt.figure()
        #self.figure_R = plt.figure()
        self.figure_R = plt.figure()                      # a figure instance to plot on
        self.figure_L = plt.figure()
                                               #if put "plt.ion" on the head, which will make two more figures idependently.
        print(matplotlib.is_interactive())

        # this is the Canvas Widget that displays the `figure`, it takes the `figure` instance as a parameter to __init__
        self.canvas_R = FigureCanvas(self.figure_R)
        self.toolbar_R = NavigationToolbar(self.canvas_R, self) # this is the Navigation widget, it takes the Canvas widget and a parent
        self.button_plot_R = QPushButton('Plot')           # Just some button connected to `plot` method
        self.button_plot_R.clicked.connect(self.plot_R)      
        self.tab2_layout_R.addWidget(self.toolbar_R)         # this also needed to show the Navigation of plot
        self.tab2_layout_R.addWidget(self.canvas_R)          # add Canvas Widget(plot widget) onto tab_2
        self.tab2_layout_R.addWidget(self.button_plot_R)

        self.tab2_layout_L = QVBoxLayout(self)
        
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

        self.tab2.setLayout(self.tab2_layout)              # set tab2.layout to be the layout of tab_2       

    def get_Scope_fig(self):
        print("begin to get the Scope figure !")
        try:
            self.scope.get_data()
            print("Got the Scope's Figuer")
        except:
            print("Fail to get the Scope's Figuer. Do it again!")

        

    def connect_Scope(self):
        print("connecting with Scope")
        try:
            self.scope = Scope_data.OscilloScope_data(1000)
            self.scope.preparation()
            print("Connected with Scope.")
        except:
            print("Fail to connecte with Scope. Do it again!")


    def getInteger(self):
        i, okPressed = QInputDialog.getInt(self, "Get integer","Percentage:", 28, 0, 100, 1)
        print(okPressed)
        if okPressed:
            self.amp = i 
            print(i)
            print("amp = ", self.amp)

    def single_data_gen(self, t=0):
            cnt = 0
            t = 0
            while cnt < 1000:
                cnt += 1
                t += 0.1
                yield t, np.sin(t)
    def plot_L(self):

        method = "add"
        data = self.single_data_gen()
        app = UI_figure(self.figure_L, data, method)
        app.UI_Animation_plot()


    def array_data_gen(self, t = 0):
        cnt = 0
        sample_num = 300
        while cnt< 100*sample_num:
            t = (cnt*sample_num + np.linspace(0,sample_num-1,sample_num))*0.01
            data = np.sin(t)
            cnt +=1
            yield t, data

    def Rigol_data_gen(self):
        cnt = 1
        Rigol_scop = Rigol_app()
        Rigol_scop.preparing()

        while cnt:
            time, volt  = Rigol_scop.get_data()
            cnt +=1
            yield time, volt
    
    def plot_R(self):
        #method = "add"
        method = "renew"
        plot_axis =[-0.06,0.06,-1,6]
        #data = self.array_data_gen()
        data = self.Rigol_data_gen()
        app = UI_figure(self.figure_R, data, method, plot_axis)
        app.UI_Animation_plot()

 
    def plot_tab1(self):
        
        '''
        figure_tab1 = plt.figure()
        app = UI_figure(figure_tab1)
        app.UI_plot()
        app.UI_print()
        '''

 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    print("the last step!")
    sys.exit(app.exec_())