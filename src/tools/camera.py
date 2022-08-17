import platform
if (platform.system() != "Windows"):
    import picamera

from Cheese.resourceManager import ResMan

from src.tools.streamingOutput import StreamingOutput

class Camera:

    @staticmethod
    def init():
        Camera.camera = picamera.PiCamera(resolution="1280x720", framerate=60)

    @staticmethod
    def start_recording():
        #camera.rotation = 90

        Camera.camera.annotate_text_size = 20
        Camera.camera.annotate_foreground = picamera.Color("white")
        Camera.camera.annotate_text = ("Framerate: %s" % (Camera.camera.framerate))

        Camera.camera.start_recording(StreamingOutput, format='mjpeg')
        print("Camera on")

    @staticmethod
    def stop_recording():
        Camera.camera.stop_recording()
        print("Camera off")

    @staticmethod
    def capture(name):
        Camera.camera.start_preview()
        #time.sleep(1)
        Camera.camera.capture(ResMan.web("gallery", name))
        Camera.camera.stop_preview()

    @staticmethod
    def changeFramerate():
        if (Camera.framerate == 60): #framerate 30 res 1920x1080
            Camera.resolution = (1920, 1080)
            Camera.framerate = 30
        else: #framerate 60 res 1280x720
            Camera.resolution = (1280, 720)
            Camera.framerate = 60

    @staticmethod
    def setCamera(args):
        Camera.camera.resolution = (int(args["RES"][0]), int(args["RES"][1]))
        Camera.camera.framerate = int(args["FPS"])
        if (args["ANN"] != ""):
            Camera.camera.annotate_text_size = 50
            Camera.camera.annotate_foreground = picamera.Color("white")
            Camera.camera.annotate_text = args["ANN"]
        else:
            Camera.camera.annotate_text = ""
        Camera.camera.brightness = int(args["BRI"])
        Camera.camera.contrast = int(args["CONT"])
        Camera.camera.exposure_mode = args["EXP"]
        Camera.camera.awb_mode = args["AWB"]

    @staticmethod
    def readCameraSettings():
        return {
            "FPS": Camera.camera.framerate,
            "RES": Camera.camera.resolution, 
            "ANN": Camera.camera.annotate_text, 
            "BRI": Camera.camera.brightness, 
            "CONT": Camera.camera.contrast, 
            "EXP": Camera.camera.exposure_mode, 
            "AWB": Camera.camera.awb_mode
        }