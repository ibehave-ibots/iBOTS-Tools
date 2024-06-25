# Adapted from https://cocalc.com/github/hackassin/learnopencv/blob/master/Optical-Flow-in-OpenCV/demo.py


## Software Installation:
# conda create -n of-demo python=3.12
# conda activate of-demo
# pip install opencv-python opencv-contrib-python numpy


## Running the Code on the terminal:
# python python optic_flow_demo_commented.py farneback
# python python optic_flow_demo_commented.py lucaskanade
# python python optic_flow_demo_commented.py lucaskanade_dense
# python python optic_flow_demo_commented.py rlof

### The Source Code:

# Importing necessary libraries for the program
# `cv2` is the OpenCV library, which provides functions for image and video processing
# `numpy` is a library for numerical operations, particularly on arrays
# `argparse` is a library for parsing command-line arguments

from argparse import ArgumentParser
import numpy as np
import cv2
import cv2.optflow

# This function calculates dense optical flow using a specified method
# `method` is the optical flow calculation method to be used
# `params` is a list of parameters specific to the chosen method
# `to_gray` is a boolean indicating whether to convert frames to grayscale
def dense_optical_flow(method, params=[], to_gray=False):
    # Capture video from the default camera (webcam)
    cap = cv2.VideoCapture(0)
    # Read the first frame from the video capture
    ret, old_frame = cap.read()

    # Initialize an HSV (Hue, Saturation, Value) image with the same shape as the first frame
    hsv = np.zeros_like(old_frame)
    # Set the saturation value to maximum (255) for all pixels
    hsv[..., 1] = 255

    # If grayscale conversion is required
    if to_gray:
        # Convert the first frame to grayscale
        old_frame = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    # Loop to continuously read frames from the video capture
    while True:
        # Read the next frame
        ret, new_frame = cap.read()
        frame_copy = new_frame  # Make a copy of the current frame
        if not ret:  # If reading the frame failed, exit the loop
            break

        # If grayscale conversion is required
        if to_gray:
            # Convert the current frame to grayscale
            new_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)

        # Calculate optical flow between the old frame and the new frame using the specified method and parameters
        flow = method(old_frame, new_frame, None, *params)

        # Convert the optical flow to polar coordinates (magnitude and angle)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        # Set the hue of the HSV image to the angle of the optical flow
        hsv[..., 0] = ang * 180 / np.pi / 2
        # Normalize the magnitude of the optical flow and set it to the value channel of the HSV image
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)

        # Convert the HSV image to BGR (Blue, Green, Red) format for display
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        # Display the original frame and the optical flow visualization
        cv2.imshow("frame", frame_copy)
        cv2.imshow("optical flow", bgr)
        k = cv2.waitKey(25) & 0xFF  # Wait for 25 milliseconds for a key press
        if k == 27:  # If the 'Esc' key is pressed, exit the loop
            break

        # Update the old frame to the current frame for the next iteration
        old_frame = new_frame

# This function calculates optical flow using the Lucas-Kanade method
def lucas_kanade_method():
    # Capture video from the default camera (webcam)
    cap = cv2.VideoCapture(0)
    # Parameters for Shi-Tomasi corner detection, used to find good features to track
    feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
    # Parameters for the Lucas-Kanade optical flow method
    lk_params = dict(
        winSize=(15, 15),
        maxLevel=2,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
    )
    # Generate random colors for drawing
    color = np.random.randint(0, 255, (100, 3))

    # Read the first frame and convert it to grayscale
    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    # Detect good features to track in the first frame
    p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
    # Create a mask image for drawing the optical flow tracks
    mask = np.zeros_like(old_frame)

    # Loop to continuously read frames from the video capture
    while True:
        ret, frame = cap.read()  # Read the next frame
        if not ret:  # If reading the frame failed, exit the loop
            break
        # Convert the current frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Calculate optical flow using the Lucas-Kanade method
        p1, st, err = cv2.calcOpticalFlowPyrLK(
            old_gray, frame_gray, p0, None, **lk_params
        )
        # Select the points with valid optical flow
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        # Draw the optical flow tracks
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel().astype(int)  # New point coordinates
            c, d = old.ravel().astype(int)  # Old point coordinates
            mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)  # Draw line
            frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)  # Draw circle
        # Combine the frame and the mask to show the tracks
        img = cv2.add(frame, mask)
        cv2.imshow("frame", img)  # Display the frame with the optical flow tracks
        k = cv2.waitKey(25) & 0xFF  # Wait for 25 milliseconds for a key press
        if k == 27:  # If the 'Esc' key is pressed, exit the loop
            break
        if k == ord("c"):  # If the 'c' key is pressed, clear the mask
            mask = np.zeros_like(old_frame)
        # Update the old frame and the points for the next iteration
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)

# Main function to parse command-line arguments and run the appropriate optical flow method
def main():
    # Create an argument parser to handle command-line arguments
    parser = ArgumentParser()
    parser.add_argument(
        "algorithm",
        choices=["farneback", "lucaskanade", "lucaskanade_dense", "rlof"],
        help="Optical flow algorithm to use",
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    # Check which algorithm is specified and call the corresponding function
    if args.algorithm == "lucaskanade":
        lucas_kanade_method()
    elif args.algorithm == "lucaskanade_dense":
        method = cv2.optflow.calcOpticalFlowSparseToDense
        dense_optical_flow(method, to_gray=True)
    elif args.algorithm == "farneback":
        method = cv2.calcOpticalFlowFarneback
        params = [0.5, 3, 15, 3, 5, 1.2, 0]  # Farneback's algorithm parameters
        dense_optical_flow(method, params, to_gray=True)
    elif args.algorithm == "rlof":
        method = cv2.optflow.calcOpticalFlowDenseRLOF
        dense_optical_flow(method)

# If this script is run as the main program, call the main function
if __name__ == "__main__":
    main()
