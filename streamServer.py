import time
import logging
import socketserver
from http import server

from camera import *
from streamOutput import *

PAGE="""\
<html>
<head>
<title>Rpi kamera</title>
</head>
<body>
<center><h1>Kamera</h1></center>
<center><img src="stream.mjpg" width="1920" height="1080"></center>
<a href="192.168.0.147">Foceni</a>
</body>
</html>
"""

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(301)
            self.send_header("Location", "/index.html")
            self.end_headers()
        elif self.path == "/index.html":
            content = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == "/stream.mjpg":
            self.send_response(200)
            self.send_header("Age", 0)
            self.send_header("Cache-Control", "no-cache, private")
            self.send_header("Pragma", "no-cache")
            self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=FRAME")
            self.end_headers()
            try:
                while True:
                    with StreamingOutput.condition:
                        StreamingOutput.condition.wait()
                        frame = StreamingOutput.frame
                    self.wfile.write(b"--FRAME\r\n")
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Content-Length", len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b"\r\n")
                    self.pause()
            except Exception as e:
                logging.warning(
                    "Removed streaming client %s: %s",
                    self.client_address, str(e))
        elif (self.path == "/capture"):
            Camera.capture("nanm")
        else:
            self.send_error(404)
            self.end_headers()

    def pause(self):
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

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
