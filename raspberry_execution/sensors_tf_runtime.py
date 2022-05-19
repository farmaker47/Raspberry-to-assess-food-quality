import tflite_runtime.interpreter as tflite
import numpy as np
from mq2 import *
from mq3 import *
from mq4 import *
#from mq5 import *
from mq6 import *
from mq7 import *
from mq8 import *
from mq9 import *
from mq135 import *
import serial
            
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
        
    while True:
        string = input()
        if string == "a":
            perc2 = mq2.MQPercentage()
            perc3 = mq3.MQPercentage()
            perc4 = mq4.MQPercentage()
            #perc5 = mq5.MQPercentage()
            perc6 = mq6.MQPercentage()
            perc7 = mq7.MQPercentage()
            perc8 = mq8.MQPercentage()
            perc9 = mq9.MQPercentage()
            perc135 = mq135.MQPercentage()
            
            # Divide per 65472
            MAX_SENSOR_VALUE = 65472
            lst = [str(perc2["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   str(perc3["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   str(perc4["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   str(perc135["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   str(perc6["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   str(perc7["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   str(perc8["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   str(perc9["RAW_VALUE"] / MAX_SENSOR_VALUE)]
            lst_of_floats = [(perc2["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   (perc3["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   (perc4["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   (perc135["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   (perc6["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   (perc7["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   (perc8["RAW_VALUE"] / MAX_SENSOR_VALUE),
                   (perc9["RAW_VALUE"] / MAX_SENSOR_VALUE)]
            print(lst_of_floats)
            #lst = ["0.02443793","0.09071359","0.01564027", "0.0173998", "0.01857283","0.028348","0.02561095", "0.01955034"]
            
            input_array = []
            for item in lst:
                input_array.append(float(item))

            test_features = np.array(input_array).astype(np.float32)
            test_features = np.expand_dims(test_features, axis=0)
            # Load the TFLite model and allocate tensors.
            interpreter = tflite.Interpreter(model_path="food_model_250.tflite")
            interpreter.allocate_tensors()

            # Get input and output tensors details.
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            #print(input_details)
            #print(output_details)

            interpreter.set_tensor(input_details[0]['index'], test_features)

            interpreter.invoke()

            # The function `get_tensor()` returns a copy of the tensor data.
            # Use `tensor()` in order to get a pointer to the tensor.
            output_data = interpreter.get_tensor(output_details[0]['index'])
            print(output_data)
            max_array_value_indice = np.argmax(output_data[0])
            print(max_array_value_indice)
            
            # Send data to mobile.
            ser = serial.Serial('/dev/rfcomm0')
            ser.isOpen()
            ser.write(str.encode(str(max_array_value_indice)))
            
            print("OK")
        else:
            # Send data to mobile.
            ser = serial.Serial('/dev/rfcomm0')
            ser.isOpen()
            ser.write(str.encode(str(2)))
            
# Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")

except:
    print("\nAborted by user")