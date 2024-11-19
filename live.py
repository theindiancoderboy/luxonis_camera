import depthai as dai
import cv2

# Create a pipeline
pipeline = dai.Pipeline()

# Define a color camera
cam = pipeline.createColorCamera()
cam.setPreviewSize(640, 480)  # Set resolution
cam.setInterleaved(False)    # Non-interleaved output
cam.setFps(30)               # Frames per second

# Create an XLinkOut node to stream data to the host
xout = pipeline.createXLinkOut()
xout.setStreamName("video")
cam.preview.link(xout.input)

# Connect to the device
with dai.Device(pipeline) as device:
    # Get the output queue
    video_queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    print("Starting video stream. Press 'q' to quit.")
    
    while True:
        # Get a frame from the queue
        video_frame = video_queue.get()
        # Convert the frame to an OpenCV format
        frame = video_frame.getCvFrame()
        # Display the frame
        cv2.imshow("Live Camera Feed", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
