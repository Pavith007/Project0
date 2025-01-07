import cv2

Algo = "haarcascade_frontalface_default.xml"

Haar_cascade=cv2.CascadeClassifier(Algo)
Camera = cv2.VideoCapture(0)

while True:
    _,img = Camera.read()
    Grayimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    Face = Haar_cascade.detectMultiScale(Grayimg,1.3,4)
    for (x,y,w,h) in Face:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
    cv2.imshow("Face Detection",img)

    key = cv2.waitKey(10)
    if key == 27:
        break
Camera.release()
cv2.destroyAllWindows()
