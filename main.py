from PyQt6.QtWidgets import (QApplication, QCheckBox, QDialog, QGridLayout, QGroupBox,
                             QLabel, QLineEdit, QPushButton, QStyleFactory)
    
class WidgetGallery(QDialog):
    def run_camera(self): 
        from collections import namedtuple
        from manager import ConcreteSubject, WebSocketObserver, FFMpegObserver 
        self.ws_socket = {
                 'relay_js_path': self.txtRelayJsPath.text(),
                 'secret': self.txtSecret.text(), 
                 'port_in': int(self.txtPortIn.text()),
                 'port_out': int(self.txtPortOut.text()),
        }
        
        self.camera = {
            'ffmpeg': self.txtFFMpegPath.text(),
            'username': self.txtUsername.text(),
             'password': self.txtPassword.text(),
             'ip': self.txtIP.text(),
             'port': int(self.txtPort.text()),
             'size': self.txtSize.text(),
             'rate': self.txtRate.text(),
        }
        
        self.socket = {
            'host': self.txtHost.text(),
            'port': int(self.txtPortIn.text()),
            'secret': self.txtSecret.text()
        }
        
        subject = ConcreteSubject()
        
        WebSocket = namedtuple('WebSocket','relay_js_path secret port_in port_out')
        web_socket = WebSocket(**self.ws_socket)
        
        self.observer_ws = WebSocketObserver(web_socket)
        
        subject.attach(self.observer_ws)
        
        Camera = namedtuple('Camera', 'ffmpeg username password ip port size rate')
        camera = Camera(**self.camera)
        
        Socket = namedtuple('Socket', 'host port secret')
        socket = Socket(**self.socket)
        
        self.observer_ffmpeg = FFMpegObserver(camera, socket)
        
        subject.attach(self.observer_ffmpeg)

        subject.run_camera()

        

    
    def check_status(self):
        try:
            message = '%s - %s' % (self.observer_ffmpeg.is_running()[1], self.observer_ws.is_running()[1])
            color = self.observer_ffmpeg.is_running()[0]
            self.lblActive.setText(message)
            self.lblActive.setStyleSheet(color)
        except AttributeError:
            pass
    
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.txtFFMpegPath = QLineEdit('ffmpeg')
        self.txtUsername = QLineEdit('admin')
        self.txtPassword = QLineEdit('123456')
        self.txtIP = QLineEdit('192.168.1.120')
        self.txtPort = QLineEdit('554')
        self.txtSize = QLineEdit('640x480')
        self.txtRate = QLineEdit('1000k')
        self.txtHost = QLineEdit('http://localhost')
        
        self.txtRelayJsPath = QLineEdit('/home/saeed/Desktop/camera/websocket-relay.js')
        self.txtPortIn = QLineEdit('8081')
        self.txtPortOut = QLineEdit('8082')
        self.txtSecret = QLineEdit('supersecret')

        self.camera_settings()  
        self.websocket_settings()  

        self.topLayout = QGridLayout()
        btnRunCamera = QPushButton('روشن | ON', self)
        
        btnCameraStatus = QPushButton('بررسی وضعیت | Status', self)

        self.topLayout.addWidget(btnRunCamera, 0, 2) 
        self.topLayout.addWidget(btnCameraStatus, 0, 1) 
          
        self.lblActive = QLabel('دوربین خاموش است') 
        self.lblActive.setStyleSheet('color: red')
        
        self.topLayout.addWidget(self.lblActive, 0, 0)
        
        chkDisableSettings = QCheckBox("&Disable Settings")
        chkDisableSettings.toggled.connect(self.topLeftGroupBox.setDisabled)
        chkDisableSettings.toggled.connect(self.topRightGroupBox.setDisabled)
        chkDisableSettings.setChecked(True)
        
        mainLayout = QGridLayout()
        mainLayout.addWidget(chkDisableSettings)
        mainLayout.addLayout(self.topLayout, 0, 1) 
        mainLayout.addWidget(self.topLeftGroupBox, 1, 1)
        mainLayout.addWidget(self.topRightGroupBox, 1, 0)
        
        mainLayout.addWidget(QLabel('carvann.ir | سامانه کاروان'), 2, 0)
        
        self.setLayout(mainLayout)

        self.setWindowTitle("Camera | دوربین")
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        
        btnRunCamera.clicked.connect(self.run_camera)
        btnCameraStatus.clicked.connect(self.check_status)
        

    def camera_settings(self):
        self.topLeftGroupBox = QGroupBox("Camera") 
        self.txtPassword.setEchoMode(QLineEdit.EchoMode.Password) 
        
        layout = QGridLayout()
        layout.addWidget(QLabel('Username: '), 0, 0) 
        layout.addWidget(self.txtUsername, 0, 1)  
        
        layout.addWidget(QLabel('Password: ')) 
        layout.addWidget(self.txtPassword)  
         
        layout.addWidget(QLabel('IP: ')) 
        layout.addWidget(self.txtIP)  
         
        layout.addWidget(QLabel('Port: ')) 
        layout.addWidget(self.txtPort)  
         
        layout.addWidget(QLabel('Size: ')) 
        layout.addWidget(self.txtSize)  
         
        layout.addWidget(QLabel('Rate: ')) 
        layout.addWidget(self.txtRate) 
        
        self.topLeftGroupBox.setLayout(layout)        
        
        
    def websocket_settings(self):
        self.topRightGroupBox = QGroupBox("Socket")
         
        self.txtSecret.setEchoMode(QLineEdit.EchoMode.Password)
        
        layout = QGridLayout()
        layout.addWidget(QLabel('Host: '), 0, 0) 
        layout.addWidget(self.txtHost, 0, 1)  
        
        layout.addWidget(QLabel('Port(in): ')) 
        layout.addWidget(self.txtPortIn)  
         
        layout.addWidget(QLabel('Port(out): ')) 
        layout.addWidget(self.txtPortOut)  
         
        layout.addWidget(QLabel('Secret: ')) 
        layout.addWidget(self.txtSecret)
         
        layout.addWidget(QLabel('Relay Path: ')) 
        layout.addWidget(self.txtRelayJsPath)
        
        self.topRightGroupBox.setLayout(layout)        
         

 
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())