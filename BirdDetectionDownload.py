#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    BirdDetectionDownload.py:  Using the developer's API downloads the bird-detection folder from Roboflow.
    
    Version:            0.1.0 - Downloads the Bird-detection folder from Roboflow. 
"""

__author__      = "Sundeep Madhas"
__version__     = "0.1.0"

import os
from dotenv import load_dotenv, dotenv_values
from roboflow import Roboflow

load_dotenv()
    
def main():
    rf = Roboflow(api_key=os.getenv("API_KEY"))

    project = rf.workspace("guy-qibej").project("bird-detection-dyr4c")
    version = project.version(14141)
    dataset = version.download("folder")  
    
if __name__ == "__main__":
    main()