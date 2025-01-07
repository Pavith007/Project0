from facial_emotion_recognition import EmotionRecognition
import cv2
er = EmotionRecognition(device='cpu')
Camera = cv2.VideoCapture(0)
while True:
    _,frame = Camera.read()
    frame=er.recognise_emotion(frame,return_type='BGR')
    cv2.imshow("CameraFeed",frame)
    key = cv2.waitKey(1)
    if key==27:
        break
Camera.release()
cv2.destroyAllWindows()
