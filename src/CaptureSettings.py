class CaptureSettings(object):

    def __init__(self):
        self.shutterSpeed = 0
        self.frameRate = 30
        self.iso = 0
        self.width = 640
        self.height = 480

    def getShutterSpeed(self):
        return self.shutterSpeed

    def setShutterSpeed(self, shutterSpeed):
        self.shutterSpeed = shutterSpeed
        return self

    def getFrameRate(self):
        return self.frameRate

    def setFrameRate(self, frameRate):
        self.frameRate = frameRate
        return self

    def getIso(self):
        return self.iso

    def setIso(self, iso):
        self.iso = iso
        return self

    def getWidth(self):
        return self.width

    def setWidth(self, width):
        self.width = width
        return self

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height
        return self

    def set(self, newSettings):
        if 'frameRate' in newSettings.keys():
            self.frameRate = newSettings['frameRate']
        if 'shutterSpeed' in newSettings.keys():
            self.shutterSpeed = newSettings['shutterSpeed']
        if 'iso' in newSettings.keys():
            self.iso = newSettings['iso']
        if 'height' in newSettings.keys():
            self.height = newSettings['height']
        if 'width' in newSettings.keys():
            self.width = newSettings['width']

    def toJSON(self):
        return dict(
            frameRate=self.frameRate,
            shutterSpeed=self.shutterSpeed,
            iso=self.iso,
            height=self.height,
            width=self.width
        )
