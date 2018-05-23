import time

class TimeService(object):

    @staticmethod
    def getTimestamp():
        return int(time.time() * 1000)
