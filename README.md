# Hand Tracking

## Overview
This project demonstrates hand tracking and gesture recognition using Python, OpenCV, and MediaPipe. It includes three main functionalities:

- Basic hand tracking visualization
- Mouse control using hand gestures
- Volume control using hand gestures

## Dependencies
- OpenCV
- MediaPipe
- PyAutoGUI
- pyvolume
- pynput

```bash
pip install opencv-python mediapipe pyautogui pyvolume pynput
```

## Usage
### 1. Basic Hand Tracking:
```bash
python HandTracking.py
```

### 2. Mouse Control:
```bash
python MouseHandControl.py
```

### 3. Volume Control:
```bash
python VolumeHandControl.py
```

## Usage
### 1. HandTracking.py
- Real-time hand detection and landmark tracking
- Visualizes hand landmarks and connections
- Provides coordinates of each hand landmark

### 2. MouseHandControl.py
- Controls mouse cursor movement using thumb and index finger
- Left click: Pinch thumb and index finger together briefly
- Left click and hold: Pinch thumb and index finger for >0.5 seconds
- Right click: Pinch thumb and middle finger together

### 3. VolumeHandControl.py
- Controls system volume using two hands
- Pinch thumb and index finger on both hands
- Adjust volume by changing distance between the two pinched hands