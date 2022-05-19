import serial

#sudo rfcomm watch hci0
#python -m serial.tools.list_ports

ser = serial.Serial('/dev/rfcomm0')
ser.isOpen()

ser.write(str.encode(str(0)))
