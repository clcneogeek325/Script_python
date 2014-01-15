# cuando queremos imprimir caracteres que usarmos para saltos de linea i escapes solo ponemos a lado isquierdo antes ina diagonal inversa

cadena = len("") #no tiene longitud
print cadena

cadena1 = len(" ")# no es lo mismo tener un espacio en blanco
print cadena1
          #0123456789 empieza desde el cero como los arreglos
cadena2 = "hola como estas"
print cadena2[3]  # se imprimer la posicion del caracter 

cadena3 = "swarsheneger"
for caracter in cadena3:  # se puede imprimir una cadena con un for-in 
  print caracter

cadena4 = "the rasmus"
for i in range(len(cadena4)):# recorre las posiciones de la cadena
 print cadena4[i]

cadena5 = "Gnome-look"
print cadena5[1:5] # otra forma de mostrar subcadenas

cadena6 = "ubuntu"
print cadena6.find("b")# el .find nos devuelve la posicion del caracter en la cadena
#si hai varios caracteres iguales muestra la posicion del primero que encuetren 

