#!/usr/bin/env python3

import cv2
import depthai as dai
import time
import os
import threading
import requests
import base64
from .database import insert_name
# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutRgb = pipeline.create(dai.node.XLinkOut)

xoutRgb.setStreamName("rgb")
sessionid="945a88c7-28b9-476e-b7b2-17812972a31c"
url = f"http://160.238.95.111/stream/upload_frame/{sessionid}/"

# Properties
# camRgb.setPreviewSize(300, 300)
camRgb.setPreviewSize(3840,2160)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
# Linking
camRgb.preview.link(xoutRgb.input)

devices = dai.Device.getAllAvailableDevices()

# Connect to device and start pipeline
def cam1():
    with dai.Device(pipeline,devices[0]) as device:

        print('Connected cameras:', device.getConnectedCameraFeatures())
        # Print out usb speed
        # Bootloader version
        if device.getBootloaderVersion() is not None:
            print('Bootloader version:', device.getBootloaderVersion())
        # Device name
        print('Device name:', device.getDeviceName(), ' Product name:', device.getProductName())

        # Output queue will be used to get the rgb frames from the output defined above
        qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

        while True:
            inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived

            # _, buffer = cv2.imencode('.jpg', inRgb.getCvFrame())
            # image_data = base64.b64encode(buffer).decode('utf-8')
            # response = requests.post(url, data={'image_data': image_data})
            # Retrieve 'bgr' (opencv format) frame
            # cv2.imshow("rgb", inRgb.getCvFrame())
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            try:
                cv2.imwrite(f"img/frame_{timestamp}cam1.jpg", inRgb.getCvFrame())
                insert_name(f"img/frame_{timestamp}cam1.jpg")
            except Exception:
                pass

def cam2():
    with dai.Device(pipeline,devices[1]) as device:

        print('Connected cameras:', device.getConnectedCameraFeatures())
        # Print out usb speed
        # Bootloader version
        if device.getBootloaderVersion() is not None:
            print('Bootloader version:', device.getBootloaderVersion())
        # Device name
        print('Device name:', device.getDeviceName(), ' Product name:', device.getProductName())

        # Output queue will be used to get the rgb frames from the output defined above
        qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

        while True:
            inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived

            # _, buffer = cv2.imencode('.jpg', inRgb.getCvFrame())
            # image_data = base64.b64encode(buffer).decode('utf-8')
            # response = requests.post(url, data={'image_data': image_data})
            # Retrieve 'bgr' (opencv format) frame
            # cv2.imshow("rgb", inRgb.getCvFrame())
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            try:
                cv2.imwrite(f"img/frame_{timestamp}cam2.jpg", inRgb.getCvFrame())
                insert_name(f"img/frame_{timestamp}cam2.jpg")
            except Exception:
                pass
            # if cv2.waitKey(1  ) == ord('q'):
            #     break