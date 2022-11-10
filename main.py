from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy, QVBoxLayout,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit, QWidget)
import subprocess

async def active_socket():
    subprocess.call(['ping', 'localhost'])

def run_ffmpeg():
    ffmpeg = 'ffmpeg -i rtsp://admin:123456@192.168.1.120:554/stream1 -f mpegts -codec:v mpeg1video -s 640x480 -b:v 1000k -bf 0 http://localhost:8081/supersecret'
    return subprocess.Popen(ffmpeg.split(' '))

def run_websocket():
    open_socket = 'node /home/saeed/Desktop/camera/websocket-relay.js supersecret 8081 8082'
    return subprocess.Popen(open_socket.split(' '))
     

def run_camera():
    from collections import namedtuple
    from observer import ConcreteSubject, WebSocketObserver, FFMpegObserver 

    subject = ConcreteSubject()
    
    WebSocket = namedtuple('WebSocket','relay_js_path secret port_in port_out')
    web_socket = WebSocket(
                 relay_js_path= '/home/saeed/Desktop/camera/websocket-relay.js',
                 secret= 'supersecret', 
                 port_in= 8081,
                 port_out= 8082,)
    
    observer_ws = WebSocketObserver(web_socket)
    
    subject.attach(observer_ws)
    
    Camera = namedtuple('Camera', 'username password ip port size rate')
    camera = Camera('admin', '123456', '192.168.1.120', 554, '640x480', '1000k')
    
    Socket = namedtuple('Socket', 'host port secret')
    socket = Socket('http://localhost',
                     8081, 
                    'supersecret')
    
    observer_ffmpeg = FFMpegObserver(camera, socket)
    
    subject.attach(observer_ffmpeg)

    subject.run_camera()


    
class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("برای فعالسازی دوربین بر روی دکمه زیر کلیک کنید") 
 
        self.createTopRightGroupBox()  

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel) 
        
        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 1) 
        mainLayout.addWidget(self.topRightGroupBox, 1, 0)
        self.setLayout(mainLayout)

        self.setWindowTitle("فعالسازی دوربین")
        QApplication.setStyle(QStyleFactory.create('Fusion'))
 

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox() 

        togglePushButton = QPushButton("روشن کردن دوربین")
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(True)
        togglePushButton.clicked.connect(run_camera)

        nom_plan_label = QLabel()
        nom_plan_label.setText('دوربین روشن است')
        nom_plan_label.setObjectName('nom_plan_label')
        nom_plan_label.setStyleSheet('QLabel#nom_plan_label {color: green}')

        layout = QVBoxLayout() 
        layout.addWidget(togglePushButton) 
        layout.addWidget(nom_plan_label) 
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)
 
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())