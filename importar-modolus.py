from modulos import *

numero = 0

while(numero < 5):
  print "Es el menu la la calculadora"
  print "1) sumar"
  print "2) restar"
  print "3) dividir"
  print "4) multiplicar"
   
  numero = int(raw_input("Ingresa una opcion"))

  if (numero == 1):
    S1 = float(raw_input("Ingresa un numero : "))
    S2 = float(raw_input("Ingresa un numero : "))
    sumar(S1,S2)
  if (numero == 2):
     R1 = float(raw_input("Ingresa un numero : "))
     R2 = float(raw_input("Ingresa un numero : "))
     restar(R1,R2)
  if (numero == 3):
    D1 = float(raw_input("Ingresa un numero : "))
    D2 = float(raw_input("Ingresa un numero : "))
    dividir(D1,D2)
  if (numero == 4):
    M1 = float(raw_input("Ingresa un numero : "))
    M2 = float(raw_input("Ingresa un numero : "))
    multiplicar(M1,M2)

