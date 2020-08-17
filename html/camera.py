import time
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

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

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
                    self.pause()
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

    def pause(self):
        global cam
        p = "-"
        if (cam.counter >= 10):
            file = open("/var/www/html/status.txt", "r")
            p = file.read()
            file.close()
            cam.counter = 0

        if (len(p) < 1):
            p = "-"

        if (p[0] != "-" and p[0] != "1" and p[0] != "0"): #fotecka
            cam.stop_recording()
            cam.setCamera(True)
            cam.capture(p)
            cam.start_recording()
        elif (p[0] == "0"): #zmena framerate
            cam.stop_recording()
            cam.changeFramerate()
            cam.start_recording()
        elif (p[0] == "1"): #zmena nastaveni
            cam.stop_recording()
            cam.setCamera(True)
            cam.start_recording()

        cam.counter += 1

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

class camera:
    def __init__(self, output):
        self.camera = picamera.PiCamera(resolution="1280x720", framerate=60)
        self.output = output
        self.counter = 0
        self.resolution = (1280, 720)
        self.framerate = 60

    def start_session(self):
        self.start_recording()
        try:
            address = ("", 8000)
            server = StreamingServer(address, StreamingHandler)
            server.serve_forever()
        finally:
            self.stop_recording()

    def start_recording(self):
        #camera.rotation = 90
        self.setCamera(False)
        self.camera.resolution = self.resolution
        self.camera.framerate = self.framerate

        self.camera.annotate_text_size = 50
        self.camera.annotate_foreground = picamera.Color("white")
        self.camera.annotate_text = ("Framerate: %s" % (self.framerate))

        self.camera.start_recording(self.output, format='mjpeg')
        print("Camera on")

    def stop_recording(self):
        self.camera.stop_recording()
        print("Camera off")

    def capture(self, name):
        print("Capturing")
        self.camera.start_preview()
        #time.sleep(1)
        self.camera.capture("/var/www/html/gallery/%s" % (name))
        self.camera.stop_preview()

        file = open("/var/www/html/status.txt", "w")
        file.write("-")
        file.close()

    def changeFramerate(self):
        if (self.framerate == 60): #framerate 30 res 1920x1080
            self.resolution = (1920, 1080)
            self.framerate = 30
        else: #framerate 60 res 1280x720
            self.resolution = (1280, 720)
            self.framerate = 60

        file = open("/var/www/html/status.txt", "w")
        file.write("-")
        file.close()

    def setCamera(self, speak):
        file = open("/var/www/html/settings.txt", "r")
        settings = file.read()
        file.close()
        sett = settings.split('|')
        if (speak):
            print("Changing camera settings")
            print("Resolution: %sx%s" % (sett[0], sett[1]))
            print("Framerate: %s" % (sett[2]))
            print("Annotation: %s" % (sett[3]))
            print("Brightness: %s" % (sett[4]))
            print("Contrast: %s" % (sett[5]))
            print("Exposure mode: %s" % (sett[6]))
            print("AWB: %s" % (sett[7]))

        self.camera.resolution = (int(sett[0]), int(sett[1]))
        self.camera.framerate = int(sett[2])
        if (sett[3] != ""):
            self.camera.annotate_text_size = 50
            self.camera.annotate_foreground = picamera.Color("white")
            self.camera.annotate_text = sett[3]
        else:
            self.camera.annotate_text = ""
        self.camera.brightness = int(sett[4])
        self.camera.contrast = int(sett[5])
        self.camera.exposure_mode = sett[6]
        self.camera.awb_mode = sett[7]

        file = open("/var/www/html/status.txt", "w")
        file.write("-")
        file.close()

    def speak(self):
        print("Ziju")

output = StreamingOutput()
cam = camera(output)
cam.start_session()
