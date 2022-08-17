
from Cheese.cheeseController import CheeseController as cc

from src.tools.camera import *

#@controller /camera;
class CameraController(cc):

    #@post /changeSettings;
    @staticmethod
    def changeSettings(server, path, auth):
        args = cc.readArgs(server)
        cc.checkJson(["FPS", "RES", "ANN", "BRI", "CONT", "EXP", "AWB"], args)

        Camera.setCamera(args)

        return cc.createResponse({"STATUS": "Changed"})

    #@get /readSettings;
    @staticmethod
    def readSettings(server, path, auth):
        return cc.createResponse(Camera.readCameraSettings())

    #@get /capture;
    @staticmethod
    def capture(server, path, auth):
        args = cc.readArgs(server)
        cc.checkJson(["FPS", "RES", "ANN", "BRI", "CONT", "EXP", "AWB"], args)

        Camera.stop_recording()
        Camera.setCamera(args)
        Camera.capture("photo.png")
        Camera.setDefault()
        Camera.start_recording()