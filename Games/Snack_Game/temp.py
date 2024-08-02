import cvzone
import cv2
import numpy as np
import pygetwindow as gw
from cvzone.HandTrackingModule import HandDetector
import math
import random

# Open the camera
cam = cv2.VideoCapture(0)

# Set the screen resolution
screen_width = 1280
screen_height = 720

# Set the window name
window_name = "Snake Game"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# Initialize hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

def ensure_alpha_channel(image):
    # Ensure the image has an alpha channel (4 channels).
    if image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    return image

class SnackGameClass:
    def __init__(self, pathFood):
        self.points = []  # List of all the points of the snake
        self.lengths = []  # Distance between each point
        self.currentLength = 0  # Total length of the snake
        self.allowedLength = 500  # Total allowed length of the snake
        self.previousHead = (0, 0)  # Previous head point

        # Load food image
        self.imageFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.imageFood = ensure_alpha_channel(self.imageFood)  # Ensure it has an alpha channel
        self.heightFood, self.widthFood, _ = self.imageFood.shape
        self.foodPoint = (0, 0)
        self.randomFoodLocation()

    def randomFoodLocation(self):
        self.foodPoint = (random.randint(100, screen_width - 100), random.randint(100, screen_height - 100))

    def update(self, imageMain, currentHead):
        previousX, previousY = self.previousHead
        currentX, currentY = currentHead

        self.points.append([currentX, currentY])
        distance = math.hypot(currentX - previousX, currentY - previousY)
        self.lengths.append(distance)
        self.currentLength += distance
        self.previousHead = currentX, currentY

        # Length reduction
        while self.currentLength > self.allowedLength:
            self.currentLength -= self.lengths[0]
            self.lengths.pop(0)
            self.points.pop(0)

        # Draw snake
        if self.points:
            for i in range(1, len(self.points)):
                cv2.line(imageMain, tuple(self.points[i - 1]), tuple(self.points[i]), (0, 255, 0), 20)
            cv2.circle(imageMain, tuple(self.points[-1]), 20, (0, 0, 255), cv2.FILLED)

        # Draw food
        randomX, randomY = self.foodPoint
        imageMain = cvzone.overlayPNG(imageMain, self.imageFood, (randomX - self.widthFood // 2, randomY - self.heightFood // 2))

        return imageMain

game = SnackGameClass("apple.png")

while True:
    success, img = cam.read()
    img = cv2.flip(img, 1)  # 1 for horizontal and 0 for vertical, -1 for both

    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)

    # Resize the image to fit the screen resolution
    img_resized = cv2.resize(img, (screen_width, screen_height))

    cv2.imshow(window_name, img_resized)  # Show the screen
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit loop when 'q' is pressed
        break

cam.release()
cv2.destroyAllWindows()
