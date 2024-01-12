import cv2 as cv 
import time

#storing the background image
first_frame = None

video = cv.VideoCapture(0)

while True: 
    check, frame = video.read()
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray,(21,21), 0) #to smooth fade, because that removes noise and increases accuracy
    
    if first_frame is None:
        first_frame = gray
        continue
    
    delta_frame = cv.absdiff(first_frame, gray)
    
    #applying the threshold method
    #note: this returns a tuple with 2 values,
    #if your are using other threshold then you need to access the first value
    #of the tuple, but if you are using the binary one, you only need the second value(the actual frame)
    thresh_frame = cv.threshold(delta_frame, 30, 255, cv.THRESH_BINARY)[1]
    
    #creating countours of the white object
    #we want to remove those black holes froms those big white areas
    #that's call delitation
    
    #iterations -> how many times you want to go through the image
    # to remove those holes
    thresh_frame = cv.dilate(thresh_frame, None, iterations= 2)
    
    #finding the countours
    (cnts,_) = cv.findContours(thresh_frame.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    #filtering the countours, only keeping the area that are bigger than 1000 pixels
    for contour in cnts:
        if cv.contourArea(contour) < 1000:
            continue
        
        (x,y, w, h) = cv.boundingRect(contour)
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,255, 0), 3)
            
    
    
    cv.imshow("Gray frame", gray)
    cv.imshow("Delta frame", delta_frame)
    cv.imshow("Threshhold Frame", thresh_frame)
    cv.imshow("Color Frame", frame)
    
    key = cv.waitKey(1)
    
    if key==ord('q'):
        break
    
    time.sleep(0.3)


video.release()
cv.destroyAllWindows()
