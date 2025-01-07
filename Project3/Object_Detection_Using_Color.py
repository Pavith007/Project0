import imutils
import cv2
Lower = (255,255,255)
Upper = (255,255,255)

Camera = cv2.VideoCapture(0)

while True:
    (_,img) = Camera.read()
    img = imutils.resize(img,width=1000)
    blurred= cv2.GaussianBlur(img,(11,11),0)
    HSV =cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)
    Mask = cv2.inRange(HSV,Lower,Upper)
    Mask = cv2.erode(Mask,None,iterations=2)
    Mask = cv2.dilate(Mask,None,iterations=2)

    Conts = cv2.findContours(Mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

    Center =None
    if len(Conts)>0:
        c= max(Conts,key=cv2.contourArea)
        ((x,y,radius))=cv2.minEnclosingCircle(c)
        M=cv2.moments(c)
        Center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        if radius > 0:
            cv2.circle(img,(int(x),int(y)),int(radius),(0,255,255),2)
            cv2.circle(img,Center,5,(0,0,255),-1)
            if radius >250:
                print("STOP")
            else:
                if(Center[0]<150):
                    print("Right")
                elif(Center[0]< 450):
                    print("Left")
                elif(Center[0]< 250):
                    print("Front")
                else:
                    print("STOP")
    cv2.imshow("Frame",img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
Camera.release()
cv2.destroyAllWindows()
