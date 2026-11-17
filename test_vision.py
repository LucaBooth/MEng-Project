import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt") # load base model

cam = cv2.VideoCapture(0) # open webcam

print("Starting camera... Use 'q' on keyboard to exit.")

while cam.isOpened():
    success, frame = cam.read()
    if not success:
        print("Failed")
        break

    # run model on each frame of cam feed
    results = model(frame)

    # bounding boxes
    annotated_frame = results[0].plot()

    # window for camera vision
    cv2.imshow("Vision Prototype", annotated_frame)

    # stop key q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# reset at end
cam.release()
cv2.destroyAllWindows()