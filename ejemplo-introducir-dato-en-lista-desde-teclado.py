#!/usr/bin/python

lista = []

elemento = raw_input("Ingrese un elemento : ")

while elemento != "":
 lista.append(int(elemento))
 elemento = raw_input("Ingrese el siguiente elemento")

print "Los elementos ingresado son : ",lista
