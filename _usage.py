from collections import namedtuple
from observer import ConcreteSubject, WebSocketObserver, FFMpegObserver

if __name__ == "__main__": 

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
