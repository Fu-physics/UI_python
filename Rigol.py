import visa
import time
import sys
import os
import pandas as pd

import struct
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

class Rigol_app():
    def __init__(self):
    ## Number of Points to request
        self.USER_REQUESTED_POINTS = 1000
        self.GLOBAL_TOUT =  10000 # IO time out in milliseconds

        # Agilent TEC
        #self.SCOPE_VISA_ADDRESS = "USB0::0x0957::0x1734::MY44001859::0::INSTR" # Get this from Keysight IO Libraries Connection Expert

        ## rigol 
        self.SCOPE_VISA_ADDRESS = "USB0::0x1AB1::0x04CE::DS1ZB154600675::0::INSTR"

        sys.stdout.write("Preparing the Rigol_Scope ! ")


        self.rm = visa.ResourceManager()
        self.KsInfiniiVisionX = self.rm.open_resource(self.SCOPE_VISA_ADDRESS)
        self.KsInfiniiVisionX.timeout = self.GLOBAL_TOUT
        self.KsInfiniiVisionX.clear()           ## Clear the instrument bus

        self.preparing()



    def preparing(self):
        self.KsInfiniiVisionX.write(":WAVeform:FORMat WORD") # 16 bit word format... or BYTE for 8 bit format - WORD recommended, see more comments below when the data is actually retrieved
        print("/n")
        print("WAVeform:FORMat is:",self.KsInfiniiVisionX.query(":WAVeform:FORMat?"))


        self.KsInfiniiVisionX.write(":WAVeform:SOURce CHANnel1")
        self.KsInfiniiVisionX.write(":WAVeform:MODE NORM") 
        print("WAVeform:MODE is:",self.KsInfiniiVisionX.query(":WAVeform:MODE?"))
        ################################################################################################################

        self.KsInfiniiVisionX.write(":WAVeform:POINts 200")

        MAX_CURRENTLY_AVAILABLE_POINTS = int(self.KsInfiniiVisionX.query(":WAVeform:POINts?")) # This is the max number of points currently available - this is for on screen data only - Will not change channel to channel.
        print("MAX_CURRENTLY_AVAILABLE_POINTS is:", MAX_CURRENTLY_AVAILABLE_POINTS)

        ## Then ask how many points it will actually give you, as it may not give you exactly what you want.
        NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE = int(self.KsInfiniiVisionX.query(":WAVeform:POINts?"))
        print("NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE is:", NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE)
        
        Pre = self.KsInfiniiVisionX.query(":WAVeform:PREamble?").split(',') # This does need to be set to a channel that is on, but that is already done... e.g. Pre = KsInfiniiVisionX.query(":WAVeform:SOURce CHANnel" + str(FIRST_CHANNEL_ON) + ";PREamble?").split(',')
        ## While these values can always be used for all analog channels, they need to be retrieved and used separately for math/other waveforms as they will likely be different.
        #ACQ_TYPE    = float(Pre[1]) # Gives the scope Acquisition Type; this is already done above in this particular script
        self.X_INCrement = float(Pre[4]) # Time difference between data points; Could also be found with :WAVeform:XINCrement? after setting :WAVeform:SOURce
        self.X_ORIGin    = float(Pre[5]) # Always the first data point in memory; Could also be found with :WAVeform:XORigin? after setting :WAVeform:SOURce
        self.X_REFerence = float(Pre[6]) # Specifies the data point associated with x-origin; The x-reference point is the first point displayed and XREFerence is always 0.; Could also be found with :WAVeform:XREFerence? after setting :WAVeform:SOURce
        self.Y_INCrement = float(Pre[7]) # Time difference between data points; Could also be found with :WAVeform:XINCrement? after setting :WAVeform:SOURce
        self.Y_ORIGin    = float(Pre[8]) # Always the first data point in memory; Could also be found with :WAVeform:XORigin? after setting :WAVeform:SOURce
        self.Y_REFerence = float(Pre[9]) # Specifies the data point associated with x-origin; The x-reference point is the first point displayed and XREFerence is always 0.; Could also be found with :WAVeform:XREFerence? after setting :WAVeform:SOURce
        print("Pre is:", Pre)
        ## This could have been pulled earlier...
        
        
        self.delt_N =400
        if self.delt_N > MAX_CURRENTLY_AVAILABLE_POINTS:

            self.delt_N  = MAX_CURRENTLY_AVAILABLE_POINTS

        print("delt_N is:", self.delt_N)

    
    def get_data(self):
        self.Wav_Data = []
        DataTime = []
        for i in range(int(1200/self.delt_N)):
            #print(":WAV:STAR " +  str(i*self.delt_N+1))
            #print(":WAV:STOP "+  str((i+1)*self.delt_N))
            self.KsInfiniiVisionX.write(":WAV:STAR " +  str(i*self.delt_N+1))
            self.KsInfiniiVisionX.write(":WAV:STOP "+  str((i+1)*self.delt_N))
            self.data = np.array(self.KsInfiniiVisionX.query_binary_values(":WAV:DATA?", "h", False))
            #data = np.array(KsInfiniiVisionX.query(":WAV:DATA?"))   # this is for ASCii formate using
            #print(data)
            self.Wav_Data = np.append(self.Wav_Data, self.data)
        
        
        self.Wav_Data = ((self.Wav_Data-self.Y_REFerence)*self.Y_INCrement)+self.Y_ORIGin
        Number_data = (self.Wav_Data).size
        #print(Number_data)
        DataTime = ((np.linspace(0,Number_data-1,Number_data)-self.X_REFerence)*self.X_INCrement)+self.X_ORIGin

        return  DataTime, self.Wav_Data



if __name__ == "__main__":


    #DataTime = ((np.linspace(0,-1,)-X_REFerence)*X_INCrement)+X_ORIGin
    Rigol_scop = Rigol_app()
    Rigol_scop.preparing()


    now = time.clock() # Only to show how long it takes to transfer and scale the data.
    x, y  = Rigol_scop.get_data()

    print ("\n\nIt took " + str(time.clock() - now) + " seconds to transfer and scale ")
    plt.plot(x, y)
    plt.show()

    print("-----  The end !  --------")