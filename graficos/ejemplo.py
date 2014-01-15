import os
  
archivos = os.popen('ls').read()

lista_archivos = archivos.split()

for x in lista_archivos:
   print x
