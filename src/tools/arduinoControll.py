
import serial
import time
arduinoMain = serial.Serial(port="COM4", baudrate=115200, timeout=1)
#arduinoDisplay = serial.Serial(port="COM3", baudrate=9600, timeout=.1)

def write_read(arduino, x):
    arduino.write(bytes(x, "utf-8"))
    time.sleep(0.05)
    data = arduino.readline()
    return data.decode("utf-8")

while True:
    # DATA-54.66|-57.00|27.47
    try:
        dataRaw = write_read(arduinoMain, "GET")
        if (dataRaw != ""):
            if (dataRaw.startswith("DATA")):
                data = dataRaw.replace("DATA", "").replace("\r\n", "").split("|")
                print(data)
            else:
                print(dataRaw.replace("\r\n", ""))
        else:
            print("ERROR")
            arduinoMain.close()
            arduinoMain = serial.Serial(port="COM4", baudrate=115200, timeout=1)
        arduinoMain.reset_output_buffer()
        time.sleep(0.1)
    except Exception as e:
        print(e)
        time.sleep(1)
        
