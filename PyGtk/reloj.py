import datetime
import thread
import time

def imprimir():
    for x in range(10):
        print "*"
        time.sleep(1)
 
mensaje = datetime.datetime.now()
thread.start_new_thread(imprimir, (mensaje,))

       # x = raw_input("presiona para terminal el programa")

