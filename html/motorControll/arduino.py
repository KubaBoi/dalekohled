
import serial
import time
#script cte osy z arduina a zapisuje je do souboru

ser = serial.Serial("/dev/ttyACM0", 115200)
ser.baudrate=115200
while True:
	read_ser=ser.readline().decode("utf-8")

	if (read_ser[0] == "."):
		file = open("actLocation.txt", "w")
		file.write(read_ser)
		file.close()
		print(read_ser)
