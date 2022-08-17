
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
            #StreamController.pause()

        return CheeseNone()
        
