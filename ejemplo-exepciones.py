numeroa = float(raw_input("Ingresa un numero : "))
numerob = float(raw_input("Ingresa otro numero : "))
# aki se inicializa la variable respuesta por si cae en  un error abajopor que
# solo estamos tratando el error de la operacion i no el de la la variable sin inicializar  
respuesta = 0

try:
 respuesta = numeroa / numerob
except:
 print "No se puede dividir etre cero o"

 print respuesta
