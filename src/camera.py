import time
import uuid
import os
from base_camera import BaseCamera
from FilenameService import FilenameService

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    imgs = [open(os.path.join(__location__, f + '.jpg'), 'rb').read() for f in ['1', '2', '3']]
    isRecording = False

    def __init__(self, cameraSettings):
        super(Camera, self).__init__()
        Camera.shutter_speed = cameraSettings.getShutterSpeed()

    @staticmethod
    def updateSettings(cameraSettings):
        Camera.shutter_speed = cameraSettings.getShutterSpeed()
        Camera.framerate = cameraSettings.getFrameRate()
        Camera.shutter_speed = cameraSettings.getShutterSpeed()
        Camera.iso = cameraSettings.getIso()
        Camera.resolution = (cameraSettings.getWidth(), cameraSettings.getHeight())
        print("updateSettings()")

    @staticmethod
    def frames():
        while True:
            time.sleep(1)
            yield Camera.imgs[int(time.time()) % 3]

    @staticmethod
    def snapshot():
        return str(uuid.uuid4()) + ".jpg"

    @staticmethod
    def startRecording():
        filename = FilenameService.generateTimeBasedFilename('.h264')
        print("filename: " + filename)
        if Camera.isRecording == False:
            Camera.isRecording = True

    @staticmethod
    def stopRecording():
        if Camera.isRecording == True:
            Camera.isRecording = False

    @staticmethod
    def isCameraRecording():
        return Camera.isRecording
