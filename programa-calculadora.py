opcion = 0

while opcion < 5:
 print "1) suma"
 print "2) resta"
 print "3) Multiplicacion"
 print "4) Divicion"
 print "5) Salir"

 opcion = int(raw_input("\n Elige un opcion: "))

 if opcion == 1 :
  print "Has elegido la suma"
  Snumero1 = float(raw_input("Ingresa el primer numero para la suma:"))
  Snumero2 = float(raw_input("Ingresa el segundo numero para la suma :"))
  Sresultado = Snumero1 + Snumero2
  print "El resultado de la suma es :" , Sresultado

 if opcion == 2 :
  print "Has elegido la resta"
  Rnumero1 = float(raw_input("Ingresa el pirmer numero para la resta :"))
  Rnumero2 = float(raw_input("Ingresa el segundo numero para la resta :"))
  Rresultado = Rnumero1 - Rnumero2
  print "El resultado de la resta es : " , Rresultado
  print Rresultado

 if opcion == 3:
  print "Has elegido una multiplicacion "
  Mnumero1 = float(raw_input("Ingresa el pirmer numero para la multiplicacion :"))
  Mnumero2 = float(raw_input("Ingresa el segundo numero para la multiplicacion :"))
  Mresultado = Mnumero1 * Mnumero2
  print "El resultado de la Multiplicacion es : " , Mresultado
  print Mresultado
 if opcion == 4:
  print "Has elegido una multiplicacion " 
  Dnumero1 = float(raw_input("Ingresa el primer numero para la Divicion :"))
  Dnumero2 = float(raw_input("Ingresa el segundo numero para la Divicion :"))
  Dresultado = Dnumero1 / Dnumero2
  print "El resultado de la Divicion es :" , Dresultado
  
