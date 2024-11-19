import depthai as dai
import cv2
import zxingcpp
import numpy as np

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

    print("Starting video stream with QR detection. Press 'q' to quit.")
    
    while True:
        # Get a frame from the queue
        video_frame = video_queue.get()
        # Convert the frame to an OpenCV format
        frame = video_frame.getCvFrame()

        # Convert the frame to grayscale (required by ZXingCpp)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect QR codes using ZXingCpp
        results = zxingcpp.read_barcodes(gray_frame)

        # Draw rectangles around detected QR codes
        for result in results:
            # Extract the corner points
            points = result.position  # This is a list of (x, y) tuples
            
            # Convert to a numpy array
            points_np = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
            
            # Draw a polygon connecting the points
            cv2.polylines(frame, [points_np], isClosed=True, color=(0, 255, 0), thickness=2)
            
            # Display the decoded text near the QR code
            text = result.text
            cv2.putText(frame, text, (points[0].x, points[0].y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame with detected QR codes
        cv2.imshow("Live QR Detection", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
