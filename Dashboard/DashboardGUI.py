from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QTabWidget, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage  
from ultralytics import YOLO
#from data_fetcher import dataFetched


import sys # Access to command line arguments
import cv2
from streamlit import success #opencv for ca.3mera feed


model = YOLO("yolov8n.pt") # load base model


class MainWindow(QMainWindow):
    def __init__(self):
       super().__init__()

       self.setWindowTitle("MiR Dashboard") # window title
       self.setGeometry(100, 100, 800, 600) # window size and position
       layout = QGridLayout() # Uses grid layout formation

       central_widget=QWidget()
       self.setCentralWidget(central_widget)
       central_widget.setLayout(layout)

        #CAM FEED 1 WIDGET
       self.video_label = QLabel("Starting Camera") #camera widget section
       layout.addWidget(self.video_label, 0, 0) #top left

        #self.api_comm = DataFetcher(ip_address="???") #Gives IP address traight into variable for data fetcher
        #self.api_comm.dataFetched.connect(self.update_MiRdata_ui) # connect mailbox signal to function in UI
        #self.api_comm.start() # turn on communication

        # CONTROLS WIDGET 

       control_widget = QWidget() # new control widget
       control_layout = QGridLayout() # mini grid for control buttons#

       self.btn_return = QPushButton("RETURN HOME")
       self.btn_stop = QPushButton("STOP")

       control_layout.addWidget(self.btn_return, 0, 0) #attaching buttons to mini grid
       control_layout.addWidget(self.btn_stop, 0, 1)

       control_widget.setLayout(control_layout)
       layout.addWidget(control_widget, 1, 1) # attaching control widget to main grid

       self.btn_return.clicked.connect(self.return_home_command) # connecting widget to commands
       self.btn_stop.clicked.connect(self.stop_command)

       status_widget = QWidget() # new status widget
       status_layout = QVBoxLayout() # box layout
       status_title = QLabel("System Checks")

       self.status_console = QLabel("Current Status: IDLE")
       self.status_console.setAlignment(Qt.AlignmentFlag.AlignTop)

       status_layout.addWidget(status_title)
       status_layout.addWidget(self.status_console)
       status_widget.setLayout(status_layout)
       layout.addWidget(status_widget, 1 ,0)

    
       
       layout.addWidget(QLabel("CAmera and map toggle"), 0, 1)

       self.capture = cv2.VideoCapture(0) #start camera feed - 0 is default

       self.timer = QTimer(self) # update feed
       self.timer.timeout.connect(self.update_frame)
       self.timer.start(30) # new frame for 30fps refresh rate

    #def update_MiRdata_ui(self,data):

       #state = data.get("state_text", "UNKNOWN") # .get() stopping auto crashes if failed to retrive, just gives unknown or 0
       #battery = data.get("battery_percentage", 0.0)


    def update_frame(self):

        ret, frame = self.capture.read() # return 1 frame
        if ret:

            results = model(frame) # run model on each frame of cam feed 
            annotated_frame = results[0].plot() # bounding boxes

            self.camera_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB) # convert openCV to Qt
            h, w, ch, = self.camera_image.shape # reconverting raw data into qt image
            bytes_per_line = ch * w
            converted_image= QImage(self.camera_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

            scaled_pixmap = QPixmap.fromImage(converted_image).scaled(
                self.video_label.width(),
                self.video_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio
            )
            self.video_label.setPixmap(scaled_pixmap)


    def return_home_command(self):
        self.status_console.setText("Status: Returning Home Now!")
        print("SENT: RETURNING HOME NOW")
    def stop_command(self):
        print("SENT: STOPPING")
        self.status_console.setText("Status: IMMEDIATE STOP")


    


app = QApplication(sys.argv) #allows command line arguements for app

window=MainWindow() #uses a QtMainWindow as the main window
window.show()

app.exec() # start the event loop