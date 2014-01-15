opcion = 0
saldo = 0.0
while opcion != 4:
  print "\n\n\n\n\n-----------Este es un cajero automatico------"
  print "1) consultar saldo "
  print "2) Adicionar saldo"
  print "3) retirar saldo"
  print "4) Salir\n\n\n"
  opcion = int(raw_input("Escoje una opcion : "))
  print "\n"
  if opcion == 1:
    print "_Ha elegido consultar saldo, su saldo es de : ", saldo
  if opcion == 2:
    adicion = float(raw_input("ha elegido adicionar saldo, cuanto desea adicionar : "))
    saldo += adicion
  if opcion == 3:
    retirar = float(raw_input("Ha elegido retirar saldo, cuanto desea retirar : "))
    saldo -= retirar

print "ha decidido salir del programa"
    
