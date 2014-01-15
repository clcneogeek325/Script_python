cadena = raw_input("Ingresa una linea de texto")

lista_cadena = cadena.split()

print "La linea contiene " , len(lista_cadena) , " palabras \n"

for palabra in lista_cadena:
  print palabra
