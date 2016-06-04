#!/usr/bin/env python
# -*- coding: utf-8 -*-

class miclase():
    def __init__(self):
        self.version = '1.0'
     
    def suma(self,a, b):
        return a+b
          
    def resta(self,a,b):
        return a-b


obj = miclase()

# accediendo a los metodos de python de modo regular
print obj.suma(4,5)
print obj.resta(5,2)

# accediendo a los metodos de python por medio de la reflexion
print getattr(obj,'suma')(3,4)
print getattr(obj,'resta')(7,2)
