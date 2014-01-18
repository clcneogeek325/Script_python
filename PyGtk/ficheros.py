fichero = open("prueba.py","r")

for linea in fichero:
    print linea.strip()

fichero.close()
