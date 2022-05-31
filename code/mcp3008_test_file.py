import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D8)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0 (from 0-7)
#chan0 = AnalogIn(mcp, MCP.P3)
chan1 = AnalogIn(mcp, MCP.P1)

#print('Raw ADC Value: ', chan.value)
#print('ADC Voltage: ' + str(chan.voltage) + 'V')

# create an analog input channel on pin 1
#chan = AnalogIn(mcp, MCP.P1)

#print('Raw ADC Value: ', chan.value)
#print('ADC Voltage: ' + str(chan.voltage) + 'V')

try:
    print("Press CTRL+C to abort.")
    
    while True:
        print('Raw ADC Value: ', chan0.value)
        print('ADC Voltage: ' + str(chan0.voltage) + 'V')
        time.sleep(0.5)
        
        #print('Raw ADC Value: ', chan1.value)
        #print('ADC Voltage: ' + str(chan1.voltage) + 'V')
        #time.sleep(0.5)
    
            
# Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")

except:
    print("\nAbort by user")
