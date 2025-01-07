import cv2,numpy,os
size =4
Haar_File = 'haarcascade_frontalface_default.xml'
Datasets = 'datasets'

print('TRAINING.....')

(imgs,labels,names,id)=([],[],{},0)
for(subdirs,dirs,files)in os.walk(Datasets):
    for subdir in dirs:
        names[id]=subdir
        subjectpath = os.path.join(Datasets,subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/'+ filename
            label=id
            imgs.append(cv2.imread(path,0))
            labels.append(int(label))
            print(label)

        id+=1
(width,height)=(130,100)
(imgs,labels)=   [numpy.array(lis) for lis in [imgs,labels]]
model = cv2.face.FisherFaceRecognizer_create()
model.train(imgs,labels)

face_casade = cv2.CascadeClassifier(Haar_File)
Camera = cv2.VideoCapture(0)

cnts= 0
while True:
    (_,img)=Camera.read()
    Gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    Faces= face_casade.detectMultiScale(Gray,1.3,5)

    for(x,y,w,h) in Faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,160),2)
        face=Gray[y:y+h,x:x+w]
        face_resize = cv2.resize(face,(width,height))
        prediction = model.predict(face_resize)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),3)
        if prediction[1]<800:
            cv2.putText(img,'%s - %.0f'%(names[prediction[0]],prediction[1]),(x-10,y-10),cv2.FONT_HERSHEY_COMPLEX,1,(51,255,255))
            print (names[prediction[0]])
            cnts=0
        else:
            cnts+=1
            cv2.putText(img,'Unknown',(x-10,y-10),cv2.FONT_HERSHEY_PLAIN,1,(255,0,255))
            if (cnts>100):
                print("Unknown Person")
                cv2.imwrite("Input.jpg",img)
                cnts=0
    cv2.imshow('OpenCV',img)
    key=cv2.waitKey(10)
    if key==27:
        break
Camera.release()
cv2.destroyAllWindows()
        
