
import serial
import time
import pygame

class ArduinoController:
    arduino = None
    hor_speed = 10
    vert_speed = 1

    @staticmethod
    def init(port="COM4", baudrate=115200, timeout=1):
        ArduinoController.arduino = serial.Serial(port, baudrate, timeout=timeout)
        for i in range(0, 5):
            ArduinoController.get_data()

    @staticmethod
    def write_read(text):
        ArduinoController.arduino.write(bytes(text, "utf-8"))
        time.sleep(0.05)
        data = ArduinoController.arduino.readline()
        return data.decode("utf-8")

    @staticmethod
    def write(text):
        ArduinoController.arduino.write(bytes(text, "utf-8"))

    @staticmethod
    def get_data():
        data_raw = ArduinoController.write_read("GET")
        data_list = data_raw.replace("DATA", "").replace("\r\n", "").split("|")
        if (len(data_list) < 3): return data_list
        data = []
        #try:
        for i in data_list:
            data.append(float(i))
        #except:
            #pass
        return data

    @staticmethod
    def move_while(horizontal_angle=-1, vertical_angle=-1):
        data = ArduinoController.get_data()
        z = data[0]
        y = data[1]

        hDir = ArduinoController.horizontal_direction(z, horizontal_angle)
        vDir = ArduinoController.vertical_direction(y, vertical_angle)

        ArduinoController.write(f"{hDir*ArduinoController.hor_speed}|{vDir*ArduinoController.vert_speed}")
        time.sleep(0.2)
        while True:
            data = ArduinoController.get_data()
            z = data[0]
            y = data[1]

            if (horizontal_angle == -1 and vertical_angle == -1): break 
            elif (horizontal_angle == -1):
                if (abs(horizontal_angle - z) <= 0.3): break
            elif (vertical_angle == -1):
                if (abs(vertical_angle - y) <= 0.3): break
            else:
                if (abs(horizontal_angle - z) <= 0.3):
                    ArduinoController.write("STOP")
                    ArduinoController.write(f"0|{vDir*ArduinoController.vert_speed}")
                if (abs(vertical_angle - y) <= 0.3):
                    ArduinoController.write("STOP")
                    ArduinoController.write(f"{hDir*ArduinoController.hor_speed}|0")

                if (abs(horizontal_angle - z) <= 0.3 and
                    abs(vertical_angle - y) <= 0.3): break
            time.sleep(0.2)
        
        ArduinoController.write("STOP")

    @staticmethod
    def horizontal_direction(act, wanted):
        dir = 1
        if (wanted != -1):
            if (act > wanted):
                if (act - wanted > 180):
                    dir = -1
        else: dir = 0
        return dir
    
    @staticmethod
    def vertical_direction(act, wanted):
        dir = 1
        if (wanted != -1):
            if (act > wanted):
                dir = -1
        else: dir = 0
        return dir

    @staticmethod
    def controller_thread():
        pygame.init()

        horSpeed = 0
        vertSpeed = 0

        joysticks = []
        for i in range(0, pygame.joystick.get_count()):
            # create an Joystick object in our list
            joysticks.append(pygame.joystick.Joystick(i))
            # initialize them all (-1 means loop forever)
            joysticks[-1].init()
            # print a statement telling what the name of the controller is
            print("Detected joystick ", joysticks[-1].get_name(),"'")

        while True:
            for event in pygame.event.get():
                if (hasattr(event, "value")):
                    if (isinstance(event.value, tuple)):
                        print("D-pad", event.value)
                    else:
                        if (event.axis == 0):
                            horSpeed = event.value * 10
                        elif (event.axis == 3):
                            vertSpeed = event.value * -10
                        else:
                            continue
                        print(f"{horSpeed}|{vertSpeed}")
                elif (hasattr(event, "button")):
                    # The 0 button is the 'a' button, 1 is the 'b' button, 2 is the 'x' button, 3 is the 'y' button
                    print("Button", event.button)
                    if (event.button == 3):
                        ArduinoController.write("STOP")
                
                ArduinoController.write(f"{horSpeed}|{vertSpeed}")
                time.sleep(0.1)

#ArduinoController.init()
#ArduinoController.move_while(100)
#ArduinoController.controller_thread()