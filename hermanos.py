#/usr/bin/env python
# -*-encoding: utf-8 -*_
print "****Este programa registra el nombre de tus hermanos, te los guarda en un arreglo***** \n"
agradecimiento = "software creado por neogeek"
agradecimiento = agradecimiento.title()
cuantos_hermanos = int(raw_input("ingresa el numero de tus hermanos"))
hermano = raw_input("Ingresa el nombre de tu hermano: ")
contenedor = []
contenedor.append(hermano)
comparame = 1
while cuantos_hermanos > comparame:
    hermano = raw_input("Ingresa el sisguiente hermano ")
    contenedor.append(hermano)
    comparame += 1

print "El numero de hermanos es %d sus nombres son %s" %(cuantos_hermanos,contenedor)
print "\n ", agradecimiento

