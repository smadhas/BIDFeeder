# BIDFeeder (Bird IDentify Feeder)

## Overview
This project will watch a bird feeder and record video when motion is detected. The recording will then be analyzed to determine if a bird fed from the feeder and if possible provide information regarding the bird. It will be deployed on a Raspberry Pi. Future versions may ID birds in real time.

## Resources Used:
- Python
  - CV2 (Open Computer Vision[OpenCV])
  - time
  - datetime
  - Roboflow
    - Bird Detection (https://universe.roboflow.com/guy-qibej/bird-detection-dyr4c)
    - Inference (https://inference.roboflow.com/)
- Raspberry Pi
- Docker
- Web Camera
- External Storage

## Contents:
### BIDFeederWatch.py
This code accesses the camera and keeps the camera on standby until motion is detected. Once motion is detected, it will record a 5 second video. After a set number of recordings the application will close so as to not fill the storage with video. 

## Getting Started
Currently BIDFeederWatch.py can be directly run using Python. If the camera doesn't seem to work, try setting the VideoCapture to 1. It may be an issue with camera order.

### Installation
Currently run using terminal. 

## Usage
Currently run BIDFeederWatch.py in terminal. 
`python3 BIDFeederWatch.py`
Future version should just run using Docker. 

## Roadmap
- [x] Write code to capture video when motion is detected.
- [ ] Write code to review video and check if it contains a bird.
- [ ] If bird is in video, find information about bird.
- [ ] Package into one application.
- [ ] Use Docker to make one that runs on scheduled tasks. 

