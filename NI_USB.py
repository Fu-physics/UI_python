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
    

class NI_AI():

    def __init__(self):
        """

        There is no need to build the "Task" initally. If you do, you just can use one "Task", not multi, in this class.

        """
        pass

    
    def Read_Data(self, channle="Dev1/ai15", sample_num = 100):
        """
        1) Everytime you call "Read_Data" function, you should get a "Task" independently, which produce futuer works.

        2) You get two dimensional np.array datas, as "return t, amp"

        """

        print("Reading data....")
        cnt = 0
        self.sample_num = sample_num
        self.channle = channle

        with nidaqmx.Task() as task:
            now = time.clock()
            task.ai_channels.add_ai_voltage_chan(self.channle)
            print ("\n\nIt took " + str(time.clock() - now) + "to connected with NI device")
            while cnt< 100*self.sample_num: 
                now = time.clock()
                data = task.read(number_of_samples_per_channel = self.sample_num)
                print ("\n\nIt took " + str(time.clock() - now) + " seconds to read the datas")
                
                data_np = np.asarray(data)
                t = np.linspace(0,self.sample_num-1,self.sample_num)
                cnt +=1
                return t, data_np

            #task.close()   
            # 
            # #If no "with self.task as task",which can close the task automatically, ortherwise the ".close()" is needed. 

    


if __name__ == "__main__":
    app = NI_AI()

    
    data = app.Read_Data(sample_num = 500)
    t, amp = data
    plt.plot(t, amp)
    plt.show()
