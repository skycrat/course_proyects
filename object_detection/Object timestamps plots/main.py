import cv2 as cv
import pandas as pd
import time
from datetime import datetime

#storing the background image
first_frame = None
status_list = [None, None]
times = []
df = pd.DataFrame(columns=["Start", "End"])

video = cv.VideoCapture(0)

while True: 
    check, frame = video.read()
    frame = cv.flip(frame, 1)
    
    #initial state without the presence of the object
    status = 0
    
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
    
    #filtering the countours, only keeping the area that are bigger than 1000 pixels (to detect bigger objects)
    for contour in cnts:
        if cv.contourArea(contour) < 1000:
            continue
        status = 1
        (x,y, w, h) = cv.boundingRect(contour)
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,255, 0), 3)
    status_list.append(status)        
    
    status_list = status_list[-2:]
    
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())
    
    # cv.imshow("Gray frame", gray)
    # cv.imshow("Delta frame", delta_frame)
    # cv.imshow("Threshhold Frame", thresh_frame)
    cv.imshow("Color Frame", frame)
    
    key = cv.waitKey(1)
    
    if key==ord('q'):
        break
    
    time.sleep(0.4)
    print(status, "\n")


for t in range(0, len(times), 2):
    time_dict = {"Start": times[t], 
                 "End": times[t+1] if len(times)% 2 == 0 else times[t+1::-2][0]}
    df.loc[len(df)] = time_dict
    
#print(status_list)

df.to_csv(".venv\Data Visualization with Bokeh\Object_timestamp.csv")

video.release()
cv.destroyAllWindows()
