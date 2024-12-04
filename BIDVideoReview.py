#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    BIDVideoReview.py:  Reviews videos to determine if video contains bird and identify the bird.
    
    Version:            0.1.0 - Current version should review a video in the folder and determine
                        if the video has a bird in it. If it finds a bird, it should try to 
                        identify the bird. Perhaps coping the video and adding metadata regarding
                        the bird in question. The information should also added as an entry in a
                        log containing all birds that have visited the feeder. 
"""

__author__      = "Sundeep Madhas"
__version__     = "0.1.0"

import os
from inference import get_model

dataSetDownloaded = True

def main():
    """Starts the analysis process. The application connects to roboflow and 
    """   
    print("Take in video, review frames, log if detected")

# Need to open video files
# Cycle through the frames and confirm if image contains birds


if __name__ == "__main__":
    main()
