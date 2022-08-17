
from Cheese.cheeseController import CheeseController as cc

from src.tools.camera import *

#@controller /camera;
class CameraController(cc):

    #@post /changeSettings;
    @staticmethod
    def changeSettings(server, path, auth):
        args = cc.readArgs(server)
        cc.checkJson(["FPS", "RES", "ANN", "BRI", "CONT", "EXP", "AWB", "SS"], args)

        Camera.setCamera(args)

        return cc.createResponse({"STATUS": "Changed"})

    #@get /readSettings;
    @staticmethod
    def readSettings(server, path, auth):
        return cc.createResponse(Camera.readCameraSettings())

    #@get /setDef;
    @staticmethod
    def setDef(server, path, auth):
        Camera.setDefault()
        return cc.createResponse({"STATUS": "OK"})

    #@get /capture;
    @staticmethod
    def capture(server, path, auth):
        Camera.stop_recording()
        Camera.capture("photo.png")
        Camera.start_recording()