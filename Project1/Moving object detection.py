import cv2
import imutils

Camera = cv2.VideoCapture(0)

FirstFrame = None
Area = 500

while True:
    _,Img = Camera.read()
    Text = "Normal"
    Img = imutils.resize(Img,width=1000)

    GrayImg = cv2.cvtColor(Img,cv2.COLOR_BGR2GRAY)
    GaussianImg = cv2.GaussianBlur(GrayImg,(21,21),0)

    if FirstFrame is None:
        FirstFrame = GaussianImg
        continue

    ImgDiff = cv2.absdiff(FirstFrame,GaussianImg)

    ThreshImg = cv2.threshold(ImgDiff,25,255,cv2.THRESH_BINARY)[1]
    ThreshImg = cv2.dilate(ThreshImg,None,iterations=2)

    cont = cv2.findContours(ThreshImg.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont = imutils.grab_contours(cont)

    for c in cont:
        if cv2.contourArea(c) < Area:
            continue
        (x,y,w,h)=cv2.boundingRect(c)
        cv2.rectangle(Img,(x,y),(x+w,y+h),(0,0,255),2)
        Text = "Moving Object Detected"
    print(Text)
    cv2.putText(Img,Text,(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
    cv2.imshow("CameraFeed",Img)

    key=cv2.waitKey(10)
    print(key)

    if key == ord("q"):
        break

Camera.release()
cv2.destroyAllWindows()
            
