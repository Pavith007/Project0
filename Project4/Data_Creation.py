import cv2,os
Haar_File='haarcascade_frontalface_default.xml'
Datasets='datasets'
subdata='Sathish'

Path=os.path.join(Datasets,subdata)
if not os.path.isdir(Path):
    os.mkdir(Path)

(Width,Height)=(130,100)
Face_cascade=cv2.CascadeClassifier(Haar_File)
Camera = cv2.VideoCapture(0)

Count = 1
while Count<51:
    print(Count)
    (_,img)=Camera.read()
    Gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    Faces = Face_cascade.detectMultiScale(Gray,1.3,4)

    for(x,y,w,h)in Faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        Face=Gray[y:y+h,x:x+w]
        Face_Resize=cv2.resize(Face,(Width,Height))
        cv2.imwrite('%s/%s.png'%(Path,Count),Face_Resize)
    Count+=1
    cv2.imshow('opencv',img)
    key=cv2.waitKey(10)
    if key == 27:
        break
Camera.release()
cv2.destroyAllWindows()
