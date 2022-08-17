
from Cheese.cheeseController import CheeseController as cc
from Cheese.cheeseNone import CheeseNone
from Cheese.Logger import Logger

from src.tools.camera import *
from src.tools.streamingOutput import StreamingOutput

#@controller /stream;
class StreamController(cc):

    #@get /get.mjpg;
    @staticmethod
    def get(server, path, auth):
        server.send_response(200)
        server.send_header("Age", 0)
        server.send_header("Cache-Control", "no-cache, private")
        server.send_header("Pragma", "no-cache")
        server.send_header("Content-Type", "multipart/x-mixed-replace; boundary=FRAME")
        server.end_headers()
        
        while True:
            with StreamingOutput.condition:
                StreamingOutput.condition.wait()
                frame = StreamingOutput.frame
            server.wfile.write(b"--FRAME\r\n")
            server.send_header("Content-Type", "image/jpeg")
            server.send_header("Content-Length", len(frame))
            server.end_headers()
            server.wfile.write(frame)
            server.wfile.write(b"\r\n")
            StreamController.pause()

        return CheeseNone()


    # METHODS

    def pause():
        p = "-"
        if (Camera.counter >= 10):
            file = open("./status.txt", "r")
            p = file.read()
            file.close()
            Camera.counter = 0

        if (len(p) < 1):
            p = "-"

        if (p[0] != "-" and p[0] != "1" and p[0] != "0"): #fotecka
            Camera.stop_recording()
            Camera.setCamera(True)
            Camera.capture(p)
            Camera.start_recording()
        elif (p[0] == "0"): #zmena framerate
            Camera.stop_recording()
            Camera.changeFramerate()
            Camera.start_recording()
        elif (p[0] == "1"): #zmena nastaveni
            Camera.stop_recording()
            Camera.setCamera(True)
            Camera.start_recording()

        Camera.counter += 1
        
