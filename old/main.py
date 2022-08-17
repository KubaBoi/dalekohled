from camera import *
from streamServer import *

StreamingOutput.init()
Camera.init()

Camera.start_recording()
try:
    address = ("", 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    Camera.stop_recording()