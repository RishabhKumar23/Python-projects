"""
Responsive screen
By: Rishabh Kumar
LinkedIn: https://www.linkedin.com/in/rishabh-kumar-7b0043217/
X: https://x.com/Rishabh24298026
"""
"""
Step-1: Open camera and set screen size
Step-2: 

"""

import cvzone
import cv2
import numpy as np
import pygetwindow as gw

cam = cv2.VideoCapture(0)   # to open camera

# Manual specification of screen resolution
screen_width = 1280
screen_height = 720

# Set the window name
window_name = "Snake Game"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)


while True:
    success, img = cam.read()
    if not success:
        break

     # Resize the image to fit the screen resolution
    img_resized = cv2.resize(img, (screen_width, screen_height))


    cv2.imshow(window_name, img_resized)  # Show the screen
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit loop when 'q' is pressed
        break