import math
from sre_constants import SUCCESS
from unittest import result
import cv2
from cv2 import VideoCapture
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode = False, maxHands = 2, mComplexity=1, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mComplexity=mComplexity
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.mComplexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]


# from pip import main


    def findHands(self,img,draw=True):
     imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
     self.results=self.hands.process(imgRGB) ##process the frame
     # print(self.results.multi_hand_landmarks) #.multi_hand_landmarks

     if self.results.multi_hand_landmarks:
         for handLms in self.results.multi_hand_landmarks: #for select single hand
             if draw:
     
     
              self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS) #draw .. in single hande   #mpHands.HAND_CONNECTIONS ... for connections 
    
     return img
    
    def findPostion(self,img,handNo=0,draw=True):
        xlist=[]
        ylist=[]
        bbox=[]
        self.lmList=[]
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handNo]

            for id,lm  in enumerate(myhand.landmark): #for get the id landmark in screen position
                        # print(id,lm)
                        h,w,c=img.shape #get height width center
                        cx,cy=int(lm.x*w),int(lm.y*h) #landmark of x value *w   ## landmark of y value *h
                        xlist.append(cx)
                        ylist.append(cy)
                       # print(id,cx,cy) #the id of .  and pos  x et y 
                        self.lmList.append([id,cx,cy])
                        if draw:
                            cv2.circle(img,(cx,cy),8,(255,0,255),cv2.FILLED)  #cv2.FILLED for background
            xmin,xmax=min(xlist),max(xlist)
            ymin,ymax=min(ylist),max(ylist)
            bbox=xmin,ymin,xmax,ymax
            if draw:
                cv2.rectangle(img,(xmin-20,ymin-20),(xmax+20,ymax+20),(0,255,0),2)
        return self.lmList,bbox

    ########         fingers methode           ###################
    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)

        return fingers

    ####  ------------find distance methode ---------------------------

    def findDistance(self,p1,p2,img,draw=True,r=15,t=3):
        x1,y1=self.lmList[p1][1:]
        x2,y2=self.lmList[p2][1:]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),t)
            cv2.circle(img,(x1,y1),r,(0, 140, 109),cv2.FILLED)
            cv2.circle(img,(x2,y2),r,(0, 140, 109),cv2.FILLED)
            cv2.circle(img,(cx,cy),10,(0, 140, 255),cv2.FILLED)
        length=math.hypot(x2-x1,y2-y1)
        return  length,img,[x1,y1,x2,y2,cx,cy]
# ----------------------------------------------------
def main():
 pTime=0
 cTime=0
 cap=cv2.VideoCapture(0) #use 1st cam n0

 detector=handDetector()
 while True:
    sucess,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPostion(img)
    if len(lmList)!=0:
     #print(lmList[4])
     print('#')

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)  #3 the scale 3tickness

    cv2.imshow("Image",img)
    cv2.waitKey(1)
if __name__=="__main__":  
    main()