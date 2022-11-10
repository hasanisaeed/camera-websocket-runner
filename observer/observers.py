from abc import ABC, abstractmethod
from subprocess import Popen

__all__ = ('Observer', 
           'WebSocketObserver',
           'FFMpegObserver')

class Observer(ABC):

    @abstractmethod
    def update(self, subject):
        pass
    
    @abstractmethod
    def is_running(self):
        pass



class WebSocketObserver(Observer):
    
    def __init__(self,
                 web_socket):
        
        self.command = 'node %s %s %d %d' % (web_socket.relay_js_path, 
                                             web_socket.secret, 
                                             web_socket.port_in,
                                             web_socket.port_out)
        
    def update(self, subject):
        if subject._state is not None and subject._state.poll() is not None:
            subject._state.terminate()  
        subject._state = Popen(self.command.split(' '))
        
    def is_running(self, subject):
        if subject._state.poll() is not None:
            print(">> Websocket is stopped.")
            

class FFMpegObserver(Observer):
    
    def __init__(self, camera, socket):
        self.command = 'ffmpeg -i rtsp://%s:%s@%s:%d/stream1' \
            ' -f mpegts -codec:v mpeg1video -s %s -b:v %s -bf 0 %s:%d/%s' % (camera.username, camera.password, camera.ip, camera.port, camera.size, camera.rate, 
                                                                            socket.host, socket.port, socket.secret)
       
    def update(self, subject):
        if subject._state is not None and subject._state.poll() is not None:
            subject._state.terminate()  
        subject._state = Popen(self.command.split(' '))
        
    def is_running(self, subject):
        if subject._state.poll() is not None:
            print(">> Websocket is stopped.")
