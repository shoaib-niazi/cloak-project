import cv2
import numpy as np
import time

# opening the webcam
cap=cv2.VideoCapture(0)

if not cap.isOpened():
    print("sorry we cannot access the camera")

# giving time to camera to adjust
time.sleep(2)

# first we need to capture the background without a cloak
print("Getting the background picture without cloak. so plz stand still")
for _ in range(60):
    ret, bg=cap.read()
    if ret:
        bg=cv2.flip(bg,1)
print("The background has beeb captured sucessfully")

# starting the reading of frames in real time
while cap.isOpened():
    ret, frame=cap.read()
    if not ret:
        break
    # mirror view
    frame=cv2.flip(frame,1)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #defining the red color ranges
    lower_red1=np.array([0,100,50])
    upper_red1=np.array([10,255,255])
    lower_red2=np.array([170,100,50])
    upper_red2=np.array([180,255,255])
    # creating a mask for the red ones
    mask1=cv2.inRange(hsv,lower_red1,upper_red1)
    mask2=cv2.inRange(hsv,lower_red2,upper_red2)
    mask=mask1+mask2
    # now we will refine a mask for that red areas
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3), np.uint8))
    mask=cv2.dilate(mask,np.ones((3,3),np.uint8),iterations=1)
    mask_inv=cv2.bitwise_not(mask)

    # replacing the red cloak region with background
    cloak_area=cv2.bitwise_and(bg,bg,mask=mask)
    non_cloak_area=cv2.bitwise_and(frame,frame,mask=mask_inv)
    final=cv2.addWeighted(cloak_area,1,non_cloak_area,1,0)
    # now showing the results
    cv2.imshow("invisibilty cloak",final)
    cv2.imshow("cloak mask",mask)

    # adding the keybaord controls
    key=cv2.waitKey(1) & 0xFF
    # if Esc than quit so
    if key==27:
        break
    # if want to recapture the bg
    elif key==ord('b'):
        print("recapturing the background")
        for _ in range(60):
              ret,bg=cap.read()
              if ret:
                  bg=cv2.flip(bg,1)
        print("The Background has been captured")

cap.release()
cv2.destroyAllWindows()
