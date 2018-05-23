import sys

sys.path.append('./src/services')

#!/usr/bin/env python
from importlib import import_module
import os
import json
from flask import Flask, render_template, Response, jsonify, send_from_directory, send_file, request
import random
import io
import time
import numpy as np
import cv2

from EnvironmentService import EnvironmentService
from USBStorageService import USBStorageService
from CommandLineService import CommandLineService
from Detector import Detector
from ImageManipulator import ImageManipulator
from TimeService import TimeService

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

from CaptureSettings import CaptureSettings
captureSettings = CaptureSettings()
captureSettings.setShutterSpeed(5000)
captureSettings.setFrameRate(60)
captureSettings.setIso(1)
captureSettings.setHeight(480)
captureSettings.setWidth(640)

### detection
REFERENCE_FRAME_AVERAGE_FRAME_COUNT = 50
REFERENCE_FRAME_UPDATE_INTERVAL_MS = 500
DRAW_DETECTED_REGIONS = True
MIN_HEIGHT = 60
MIN_WIDTH = 100

referenceFrame = None
referenceFrameDeque = None
referenceFrameLastUpdate = TimeService.getTimestamp()

lastIdentifiedFrame = None
secondLastIdentifiedFrame = None
thirdLastIdentifiedFrame = None

app = Flask(__name__, static_folder='static')

@app.route('/<path:filename>')
def send_static_file(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/python-reload')
def pythonReload():
    processId = os.getpid()
    CommandLineService.run_command('git pull && pip3 install -r requirements.txt && kill -9 {}'.format(processId))

@app.route('/hello')
def hello():
    obj = {}
    obj['message'] = "hola foobar"
    return jsonify(obj)

@app.route('/increase')
def increase():
    obj = {}
    obj['message'] = "increased"
    return jsonify(obj)

@app.route('/decrease')
def decrease():
    obj = {}
    obj['message'] = "decreased"
    return jsonify(obj)

@app.route('/settings', methods = ['GET', 'POST'])
def settings():
    if request.method == 'GET':
        return jsonify(captureSettings.toJSON())

    if request.method == 'POST':
        jsonObject = request.get_json()
        captureSettings.set(jsonObject)
        # Camera.updateSettings(captureSettings)
        return json.dumps({ 'success': True }, 200, { 'Content-Type': 'applicaton/json' })

@app.route('/recording/start', methods = ['GET'])
def recordingStart():
    try:
        Camera.startRecording()
        return json.dumps({ 'message': 'recording started' }, 200, { 'Content-Type': 'applicaton/json' })
    except:
        return json.dumps({ 'message': 'recording starting failed' }, 500, { 'Content-Type': 'applicaton/json' })

@app.route('/recording/stop', methods = ['GET'])
def recordingStop():
    Camera.stopRecording()
    return json.dumps({ 'message': 'recording stopped' }, 200, { 'Content-Type': 'applicaton/json' })

@app.route('/usb/mount', methods = ['GET'])
def usbMount():
    if Camera.isCameraRecording() == True:
        return json.dumps({ 'message': 'can not mount while camera is recording' }, 400, { 'Content-Type': 'applicaton/json' })

    statusCode, message = USBStorageService.mount()
    return json.dumps({ 'message': message }, statusCode, { 'Content-Type': 'applicaton/json' })

@app.route('/usb/unmount', methods = ['GET'])
def usbUnmount():
    if Camera.isCameraRecording() == True:
        return json.dumps({ 'message': 'stop recording before unmounting' }, 400, { 'Content-Type': 'applicaton/json' })

    try:
        USBStorageService.unmount()
        return json.dumps({ 'message': 'unmounting successful' }, 200, { 'Content-Type': 'applicaton/json' })
    except:
        print('ERROR')
        return json.dumps({ 'message': 'unmounting error' }, 500, { 'Content-Type': 'applicaton/json' })


@app.route('/status', methods = ['GET'])
def status():
    body = dict(
        isRecording=Camera.isCameraRecording(),
        isUsbConnected=USBStorageService.isUSBStorageMounted()
    )
    return json.dumps(body, 200, { 'Content-Type': 'applicaton/json' })

def gen(camera):
    """Video streaming generator function"""
    referenceFrame = None
    while True:
        frame = camera.get_frame()

        data = np.fromstring(frame, dtype=np.uint8)
        image = cv2.imdecode(data, 1)

        if referenceFrame is None:
            _, _, referenceFrame = Detector.generateReferenceImageItem(image)
            referenceFrameDeque = Detector.generateReferenceImageDeque(referenceFrame, REFERENCE_FRAME_AVERAGE_FRAME_COUNT)
            referenceFrameLastUpdate = TimeService.getTimestamp()

        if TimeService.getTimestamp() > referenceFrameLastUpdate + REFERENCE_FRAME_UPDATE_INTERVAL_MS:
            _, _, referenceFrameItem = Detector.generateReferenceImageItem(image)
            referenceFrameDeque.append(referenceFrameItem)
            referenceFrame = Detector.generateReferenceImage(referenceFrameDeque)
            referenceFrameLastUpdate = TimeService.getTimestamp()

        detectedRegionRectangles, processedImage, deltaImage, thresholdImage = Detector.detect(MIN_HEIGHT, MIN_WIDTH, referenceFrame, image)

        if DRAW_DETECTED_REGIONS and len(detectedRegionRectangles):
            for rectangle in detectedRegionRectangles:
                ImageManipulator.drawRectangleMutable(processedImage, rectangle)

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode(".jpeg", processedImage)[1].tostring() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        gen(Camera(captureSettings)),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/image')
def image():
    """Get current image"""
    camera = Camera(captureSettings)
    image_binary = camera.get_frame()
    image = io.BytesIO(image_binary)
    filename = '{}.jpg'.format(time.time())
    return send_file(image, mimetype='image/jpeg', cache_timeout=-1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
