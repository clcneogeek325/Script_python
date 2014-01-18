import os

salida = os.popen('ls *.jpg *.png').read()

f = open(".nombres.txt","w")
f.write(salida)
f.close()



