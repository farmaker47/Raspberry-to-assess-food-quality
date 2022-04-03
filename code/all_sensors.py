from mq2 import *
from mq3 import *
from mq4 import *
from mq5 import *
from mq6 import *
from mq7 import *
from mq8 import *
from mq9 import *
from mq135 import *
import sys, time

filename = "mq_sensors_log.csv"

# Create header row in new CSV file
csv = open(filename, 'w')
csv.write("Timestamp,Raw_value_MQ2,Raw_value_MQ3,Raw_value_MQ4,Raw_value_MQ135,Raw_value_MQ6,Raw_value_MQ7,Raw_value_MQ8,Raw_value_MQ9, \n")
csv.close

try:
    print("Press CTRL+C to abort.\n")
    
    mq2 = MQ2()
    mq3 = MQ3()
    mq4 = MQ4()
    #mq5 = MQ5()
    mq135 = MQ135()
    mq6 = MQ6()
    mq7 = MQ7()
    mq8 = MQ8()
    mq9 = MQ9()
    
    now_time = time.time()
    
    while True:
        perc2 = mq2.MQPercentage()
        perc3 = mq3.MQPercentage()
        perc4 = mq4.MQPercentage()
        #perc5 = mq5.MQPercentage()
        perc6 = mq6.MQPercentage()
        perc7 = mq7.MQPercentage()
        perc8 = mq8.MQPercentage()
        perc9 = mq9.MQPercentage()
        perc135 = mq135.MQPercentage()
        print("MQ2 measurment")
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("Raw_value:   %g, \nLPG:         %g ppm, \nCO:          %g ppm, \nSmoke:       %g ppm, \nPropane:     %g ppm, \nH2:          %g ppm, \nAlcohol:     %g ppm, \nCH4:         %g ppm" % (perc2["RAW_VALUE"], perc2["GAS_LPG"], perc2["CO"], perc2["SMOKE"], perc2["PROPANE"], perc2["H2"], perc2["ALCOHOL"], perc2["CH4"]))
        sys.stdout.flush()
        print("\n\n")
        #time.sleep(0.1)
        print("MQ3 measurment")
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("Raw_value:   %g, \nAlcohol:     %g mg/L, \nBenzine:     %g mg/L, \nExane:       %g mg/L, \nLPG:         %g mg/L, \nCO:          %g mg/L, \nCH4:         %g mg/L" % (perc3["RAW_VALUE"], perc3["ALCOHOL"], perc3["BENZINE"], perc3["EXANE"], perc3["LPG"], perc3["CO"], perc3["CH4"]))
        sys.stdout.flush()
        print("\n\n")
        #time.sleep(0.1)
        print("MQ4 measurment")
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("Raw_value:   %g, \nCH4:         %g ppm, \nLPG:         %g ppm, \nH2:          %g ppm, \nSmoke:       %g ppm, \nAlcohol:     %g ppm, \nCO:          %g ppm" % (perc4["RAW_VALUE"], perc4["CH4"], perc4["LPG"], perc4["H2"], perc4["SMOKE"], perc4["ALCOHOL"], perc4["CO"]))
        sys.stdout.flush()
        print("\n\n")
        #time.sleep(0.1)
        print("MQ135 measurment")
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("Raw_value:   %g, \nACETON:      %g ppm, \nTOLUENO:     %g ppm, \nALCOHOL:     %g ppm, \nCO2:         %g ppm, \nNH4:         %g ppm, \nCO:          %g ppm" % (perc135["RAW_VALUE"], perc135["ACETON"], perc135["TOLUENO"], perc135["ALCOHOL"], perc135["CO2"], perc135["NH4"], perc135["CO"]))
        sys.stdout.flush()
        print("\n\n")
        #print("MQ5 measurment")
        #sys.stdout.write("\r")
        #sys.stdout.write("\033[K")
        #sys.stdout.write("Raw_value:   %g, \nLPG:         %g ppm, \nCH4:         %g ppm, \nH2:          %g ppm, \nAlcohol:     %g ppm, \nCO:          %g ppm" % (perc5["RAW_VALUE"], perc5["LPG"], perc5["CH4"], perc5["H2"], perc5["ALCOHOL"], perc5["CO"]))
        #sys.stdout.flush()
        #print("\n\n")
        #time.sleep(0.1)
        print("MQ6 measurment")
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("Raw_value:   %g, \nLPG:         %g ppm, \nCH4:         %g ppm, \nH2:          %g ppm, \nAlcohol:     %g ppm, \nCO:          %g ppm" % (perc6["RAW_VALUE"], perc6["LPG"], perc6["CH4"], perc6["H2"], perc6["ALCOHOL"], perc6["CO"]))
        sys.stdout.flush()
        print("\n\n")
        #time.sleep(0.1)
        print("MQ7 measurment")
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("Raw_value:   %g, \nH2:          %g ppm, \nCO:          %g ppm, \nLPG:         %g ppm, \nCH4:         %g ppm, \nAlcohol:     %g ppm" % (perc7["RAW_VALUE"], perc7["H2"], perc7["CO"], perc7["LPG"], perc7["CH4"], perc7["ALCOHOL"]))
        sys.stdout.flush()
        print("\n\n")
        #time.sleep(0.1)
        print("MQ8 measurment")
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("Raw_value:   %g, \nH2:          %g ppm, \nAlcohol:     %g ppm, \nLPG:         %g ppm, \nCH4:         %g ppm, \nCO:          %g ppm" % (perc8["RAW_VALUE"], perc8["H2"], perc8["ALCOHOL"], perc8["LPG"], perc8["CH4"], perc8["CO"]))
        sys.stdout.flush()
        print("\n\n")
        #time.sleep(0.1)
        print("MQ9 measurment")
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("Raw_value:   %g, \nCO:          %g ppm, \nLPG:         %g ppm, \nCH4:         %g ppm" % (perc9["RAW_VALUE"], perc9["CO"], perc9["LPG"], perc9["CH4"]))
        sys.stdout.flush()
        print("\n\n")
        
        # Write values to csv file
        entry = str(round((time.time() - now_time) / 60))
        entry = entry + "," + str(perc2["RAW_VALUE"]) + "," + str(perc3["RAW_VALUE"]) + "," + str(perc4["RAW_VALUE"]) + "," + str(perc135["RAW_VALUE"]) + "," + str(perc6["RAW_VALUE"]) + "," + str(perc7["RAW_VALUE"]) + "," + str(perc8["RAW_VALUE"]) + "," + str(perc9["RAW_VALUE"]) + "\n"

        # Log (append) entry into file
        csv = open(filename, 'a')
        try:
            csv.write(entry)
        finally:
            csv.close()
        
        
        time.sleep(58)
    
            
# Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
    
    #print csv
    csv = open(filename, 'r')
    print(csv.read())
    csv.close()

except:
    print("\nAbort by user")
    
