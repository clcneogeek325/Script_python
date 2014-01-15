def duplicar(lista):# esta funcion es la que se encarga de duplicar los valores de la lista
  for i in range(len(lista)):
    lista[i] = lista[i]*2
  return

numeros = [4,8,20,7,3]

duplicar(numeros)# es aqui donde se duplican los valores de la lista

print numeros

def ordenar(lista):
  for recorrido in range(1,len(lista)):
    for posicion in range(len(lista) - recorrido):
      if lista[posicion] > lista[posicion + 1]:
        lista[posicion], lista[posicion+1] = lista[posicion+1], lista[posicion]

desordenados = [34,65,7,9,54,34,8]

ordenar(desordenados)

print desordenados
