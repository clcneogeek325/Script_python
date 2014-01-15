lista = []

dato = raw_input("Ingresa el primer dato : ")

while dato != "":
  lista.append(int(dato))
  dato = raw_input("Ingresa el siguiente elemento : ")

print "Estos son los datos que acaba de introducir : ", lista

for recorrido in range(1,len(lista)):
  for posicion in range(len(lista) - recorrido):
    if lista[posicion] > lista[posicion + 1]:
      temp = lista[posicion]
      lista[posicion] = lista[posicion + 1]
      lista[posicion + 1] = temp
print "Estos son los datos que acaba de introducir ordenado de menor a mayor : ", lista

for recorrido in range(1,len(lista)):
  for posicion in range(len(lista) - recorrido):
    if lista[posicion] < lista[posicion + 1]:
      temp = lista[posicion]
      lista[posicion] = lista[posicion + 1]
      lista[posicion + 1] = temp
print "Estos son los datos que acaba de introducir ordenado de mayor a menor : ", lista

