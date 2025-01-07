import numpy as np
import imutils
import cv2
import time

model = "MobileNetSSD_deploy.caffemodel"
prototxt = "MobileNetSSD_deploy.prototxt.txt"
confidenceTresh = 0.2

Classes = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor","mobile"]
Color = np.random.uniform(0,255,size=(len(Classes),3))
print("Loading Model")
net = cv2.dnn.readNetFromCaffe(prototxt,model)
print("Model Loaded")
print("Starting CameraFeed")

vs=cv2.VideoCapture(0)
time.sleep(2.0)

while True:
    _,frame=vs.read()
    frame = imutils.resize(frame,width=1000)
    (h,w)=frame.shape[:2]
    imResizeBlob =cv2.resize(frame,(300,300))
    blob = cv2.dnn.blobFromImage(imResizeBlob,0.007843,(300,300),127.5)

    net.setInput(blob)
    Detection =net.forward()
    ##print(Detection)
    detShape = Detection.shape[2]

    for i in np.arange(0,detShape):
        Confidence = Detection[0,0,i,2]
        if Confidence>confidenceTresh:
            idx = int(Detection[0,0,i,1])
            print(Detection[0,0,i,1])
            box=Detection[0,0,i,3:7]*np.array([w,h,w,h])
            (startX,startY,endX,endY)=box.astype("int")

            label="{}:{:.2f}%".format(Classes[idx],Confidence*100)
            cv2.rectangle(frame,(startX,startY),(endX,endY),Color[idx],2)

            if startY-15>15:
                y=startY-15
            else:
                y=startY+15
            cv2.putText(frame,label,(startX,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,Color[idx],2)

    cv2.imshow("VIDEO",frame)
    key = cv2.waitKey(1)
    if key==27:
        break
vs.release()
cv2.destroyAllWindows()
