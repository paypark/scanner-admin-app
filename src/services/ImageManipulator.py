import numpy as np
import cv2
import imutils

class ImageManipulator(object):

    @staticmethod
    def resize(image, width=500):
        return imutils.resize(image, width=width)

    @staticmethod
    def gaussianBlur(image, kernel=(21, 21)):
        return cv2.GaussianBlur(image, kernel, 0)

    @staticmethod
    def gray(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def deltaImage(referenceGrayImage, testedGrayImage):
        """compute the absolut difference between the current frame and first frame"""
        return cv2.absdiff(referenceGrayImage, testedGrayImage)

    @staticmethod
    def threshold(deltaImage, dilateKernel = (11, 11)):
        """dilate the thresholded image to fill in holes, then find contours on thesholded image"""
        return cv2.threshold(deltaImage, 15, 255, cv2.THRESH_BINARY)[1]

    @staticmethod
    def dilate(image, kernel=(11, 11), iterations=10):
        """dilate the thresholded image to fill in holes, then find contours on thesholded image"""
        return cv2.dilate(image, kernel, iterations)

    @staticmethod
    def contours(thresholdImage):
        _, contours, _ = cv2.findContours(thresholdImage.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    @staticmethod
    def drawRectangleMutable(image, rectangle, color=(0, 255, 0)):
        (x, y, width, height) = rectangle
        cv2.rectangle(image, (x, y), (x + width, y + height), color, 2)

    @staticmethod
    def getBoundingRectangle(contour):
        return cv2.boundingRect(contour)

    @staticmethod
    def getAverageImage(imageDeque):
        for idx, image in enumerate(imageDeque):
            if idx == 0:
                sumImage = np.array(image, copy=True, dtype=np.uint16)
            else:
                sumImage = sumImage + image

        sumImage = sumImage / len(imageDeque)
        sumImage = np.rint(sumImage)
        sumImage = sumImage.astype(dtype=np.uint8)
        return sumImage
