import cv2
from cvzone import HandTrackingModule as htm
cap=cv2.VideoCapture(0)
cap.set(3,1200)
cap.set(4,720)
img1=cv2.imread('infinity.jpg')
img1 = cv2.resize(img1,(0,0),fx = 0.1, fy = 0.1)
i1,i2=200,200
#print(img1.shape)
ih,iw,_= img1.shape
handDetection=htm.HandDetector(detectionCon=0.8)
start_distance=None
scale=0
_,img=cap.read()
mainH,mainW,_=img.shape
cx,cy=mainW//2,mainH//2
while True:
    _,img=cap.read()
    #mainH,mainW=img.shape
    no_hands,img=handDetection.findHands(img)
    #img[i1:i1+ih,i2:i2+iw]=img1
    if len(no_hands)==2:
        hand1=no_hands[0]
        hand2=no_hands[1]
        l1=handDetection.fingersUp(hand1)
        l2=handDetection.fingersUp(hand2)
        if l1==[1,1,0,0,0] and l2==[1,1,0,0,0]:
            index_fingure_1=hand1['lmList'][8]
            index_fingure_2=hand2['lmList'][8]
            x1,y1=index_fingure_1[0],index_fingure_1[1]
            x2,y2=index_fingure_2[0],index_fingure_2[1]
            if start_distance is None:
                #length,info,img=handDetection.findDistance((x1,y1),(x2,y2),img)
                length,info,img=handDetection.findDistance(no_hands[0]["center"],no_hands[1]["center"],img)

                start_distance=length
            #length,info,img=handDetection.findDistance((x1,y1),(x2,y2),img)
            length,info,img=handDetection.findDistance(no_hands[0]["center"],no_hands[1]["center"],img)
            scale=length-start_distance
            cx,cy=info[4:]
    else:
        start_distance=None
    try:
        newH,newW=(ih+scale//2)*2,(iw+scale//2)*2
        #print(newH,newW)
        img1=cv2.resize(img1,(int(newW),int(newH)))
        #print(cy-newH//2)
        #print(cy+newH//2)
        img[int(cy-newH//2):int(cy+newH//2), int(cx-newW//2):int(cx+newW//2)]=img1
        cv2.imshow("main frame",img)
    except:
        pass
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break