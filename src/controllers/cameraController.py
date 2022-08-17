
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

    #@get /readSettings;
    @staticmethod
    def readSettings(server, path, auth):
        return cc.createResponse(Camera.readCameraSettings())