# -*- coding: utf-8 -*-

from abc import abstractmethod

"""
Estas clases definen el patron Observer para actualizar ciertos campos de la
GUI oportunamente.
Se aprovecha la herencia multiple de Python
"""

class Observer:

    def __init__(self, name, subject):
        self.name = name
        subject.register(self)

    @abstractmethod
    def notify(self, event):
        pass

class Subject:

     def __init__(self):
         self.observers = []
 
     def register(self, observer):
         self.observers.append(observer)
 
     def unregister(self, observer):
         self.observers.remove(observer)
 
     def notify_observers(self, event):
         for observer in self.observers:
             observer.notify(event)
