from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from subprocess import Popen

class Subject(ABC):
        
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class ConcreteSubject(Subject):
    
    _state: Popen = None

    _observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def run_camera(self):
        self.notify()


class Observer(ABC):

    @abstractmethod
    def update(self, subject: Subject):
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
        
    def update(self, subject: Subject):
        if subject._state is not None and subject._state.poll() is not None:
            subject._state.terminate()  
        subject._state = Popen(self.command.split(' '))
        
    def is_running(self, subject: Subject):
        if subject._state.poll() is not None:
            print(">> Websocket is stopped.")

from collections import namedtuple

class FFMpegObserver(Observer):
    
    def __init__(self, camera, socket):
        self.command = 'ffmpeg -i rtsp://%s:%s@%s:%d/stream1' \
            ' -f mpegts -codec:v mpeg1video -s %s -b:v %s -bf 0 %s:%d/%s' % (camera.username, camera.password, camera.ip, camera.port, camera.size, camera.rate, 
                                                                            socket.host, socket.port, socket.secret)

        
        
    def update(self, subject: Subject):
        if subject._state is not None and subject._state.poll() is not None:
            subject._state.terminate()  
        subject._state = Popen(self.command.split(' '))
        
    def is_running(self, subject: Subject):
        if subject._state.poll() is not None:
            print(">> Websocket is stopped.")


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
