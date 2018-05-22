import os
import shutil

class FileService(object):

    @staticmethod
    def ensureDirectoryExists(directory):
        if not FileService.doesDirectoryExist(directory):
            FileService.createDirectoy(directory)

    @staticmethod
    def doesDirectoryExist(directory):
        return os.path.exists(directory)

    @staticmethod
    def createDirectoy(directory):
        os.makedirs(directory)

    @staticmethod
    def removeDirectory(directory):
        shutil.rmtree(directory, ignore_errors=True)
