
import datetime

from Cheese.cheeseController import CheeseController as cc

from src.tools.camera import *

#@controller /camera;
class CameraController(cc):

    #@post /changeSettings;
    @staticmethod
    def changeSettings(server, path, auth):
        args = cc.readArgs(server)
        cc.checkJson(["FPS", "RES", "ANN", "BRI", "CONT", "EXP", "AWB", "SS"], args)

        Camera.stop_recording()
        Camera.setCamera(args)
        Camera.start_recording()

        return cc.createResponse({"STATUS": "Changed"})

    #@get /readSettings;
    @staticmethod
    def readSettings(server, path, auth):
        return cc.createResponse(Camera.readCameraSettings())

    #@get /setDef;
    @staticmethod
    def setDef(server, path, auth):
        Camera.stop_recording()
        Camera.setDefault()
        Camera.start_recording()
        return cc.createResponse({"STATUS": "OK"})

    #@get /capture;
    @staticmethod
    def capture(server, path, auth):
        now = datetime.datetime.now()
        name = now.strftime("%Y_%m_%dT%H_%M_%S")

        Camera.stop_recording()
        Camera.capture(f"picture_{name}.png")
        Camera.start_recording()
        return cc.createResponse({"STATUS": "OK"})