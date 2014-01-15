matriz = []
print "Este es un programa para creae matricez"
filas = int(raw_input("Ingrese la catidad de filas : "))
columnas = int(raw_input("Ingrese la cantidad de columnas : "))

for i in range(filas):
  matriz.append([0]*columnas)

for f in range(filas):
  for c in range(columnas):
    matriz[f][c] = int(raw_input("Elemento en la posicion  %d,%d :" %(f,c)))

print matriz 
