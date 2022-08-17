import platform
if (platform.system() != "Windows"):
    import picamera

from src.tools.streamingOutput import StreamingOutput

class Camera:

    @staticmethod
    def init():
        Camera.camera = picamera.PiCamera(resolution="1280x720", framerate=60)
        Camera.counter = 0
        Camera.resolution = (1280, 720) # 2592|1944|15||40|38|auto|auto|
        Camera.framerate = 60

    @staticmethod
    def start_recording():
        #camera.rotation = 90
        Camera.setCamera(True)
        Camera.camera.resolution = Camera.resolution
        Camera.camera.framerate = Camera.framerate

        Camera.camera.annotate_text_size = 50
        Camera.camera.annotate_foreground = picamera.Color("white")
        Camera.camera.annotate_text = ("Framerate: %s" % (Camera.framerate))

        Camera.camera.start_recording(StreamingOutput, format='mjpeg')
        print("Camera on")

    @staticmethod
    def stop_recording():
        Camera.camera.stop_recording()
        print("Camera off")

    @staticmethod
    def capture(name):
        print("Capturing")
        Camera.camera.start_preview()
        #time.sleep(1)
        Camera.camera.capture("./gallery/%s" % (name))
        Camera.camera.stop_preview()

        file = open("./status.txt", "w")
        file.write("-")
        file.close()

    @staticmethod
    def changeFramerate():
        if (Camera.framerate == 60): #framerate 30 res 1920x1080
            Camera.resolution = (1920, 1080)
            Camera.framerate = 30
        else: #framerate 60 res 1280x720
            Camera.resolution = (1280, 720)
            Camera.framerate = 60

        file = open("./status.txt", "w")
        file.write("-")
        file.close()

    @staticmethod
    def setCamera(speak):
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

        Camera.camera.resolution = (int(sett[0]), int(sett[1]))
        Camera.camera.framerate = int(sett[2])
        if (sett[3] != ""):
            Camera.camera.annotate_text_size = 50
            Camera.camera.annotate_foreground = picamera.Color("white")
            Camera.camera.annotate_text = sett[3]
        else:
            Camera.camera.annotate_text = ""
        Camera.camera.brightness = int(sett[4])
        Camera.camera.contrast = int(sett[5])
        Camera.camera.exposure_mode = sett[6]
        Camera.camera.awb_mode = sett[7]

        file = open("./status.txt", "w")
        file.write("-")
        file.close()

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