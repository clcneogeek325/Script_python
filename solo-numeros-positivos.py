def lee_numero_positivo():
  numero = int(raw_input("Ingresa un numero : "))
  while numero < 0:
    print "El numero debe ser positivo "
    numero = int(raw_input("Ingresa un numero : "))
  return numero


numero1 = lee_numero_positivo()
numero2 = lee_numero_positivo()
numero3 = lee_numero_positivo()
numero4 = lee_numero_positivo() 
numero5 = lee_numero_positivo()

print numero1,numero2,numero3,numero4,numero5

