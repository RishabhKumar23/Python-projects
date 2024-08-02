"""
Hand Tracing Module
By: Rishabh Kumar
LinkedIn: https://www.linkedin.com/in/rishabh-kumar-7b0043217/
X: https://x.com/Rishabh24298026
"""

import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
scale = 0
cx, cy = 500,500

detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img) # With draw
    #hands, img = detector.findHands(img, draw=False) # No draw
    #print(len(hands)) # To count the number of hands
    
    if hands:
        # Hand_1
        hand1 = hands[0]
        lmList1 = hand1["lmList"] # list of 21 landmarks points of a hand
        bbox1 = hand1["bbox"] # Bounding box info x, y, w, h
        centerPoint1 = hand1["center"] # Center of the hand cx, cy
        handType1 = hand1["type"] # Gives Hand type {Left hand or Right Hand}
        fingers1 = detector.fingersUp(hand1)
        #length, info, img = detector.findDistance(lmlist1[8], lmlist1[12], img) # With Draw
        #length, info, img = detector.findDistance(lmlist1[8], lmlist1[12]) # With No Draw
        
    # For more than 2 Hands
    if len(hands) == 2:
        hand2 = hands[1]
        lmList2 = hand2["lmList"] # list of 21 landmarks points of a hand
        bbox2 = hand2["bbox"] # Bounding box info x, y, w, h
        centerPoint2 = hand2["center"] # Center of the hand cx, cy
        handType2 = hand2["type"] # Gives Hand type {Left hand or Right Hand}
        fingers2 = detector.fingersUp(hand2)

        # print(handType1,handType2)
        # print(fingers1,fingers2)
        # length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
        length, info, img = detector.findDistance(centerPoint1, centerPoint2, img)  # with draw
        print(int(length))

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit loop when 'q' is pressed
        break
