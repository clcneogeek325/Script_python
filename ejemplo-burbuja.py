lista = [5,4,7,8,1,3,2]

for recorrido in range(1,len(lista)):
  for posicion in range(len(lista) - recorrido):
    if lista[posicion] > lista[posicion + 1]:
      temp = lista[posicion]
      lista[posicion] = lista[posicion + 1]
      lista[posicion + 1] = temp

print lista
