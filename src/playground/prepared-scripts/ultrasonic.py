import RPi.GPIO as GPIO
import threading
import time

class UltrasonicSensor(object):

    SPEED_OF_SOUND_SEA_LEVEL_METER_PER_SECOND = 343

    def __init__(self, pinMode, triggerPin, echoPin, intervalSleep=0.05):
        self.pinMode = pinMode
        self.triggerPin = triggerPin
        self.echoPin = echoPin
        self._setup()

    def streamMeasurements(self):
        print('streamMeasurements()')
        threading.Thread(target=self._streamMeasurementsThread).start()

    def _streamMeasurementsThread(self):
        print('_streamMeasurementsThread()')
        try:
            while True:
                distance = ultraSonicSensor.measure()
                yield distance
                print('_streamMeasurementsThread(): distance: {}'.format(distance))
                time.sleep(self.intervalSleep)
        except KeyboardInterrupt:
            ultraSonicSensor.cleanUp()

    def measure(self):
        self._triggerMeasurement()
        pulse_start, pulse_end = self._measureResponse()
        distance = UltrasonicSensor._distance(pulse_start, pulse_end)
        return distance

    def cleanUp(self):
        GPIO.cleanup()

    def _setup(self):
        GPIO.setmode(self.pinMode)
        GPIO.setup(self.triggerPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)
        GPIO.output(self.triggerPin, False)
        # wait for sensor to settle
        time.sleep(2)

    def _triggerMeasurement(self):
        GPIO.output(self.triggerPin, True)
        time.sleep(0.00001)
        GPIO.output(self.triggerPin, False)

    def _measureResponse(self):
        while GPIO.input(self.echoPin) == 0:
            pulse_start = time.time()
        while GPIO.input(self.echoPin) == 1:
            pulse_end = time.time()
        return pulse_start, pulse_end

    @staticmethod
    def _distance(pulse_start, pulse_end):
        pulse_duration = pulse_end - pulse_start
        distance = (UltrasonicSensor.SPEED_OF_SOUND_SEA_LEVEL_METER_PER_SECOND * pulse_duration) / 2;
        return distance

TRIG = 23
ECHO = 24
MODE = GPIO.BCM
ultraSonicSensor = UltrasonicSensor(MODE, TRIG, ECHO)
ultraSonicSensor.streamMeasurements()
time.sleep(1000)
