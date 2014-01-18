#!/usr/bin/env python
import time
import thread
import datetime

def imprimir_mensaje(mensaje):
    while True:
        print mensaje
        time.sleep(1)

def main():
    mensaje1 = datetime.datetime.now()
    mensaje2 = "hilo2"

    thread.start_new_thread(imprimir_mensaje, (mensaje1,))
    thread.start_new_thread(imprimir_mensaje, (mensaje2,))
    x = raw_input("Presiona enter...")
    print "La aplicasion ha finalizado"

main()
