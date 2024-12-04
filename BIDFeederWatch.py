#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    BIDFeederWatch.py:  Application to monitor bird feeder for birds.
    
    Version:            0.1.0 - Records video of movement. There is a threshold for the amount 
                        of movement necessary for the motion detection to kick in and start 
                        the recording. Records for 5 seconds at a time. Current version 
                        records with green boxes. Future version should record two versions of
                        the video, one with green boxes, one without. Currently after 3 
                        recordings, the program will end. This is to prevent recording too
                        many videos and flooding the storage.
"""

__author__      = "Sundeep Madhas"
__version__     = "0.1.0"

import cv2
import time
import datetime

# Constants
CAMERA_INDEX = 0  # use 1, if using external webcam on laptop with built-in camera
MAX_RECORDINGS = 3
RECORDING_TIME = 5  # in seconds 
GREATER_THAN_RECORDING_TIME = 10  # in seconds, this number should always be larger than RECORDING_TIME
MOTION_RESET_TIME = 5  # in seconds
MIN_CONTOUR_SIZE = 500
FPS = 20.0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Global Variables
firstFrame = None
firstFrameTime = 0.0

def main():
    """Starts the application. Gets the camera resource
    and puts the application into a state where it will wait for motion
    detection during the standby phase. Upon leaving the standby phase
    it will release the camera resource and destroy all windows. 
    """
    
    # Open camera. On laptop, this value is 1.
    # Due to the fact that the laptop has a built in camera.
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    # Turns camera on and is prepared to record when movement is detected.
    cameraStandby(cap)

    # Release camera resource, and destroy all windows used to view frames.          
    cap.release()
    cv2.destroyAllWindows()

def cameraStandby(cap: cv2.VideoCapture):    
    """A standby phase that checks for motion, and will start recording 
    if motion is detected. Motion detection resets reference frame 
    every 5 seconds. Recordings also currently last 5 seconds. 

    Args:
        cap (cv2.VideoCapture): Video capture resource.
    """
    # Local Variables
    # Set start time before the current time, so it doesn't start recording.
    startRecordingTime = time.time() - GREATER_THAN_RECORDING_TIME
    recording = False
    out = cv2.VideoWriter()
    recordingsMade = 0
    
    # Standby loop. 
    while(True):
        ret, frame = cap.read()
        if ret:
            #cv2.imshow('Bird Feeder Camera',frame)
            frame, motionDet = isMotionDetected(frame)
            cv2.imshow('Bird Feeder Camera', frame)
            
            # Record with outline. 
            if motionDet and not recording:
                # Define the codec and create a VideoWriter object to save the video named as date and time.
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                name = videoName() + '.mp4'
                out = cv2.VideoWriter(
                    name, 
                    fourcc, 
                    FPS, 
                    (FRAME_WIDTH, FRAME_HEIGHT),
                )
                startRecordingTime = time.time()
                recording = True                
                # Write the first frame of recording.
                out.write(frame)
            elif time.time() - startRecordingTime < RECORDING_TIME and recording:
                # out should already exist from earlier loop. 
                # While start time is with within 5 seconds of current time, keep recording. 
                out.write(frame)
            elif recording:
                # When no longer in time, turn off recording. 
                out.release()
                # When recording is done add to recording made counter. 
                # Adding to it before this will create a single frame video.
                recordingsMade = recordingsMade + 1
                recording = False
                    
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break
            
            if recordingsMade >= MAX_RECORDINGS:
                break
        else:
            break

def isMotionDetected(frame):
    """Uses cv2 Gaussian blue and frame difference to determine if there
    was movement between the frames. First frame is reset every 5 seconds.
    When motion is detected, green boxes are used to show the movement. 

    Args:
        frame : The current frame to be checked against an earlier reference
        frame. If the current frame is the first frame, then it is stored
        and the method returns with no motion detected. If time has exceeded limitation
        then the current frame is stored, and the method returns with no
        motion detected.

    Returns:
        frame: Either returns the current frame, or a modified frame with green boxes.
        motionDetected (bool): Returns a boolean value to indicate if motion was detected.
    """
    # Global Variables
    global firstFrame  # global because it must be stored beyond the scope of the method
    global firstFrameTime  # global because it must be stored beyond the scope of the method
    
    # Local Variable
    motionDetected = False 
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the frame to reduce noise and improve detection
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    # Initialize the first frame if it hasn't been set yet
    if firstFrame is None:
        firstFrame = gray
        firstFrameTime = time.time()
        motionDetected = False
        return frame, motionDetected
    
    # Reset the first frame after 5 seconds so not comparing to original. 
    if time.time() - firstFrameTime > MOTION_RESET_TIME:
        firstFrame = gray
        firstFrameTime = time.time()
        motionDetected = False
        return frame, motionDetected

    # Compute the absolute difference between the current frame and the first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    
    # Apply a threshold to the difference to create a binary image
    thresh = cv2.threshold(
        frameDelta, 
        25, 
        255, 
        cv2.THRESH_BINARY,
    )[1]

    # Dilate the threshold image to fill in holes
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    # Find contours in the threshold image to detect motion
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #cv2.imshow("gray", gray)
    #cv2.imshow("thresh", thresh)

    # Loop over the contours
    for contour in contours:
        # If the contour is too small, ignore it (this filters out small changes)
        if cv2.contourArea(contour) < MIN_CONTOUR_SIZE:
            continue

        # Get the bounding box for the contour and draw it on the frame
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(
            frame, 
            (x, y), 
            (x + w, y + h), 
            (0, 255, 0), 
            2
        )
        motionDetected = True        
        
    return frame, motionDetected


def videoName():
    """Determines the current date and time and creates a name for the 
    file.

    Returns:
        str: name - The name of the file to be used to store a recording.
    """
    cur = datetime.datetime.now()
    name = cur.strftime("%Y%m%d-%H%M%S")
    return name


if __name__ == "__main__":
    main()

