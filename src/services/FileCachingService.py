import os

from FileService import FileService

class FileCachingService(object):
    CACHE_DIR_REL_PATH = '/cache'

    @staticmethod
    def getCacheDirectory():
        currentWorkingDirectory = os.getcwd()
        cacheDirectory = currentWorkingDirectory + FileCachingService.CACHE_DIR_REL_PATH
        FileService.ensureDirectoryExists(cacheDirectory)
        return cacheDirectory

    @staticmethod
    def clear():
        cacheDirectory = FileCachingService.getCacheDirectory()
        FileService.removeDirectory(cacheDirectory)
        FileService.ensureDirectoryExists(cacheDirectory)
