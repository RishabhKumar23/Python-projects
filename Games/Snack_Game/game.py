"""
Snack Game
By: Rishabh Kumar
LinkedIn: https://www.linkedin.com/in/rishabh-kumar-7b0043217/
X: https://x.com/Rishabh24298026
"""
"""
Step-1: Open camera and set screen size
Step-2: Detect hand and fix flip
Step-3: Add snake food
Step-4: Add score
Step-5: Add game over text 

"""

import cvzone
import cv2
import numpy as np
import pygetwindow as gw
from cvzone.HandTrackingModule import HandDetector
import math
import random

cam = cv2.VideoCapture(0)   # to open camera
cam.set(3, 1280)     # to set width 
cam.set(4, 720)      # to set height

# Manual specification of screen resolution
# screen_width = 1280
# screen_height = 720

# Set the window name
window_name = "Snake Game"
# cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# for hand detection
detector = HandDetector(detectionCon=0.8, maxHands=1)

class SnackGameClass:
    def __init__(self, pathFood):
        self.points = [] # list of all the points af the snack
        self.lengths = [] # distance between each points
        self.currentLength = 0 # total length of the snack
        self.allowedLength = 500 # total allowed length of the snack
        self.previousHead = 0, 0 # previous head point

        #imgFood, hFood, wFood
        self.imageFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.heightFood, self.widthFood, _ = self.imageFood.shape
        self.foodPoint = 0, 0
        self.score = 0
        self.randomFoodLocation()
        self.gameOver = False

    
    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imageMain, currentHead): # imgMain
        
        if self.gameOver:
            cvzone.putTextRect(imageMain, "Game Over", [300, 400], scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imageMain, f'Your Score: {self.score}', [300, 550], scale=7, thickness=5, offset=20)

        else:
                
            #px, py = self.previousHead
            previousX, previousY = self.previousHead
            #cx, cy = self.currentHead
            currentX, currentY = currentHead

            self.points.append([currentX,currentY])
            distance = math.hypot(currentX - previousX, currentY - previousY)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = currentX, currentY

            #Length Reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break
            
            # check if snack ate the food or not
            randomX, randomY = self.foodPoint
            if randomX - self.widthFood // 2 < currentX < randomX + self.widthFood // 2 and\
                randomY - self.heightFood // 2 < currentY < randomY + self.heightFood // 2:
                #print("ate")
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
                print(self.score)

            # draw snake
            if self.points:
                for i,point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imageMain, self.points[i - 1], self.points[i], (0, 0, 255), 20) # green
                cv2.circle(imageMain, self.points[-1], 20, (255, 0, 0), cv2.FILLED) # red

            # draw food
            # randomX, randomY = self.foodPoint
            # if randomX < currentX < randomX + self.widthFood and randomY < currentY + self.heightFood:
                # print("ate")
            imageMain = cvzone.overlayPNG(imageMain, self.imageFood,(randomX - self.widthFood // 2, randomY - self.heightFood // 2))
            cvzone.putTextRect(imageMain, f'Score: {self.score}', [50, 80], scale=3, thickness=3, offset=10, colorR=(0, 255, 0))

            # check for the collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imageMain, [pts], False, (0, 255, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (currentX, currentY), True)
            # print(minDist)

            # game over
            # if -1 < minDist < 1:
            #     print("Hit")
            #     self.gameOver = True
            #     self.points = [] # list of all the points af the snack
            #     self.lengths = [] # distance between each points
            #     self.currentLength = 0 # total length of the snack
            #     self.allowedLength = 500 # total allowed length of the snack
            #     self.previousHead = 0, 0 # previous head point
            #     self.score = 0
            #     self.randomFoodLocation()

        return imageMain

game = SnackGameClass("image.png")


while True:
    success, img = cam.read()
    img = cv2.flip(img, 1) # 1 for horizontal adn 0 for vertical -1 for both

    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        #cv2.circle(img, pointIndex, 20, (255, 0, 0), cv2.FILLED)
        img = game.update(img, pointIndex)

    # # Resize the image to fit the screen resolution
    # img_resized = cv2.resize(img, (screen_width, screen_height))

    cv2.imshow(window_name, img)  # Show the screen
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):  # Exit loop when 'q' is pressed
        break
    if key == ord('r'):
        game.gameOver = False
