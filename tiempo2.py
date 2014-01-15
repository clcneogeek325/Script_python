#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import time

cadena = "ejemplo mundo"

class hilo(threading.Thread):
	"""docstring para hilo"""
	def __init__(self, cadena):
		super(hilo, self).__init__()
		self.cadena = cadena 
		
	def run(self):
		for x in range(len(cadena)):
    		    print cadena[x],
    	            time.sleep(0.01)


obj = hilo(cadena)
obj.start()
obj.join()
