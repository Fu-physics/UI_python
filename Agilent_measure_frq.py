import visa
import time
# start of Untitled

frequency=0

rm = visa.ResourceManager()
#rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
Fu_DSO6034A = rm.open_resource('USB0::0x0957::0x1734::MY44001859::0::INSTR')
idn = Fu_DSO6034A.query('*IDN?')
Fu_DSO6034A.write(':AUToscale %s' % ('CHANnel1'))
temp_values = Fu_DSO6034A.query_ascii_values(':MEASure:VMIN? %s' % ('CHANnel1'))

value = temp_values[0]
temp_values = Fu_DSO6034A.query_ascii_values(':MEASure:FREQuency? %s' % ('CHANnel1'))
print("temp_values is:", temp_values)
frequency = temp_values[0]
print("frequency = ",frequency)
Fu_DSO6034A.close()
rm.close()

# end of Untitled
