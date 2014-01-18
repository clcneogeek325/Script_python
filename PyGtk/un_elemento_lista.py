import os

salida = os.popen('ls *.png *.jpg').read()
nombres = salida.split()

for nombre in nombres:
    print nombre
