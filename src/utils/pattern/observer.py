# -*- coding: utf-8 -*-

from abc import ABCMeta

"""
Estas clases definen el patron Observer para actualizar ciertos campos de la
GUI oportunamente.
Se aprovecha la herencia multiple de Python
"""

class Listener:

    def __init__(self, name, subject):
        self.name = name
        subject.register(self)

    @abstractmethod
    def notify(self, event):
        pass

class Subject:

     def __init__(self):
         self.listeners = []
 
     def register(self, listener):
         self.listeners.append(listener)
 
     def unregister(self, listener):
         self.listeners.remove(listener)
 
     def notify_listeners(self, event):
         for listener in self.listeners:
             listener.notify(event)
