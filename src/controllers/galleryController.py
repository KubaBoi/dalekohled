import os

from Cheese.cheeseController import CheeseController as cc
from Cheese.resourceManager import ResMan 

#@controller /gallery;
class GalleryController(cc):

    #@get /get;
    @staticmethod
    def get(server, path, auth):
        for root, dirs, files in os.walk(ResMan.web("gallery")):
            return cc.createResponse({"FILES": files})