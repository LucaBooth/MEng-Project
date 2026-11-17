import cv2
import numpy as np

image = cv2.imread("test_frame_lab_pic.jpg")
cv2.imshow(image)
cv2.setMouseCallback

pxl = np.float32([
    [2673, 2320], # top left
    [4485, 2419], #top right
    [2430, 3036], # bl
    [4726, 3251], #br
])

dst = np.float32([
    [0,0]
    [450, 0]
    [0, 300]
    [450, 300]
])

image_transform = cv2.perspectiveTransform(pxl,dst)

def pxl_to_real(points) # used to list x,y pixel coords to x,y coords in cm
    points
    

