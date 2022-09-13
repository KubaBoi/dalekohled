

import time
import pygame
import socket

class Controller:

    @staticmethod
    def init(host, port):
        Controller.host = host
        Controller.port = port

    @staticmethod
    def controller_thread():
        pygame.init()

        hor_speed = 0
        vert_speed = 0

        joysticks = []
        for i in range(0, pygame.joystick.get_count()):
            # create an Joystick object in our list
            joysticks.append(pygame.joystick.Joystick(i))
            # initialize them all (-1 means loop forever)
            joysticks[-1].init()
            # print a statement telling what the name of the controller is
            print("Detected joystick ", joysticks[-1].get_name(),"'")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((Controller.host, Controller.port))
            while True:
                for event in pygame.event.get():
                    if (hasattr(event, "value")):
                        if (isinstance(event.value, tuple)):
                            print("D-pad", event.value)
                        else:
                            if (event.axis == 0):
                                hor_speed = int(event.value * 10)
                            elif (event.axis == 3):
                                if (event.value == 0): vert_speed = 0
                                else: vert_speed = int(event.value * -10)
                    elif (hasattr(event, "button")):
                        # The 0 button is the 'a' button, 1 is the 'b' button, 2 is the 'x' button, 3 is the 'y' button
                        print("Button", event.button)
                        if (event.button == 3):
                            command = "STOP"
                    
                s.sendall(bytes(f"{hor_speed}|{vert_speed}", "utf-8"))
                time.sleep(0.2)

Controller.init("192.168.0.108", 55573)
Controller.controller_thread()