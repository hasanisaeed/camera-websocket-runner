from abc import ABC, abstractmethod
from subprocess import Popen

__all__ = ('Subject', 'ConcreteSubject')

class Subject(ABC):
        
    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass


class ConcreteSubject(Subject):
    
    _state: Popen = None

    _observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def run_camera(self):
        self.notify()
