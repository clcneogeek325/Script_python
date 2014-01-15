dato = 0

while dato < 3:

 print "\n\n\n\n---------programa para mostrar numeros impares--------\n"
 print "1) Numeros impares"
 print "2) Numeros pares"
 print "3) Salir \n"

 dato = int(raw_input("Escoja un opcion : "))
 print "\n\n"

 if dato == 1:
  p = 1
  while p <= 10:
   print p
   p += 2 
 
 if dato == 2:
  f = 2
  while f <= 10:
   print f
   f += 2
