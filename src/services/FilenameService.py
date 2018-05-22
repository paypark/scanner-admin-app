import datetime

class FilenameService(object):

    @staticmethod
    def generateTimeBasedFilename(fileType):
        return FilenameService.getTimeString() + '.' + fileType

    @staticmethod
    def getTimeString():
        utcDatetime = datetime.datetime.utcnow()
        return utcDatetime.strftime("%Y-%m-%d-%H-%M-%S-%f")

