import collections

from ImageManipulator import ImageManipulator
from TimeService import TimeService

GAUSSIAN_KERNEL = (21, 21)
DILATION_KERNEL = (11, 11)
DILATION_ITERATIONS = 10

class Detector(object):

    @staticmethod
    def detect(minHeight, minWidth, referenceImage, image):
        resized, grayed, blurred = Detector.generateReferenceImageItem(image)
        deltaImage = ImageManipulator.deltaImage(referenceImage, blurred)
        thresholdImage = ImageManipulator.threshold(deltaImage)
        dilatedThresholdImage = ImageManipulator.dilate(thresholdImage, DILATION_KERNEL, DILATION_ITERATIONS)

        contours = ImageManipulator.contours(dilatedThresholdImage)
        detectedRectangles = []
        for contour in contours:
            rectangle = ImageManipulator.getBoundingRectangle(contour)
            (x, y, width, height) = rectangle

            if width < height:
                continue
            if height < minHeight:
                continue
            if width < minWidth:
                continue

            detectedRectangles.append(rectangle)

        return detectedRectangles, resized, deltaImage, dilatedThresholdImage

    @staticmethod
    def generateReferenceImageItem(image):
        resized = ImageManipulator.resize(image)
        grayed = ImageManipulator.gray(resized)
        blurred = ImageManipulator.gaussianBlur(grayed, GAUSSIAN_KERNEL)
        return resized, grayed, blurred

    @staticmethod
    def generateReferenceImage(imageDeque):
        return ImageManipulator.getAverageImage(imageDeque)

    @staticmethod
    def generateReferenceImageDeque(image, size=10):
        imageList = []
        count = 0
        while count < size:
            imageList.append(image)
            count = count + 1
        return collections.deque(imageList, size)
