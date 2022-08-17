import picamera

from streamServer import *

class camera:
    def __init__(self):
        self.camera = picamera.PiCamera(resolution="1280x720", framerate=60)
        self.counter = 0
        self.resolution = (1280, 720) # 2592|1944|15||40|38|auto|auto|
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
        self.setCamera(True)
        self.camera.resolution = self.resolution
        self.camera.framerate = self.framerate

        self.camera.annotate_text_size = 50
        self.camera.annotate_foreground = picamera.Color("white")
        self.camera.annotate_text = ("Framerate: %s" % (self.framerate))

        self.camera.start_recording(StreamingOutput, format='mjpeg')
        print("Camera on")

    def stop_recording(self):
        self.camera.stop_recording()
        print("Camera off")

    def capture(self, name):
        print("Capturing")
        self.camera.start_preview()
        #time.sleep(1)
        self.camera.capture("./gallery/%s" % (name))
        self.camera.stop_preview()

        file = open("./status.txt", "w")
        file.write("-")
        file.close()

    def changeFramerate(self):
        if (self.framerate == 60): #framerate 30 res 1920x1080
            self.resolution = (1920, 1080)
            self.framerate = 30
        else: #framerate 60 res 1280x720
            self.resolution = (1280, 720)
            self.framerate = 60

        file = open("./status.txt", "w")
        file.write("-")
        file.close()

    def setCamera(self, speak):
        file = open("./settings.txt", "r")
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

        file = open("./status.txt", "w")
        file.write("-")
        file.close()

    def speak(self):
        print("Ziju")