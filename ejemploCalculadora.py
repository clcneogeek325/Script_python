
print "---------**********************--------"
print "           Bienvenido a linux"
print "Este programa es una calculadora estas son las opciones :"
print "1) Suma"
print "2) Resta"
print "3) Divicion"
print "4) Multiplicacion"
print "5) Salir"

numero = int(raw_input("Elija alguna de las opcione: "))

if numero == 1:
    print "Ha elegido hacer una suma"
    Sum1 = float(raw_input("Ingrese el primer numero: ")) 
    Sum2 = float(raw_input("Ingrese el segundo numero: "))
    ResSuma = Sum1 + Sum2
    print ResSuma

if numero == 2:
    print "Ha elegudo hacer una resta"
    Res1 = float(raw_input("Ingrese el primer numero: "))
    Res2 = float(raw_input("Ingrese el segundo numero: "))
    ResRes = Res1 - Res2
    print ResRes

if numero == 3:
    print "Ha elegido hacer una multiplicacion "
    Mul1 = float(raw_input("Ingrese el primer numero: "))
    Mul2 = float(raw_input("Ingrese el segundo numero: "))
    ResMul = Mul1 * Mul2
    print ResMul

if numero == 4:
    print "Ha elegido hacer una Divicion "
    Div1 = float(raw_input("Ingrese el primer numero: "))
    Div2 = float(raw_input("Ingrese el segundo numero: "))
    ResDiv = Div1 / Div2
    print ResDiv
