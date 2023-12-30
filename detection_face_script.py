import cv2 as cv


face_cascade = cv.CascadeClassifier(".venv\ImageProcessing\Detecting_faces\haarcascade_frontalface_default.xml")

img = cv.imread(".venv\ImageProcessing\Detecting_faces\\several_faces.jpeg")
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray_img, 
                                      scaleFactor= 1.5,
                                      minNeighbors=3,
                                      )

for x, y, w, h in faces:
    img = cv.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 3)
    

resized = cv.resize(img,(int(img.shape[1]*2), int(img.shape[0]*2)))

cv.imshow("Ryan_Gray", resized)
cv.waitKey(0)
cv.destroyAllWindows()
