import cv2 
import numpy as np
import sys
import math
print("Write down the path to file")
ans = str(input())
img = cv2.imread(ans)
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
lower1 = np.array([0, 50, 50])
upper1 = np.array([8, 255, 255])
lower2 = np.array([165, 50, 50])
upper2 = np.array([179, 255, 255])
mask1 = cv2.inRange(img2, lower1, upper1)
mask2 = cv2.inRange(img2, lower2, upper2)
red = mask1 + mask2
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
lower = np.array([0, 0, 150])
upper = np.array([255, 100, 255])
white = cv2.inRange(img2, lower, upper)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
_, trash = cv2.threshold(white, 100, 255, cv2.THRESH_BINARY)
rcontours, rhierarchy = cv2.findContours(trash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
circles = []
triangles = []
rectangles = []
others = []
shape = "Strange"
i=0
for c in rcontours:
    con = cv2.arcLength(c, True)
    cont = cv2.approxPolyDP(c, con/10000, True)
    smallcont = cv2.approxPolyDP(c, con/5, True)
    (x,y),radius = cv2.minEnclosingCircle(cont)
    x,y,w,h = cv2.boundingRect(cont)
    center = (int(x),int(y))
    r = int(radius)
    if r>0 and abs(r-cv2.contourArea(cont)/(math.pi*r))<=r/20 and cv2.contourArea(cont)>20:
        circles.append(cont)
        if rhierarchy[0][i][3]==-1:
            shape = "Circle"
    elif r>0 and w+h-cv2.arcLength(cont,True)/2<(w+h)/20 and len(smallcont)<5 and w*h-cv2.contourArea(cont)<500 and cv2.contourArea(cont)>20:
        rectangles.append(cont)
        if rhierarchy[0][i][3]==-1:
            shape = "Rectangle"
    elif r>0 and len(smallcont)==3 and cv2.contourArea(cont)>20:
        triangles.append(cont)
        if rhierarchy[0][i][3]==-1:
            shape = "Triangle"
    elif r>0 and cv2.contourArea(cont)>20:
        others.append(cont)
        if rhierarchy[0][i][3]==-1:
            shape = "Strange"
    i+=1
print(shape)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
if shape=="Strange":
    cv2.drawContours(img, others, -1, (0,255,0), 1)
    print("Stop")
elif shape=="Circle":
    cv2.drawContours(img, circles, -1, (0,255,0), 1)
    if len(rhierarchy[0])>2:
        print("Entry is prohibited")
    else:
        if white[np.shape(img)[0]//2][np.shape(img)[1]//2]==0 and white[np.shape(img)[0]//5*2+5][np.shape(img)[1]//5*3+20]==255:
            print("Driving right")
        elif white[np.shape(img)[0]//2][np.shape(img)[1]//2]==0 and white[np.shape(img)[0]//5*2+5][np.shape(img)[1]//5+20]==255:
            print("Driving left")
        else:
            print("Driving straight")
elif shape=="Rectangle":
    cv2.drawContours(img, rectangles, -1, (0,255,0), 1)
    if np.sum(red)<500000:
        if len(triangles)>0:
            if len(rhierarchy[0])>4:
                print("Pedestrian crossing")
            else:
                print("Bump")
        else:
            print(white[np.shape(img)[0]//3*2][np.shape(img)[1]//2])
            if white[np.shape(img)[0]//3*2][np.shape(img)[1]//2]==255:
                print("Deadlock forward")
            elif red[np.shape(img)[0]//2][np.shape(img)[1]//3*2]==255:
                print("Deadlock to the right")
            else:
                print("Deadlock to the left")
    else:
        print("Hazard chevron")
elif shape=="Triangle":
    cv2.drawContours(img, others, -1, (0,255,0), 1)
    if len(circles)==1:
        print("Hazards")
    elif len(others)>5:
        print("Children")
    elif white[np.shape(img)[0]//5*2][np.shape(img)[1]//2]==0:
        print(1)
    else:
        print(len(rhierarchy[0]))
        if len(rhierarchy[0])==4:
            if white[106][110]==0:
                print("Bump")
            elif white[np.shape(img)[0]//5*4][np.shape(img)[1]//2-5]==0:
                print("Dangerous turn right")
            elif white[np.shape(img)[0]//5*4][np.shape(img)[1]//2+5]==0:
                print("Dangerous turn left")
            else:
                print("Dangerous turns")
        else:
            print("Narrowing of the road")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
cv2.imshow("white", trash)
cv2.imshow("img",img)
cv2.waitKey(0)
