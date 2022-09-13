
from Cheese.cheeseController import CheeseController as cc

from src.tools.arduinoControll import ArduinoController

#@controller /movement;
class MovementController(cc):
    
    #@get /controller;
    @staticmethod
    def controller(server, path, auth):
        args = cc.getArgs(path)
        print(args)
        ArduinoController.write(args["command"])

        return cc.createResponse({"STATUS": "OK"})
        