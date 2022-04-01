import cv2
import numpy as np

import handTrackingModel as htm
import time
import autopy
wScrn,hScrn=autopy.screen.size()
# hScrn+=100
# print(wScrn,hScrn)
frameR=150 #frame Reduction
camWidth,camHeight=640,480
ptime=0
pLocX,pLocY=0,0
cLocX,cLocY=0,0
smooth=7
cap=cv2.VideoCapture(0)
cap.set(3,camWidth) #the width
cap.set(4,camHeight)
detector=htm.handDetector(maxHands=1)


while True:
    #1 find hand landmarks
    success,img=cap.read()
    img=detector.findHands(img)
    lmList,bbox=detector.findPostion(img)
    # print(lmList)
    # 2  get the tip of index and middle fingers
    if (len(lmList)!=0):
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        # print(x1,x2,y1,y2)
        # 3  check which fingers are up
        fingers=detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (camWidth - frameR, camHeight - frameR), (0, 255, 255), 2)

        # 4  only index finger: Moving mode
        if fingers[1]==1 and fingers[2]==0:

         # 5  convert cordinates
         x3=np.interp(x1,(frameR, camWidth-frameR),(0,wScrn)) #from width cam to width screen
         y3 = np.interp(y1, (frameR, camHeight-frameR), (0,hScrn))

         # 6  Snoothen Values
         cLocX=pLocX+(x3-pLocX)/smooth
         cLocY=pLocY+(y3-pLocY)/smooth

         # 7  move mouse
         autopy.mouse.move(wScrn-cLocX,cLocY)
         cv2.circle(img,(x1,y1),15,(0,255,0),cv2.FILLED)
         pLocX,pLocY=cLocX,cLocY
        # 8  both index and middle fingers are up :Cicking mode
        if fingers[1]==1 and fingers[2]==1:
         # length,img,_=detector.findDistance(8,12,img)
         length,img,infoL=detector.findDistance(8,12,img)

         print(length)
         # 9  find find distance between fingers
         if length<25:
             cv2.circle(img, (infoL[4], infoL[5]), 10, (0, 255, 0), cv2.FILLED)
             autopy.mouse.click()

        # 10 Click mouse if didtance short
    # 11 frame Rate 
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime 
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    # 12 display
    cv2.imshow("Image",img)
    cv2.waitKey(1)
