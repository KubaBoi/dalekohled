import os

from Cheese.cheeseController import CheeseController as cc
from Cheese.resourceManager import ResMan 

from src.tools.camera import *

#@controller /gallery;
class CameraController(cc):

    #@get /get;
    @staticmethod
    def get(server, path, auth):
        for root, dirs, files in os.walk(ResMan.web("gallery")):
            return cc.createResponse({"FILES": files})