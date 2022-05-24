import time
import math
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class MQ3():

    ######################### Hardware Related Macros #########################
    RL_VALUE                     = 10       # define the load resistance on the board, in kilo ohms
    RO_CLEAN_AIR_FACTOR          = 60       # RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                            # which is derived from the chart in datasheet
 
    ######################### Software Related Macros #########################
    CALIBRATION_SAMPLE_TIMES     = 50       # define how many samples you are going to take in the calibration phase
    CALIBRATION_SAMPLE_INTERVAL  = 50       # define the time interval(in milisecond) between each samples in the
                                            # cablibration phase
    READ_SAMPLE_INTERVAL         = 50       # define the time interval(in milisecond) between each samples in
    READ_SAMPLE_TIMES            = 5        # define how many samples you are going to take in normal operation 
                                            # normal operation
 
    ######################### Application Related Macros ######################
    GAS_ALCOHOL                  = 0
    GAS_BENZINE                  = 1
    GAS_EXANE                    = 2
    GAS_LPG                      = 3
    GAS_CO                       = 4
    GAS_CH4                      = 5

    def __init__(self, Ro=10):
        self.Ro = Ro        
        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.D8)

        # create the mcp object
        mcp = MCP.MCP3008(spi, cs)

        # create an analog input channel on pin 1 for MQ3
        self.chan_MQ3 = AnalogIn(mcp, MCP.P1)
        
        self.AlcoholCurve = [-1,0.35,-0.54] # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent"
                                            # to the original curve. 
                                            # data format:{ x, y, slope}; point1: (lg0.1, 0.35), point2: (lg10, -0.72) 
        self.BenzineCurve = [-1,0.62,-0.36] # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg0.1, 0.62), point2: (lg10, -0.1)
        self.ExaneCurve =[-1,1.70,-0.35]    # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg0.1, 1.70), point2: (lg10,  1)
        self.LPGCurve =[-1,1.70,-0.28]      # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg0.1, 1.70), point2: (lg10, 1.15)
        self.COCurve =[-1,1.70,-0.23]       # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg0.1, 1.70), point2: (lg10, 1.23)
        self.CH4Curve =[-1,1.70,-0.05]      # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg0.1, 1.70), point2: (lg10, 1.60)
                
        print("Calibrating MQ-3...")
        self.Ro = self.MQ3_Calibration()
        print("Calibration of MQ-3 is done...")
        print("MQ-3 Ro=%f kohm" % self.Ro)
        print("\n")
    
    ######################### MQCalibration ####################################
    # Input:   mq_pin - analog channel
    # Output:  Ro of the sensor
    # Remarks: This function assumes that the sensor is in clean air. It use  
    #          MQResistanceCalculation to calculates the sensor resistance in clean air 
    #          and then divides it with RO_CLEAN_AIR_FACTOR. RO_CLEAN_AIR_FACTOR is about 
    #          60, which differs slightly between different sensors.
    ############################################################################ 
    def MQ3_Calibration(self):
        val = 0.0
        for i in range(self.CALIBRATION_SAMPLE_TIMES):          # take multiple samples
            val += self.MQResistanceCalculation(self.chan_MQ3.value)
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000.0)
            
        val = val/self.CALIBRATION_SAMPLE_TIMES                 # calculate the average value
        val = val/self.RO_CLEAN_AIR_FACTOR                      # divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                                # according to the chart in the datasheet 
        return val
        
    ######################### MQResistanceCalculation #########################
    # Input:   raw_adc - raw value read from adc, which represents the voltage
    # Output:  the calculated sensor resistance
    # Remarks: The sensor and the load resistor forms a voltage divider. Given the voltage
    #          across the load resistor and its resistance, the resistance of the sensor
    #          could be derived.
    ############################################################################ 
    def MQResistanceCalculation(self, raw_adc):
        # print(raw_adc)
        # 1023 for 3008()
        # https://github.com/tutRPi/Raspberry-Pi-Gas-Sensor-MQ
        
        # 65472 for circuit python
        # Even though the MCP3008 is a 10-bit ADC, the value returned is a 16-bit number to provide a consistent interface across ADCs in CircuitPython
        # https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx/blob/main/adafruit_mcp3xxx/analog_in.py#L50-L54
        
        if raw_adc == 0:
            raw_adc = 1
            
        return float(self.RL_VALUE * (65473.0-raw_adc) / float(raw_adc))    
      
    #########################  MQRead ##########################################
    # Input:   mq_pin - analog channel
    # Output:  Rs of the sensor
    # Remarks: This function use MQResistanceCalculation to caculate the sensor resistenc (Rs).
    #          The Rs changes as the sensor is in the different consentration of the target
    #          gas. The sample times and the time interval between samples could be configured
    #          by changing the definition of the macros.
    ############################################################################ 
    def MQRead(self):
        rs = 0.0
        raw_value = 0.0
        for i in range(self.READ_SAMPLE_TIMES):
            raw_value += self.chan_MQ3.value
            rs += self.MQResistanceCalculation(self.chan_MQ3.value)
            time.sleep(self.READ_SAMPLE_INTERVAL/1000.0)

        rs = rs / self.READ_SAMPLE_TIMES
        raw_value = raw_value / self.READ_SAMPLE_TIMES

        return rs, raw_value
    
    def MQPercentage(self):
        val = {}
        read, raw_value = self.MQRead()
        val["ALCOHOL"]  = self.MQGetGasPercentage(read/self.Ro, self.GAS_ALCOHOL)
        val["BENZINE"]  = self.MQGetGasPercentage(read/self.Ro, self.GAS_BENZINE)
        val["EXANE"]    = self.MQGetGasPercentage(read/self.Ro, self.GAS_EXANE)
        val["LPG"]      = self.MQGetGasPercentage(read/self.Ro, self.GAS_LPG)
        val["CO"]       = self.MQGetGasPercentage(read/self.Ro, self.GAS_CO)
        val["CH4"]      = self.MQGetGasPercentage(read/self.Ro, self.GAS_CH4)
        val["RAW_VALUE"]= raw_value
        return val
     
    #########################  MQGetGasPercentage ##############################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          gas_id      - target gas type
    # Output:  ppm of the target gas
    # Remarks: This function passes different curves to the MQGetPercentage function which 
    #          calculates the ppm (parts per million) of the target gas.
    ############################################################################ 
    def MQGetGasPercentage(self, rs_ro_ratio, gas_id):
        if ( gas_id == self.GAS_ALCOHOL ):
            return self.MQGetPercentage(rs_ro_ratio, self.AlcoholCurve)
        elif ( gas_id == self.GAS_BENZINE ):
            return self.MQGetPercentage(rs_ro_ratio, self.BenzineCurve)
        elif ( gas_id == self.GAS_EXANE ):
            return self.MQGetPercentage(rs_ro_ratio, self.ExaneCurve)
        elif ( gas_id == self.GAS_LPG ):
            return self.MQGetPercentage(rs_ro_ratio, self.LPGCurve)
        elif ( gas_id == self.GAS_CO ):
            return self.MQGetPercentage(rs_ro_ratio, self.COCurve)
        elif ( gas_id == self.GAS_CH4 ):
            return self.MQGetPercentage(rs_ro_ratio, self.CH4Curve)
        return 0
     
    #########################  MQGetPercentage #################################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          pcurve      - pointer to the curve of the target gas
    # Output:  ppm of the target gas
    # Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) 
    #          of the line could be derived if y(rs_ro_ratio) is provided. As it is a 
    #          logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic 
    #          value.
    ############################################################################ 
    def MQGetPercentage(self, rs_ro_ratio, pcurve):
        #print(rs_ro_ratio)
        #print((math.log(rs_ro_ratio)-pcurve[1]))
        #print(((math.log(rs_ro_ratio)-pcurve[1])/ pcurve[2]) + pcurve[0]))
        
        # This is the natural natural logarithm -> log(rs_ro_ratio)
        return (math.pow(10,(((math.log(rs_ro_ratio)-pcurve[1])/ pcurve[2]) + pcurve[0])))
    
    
    
    
