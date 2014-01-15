#/usr/bin/env python
# -*-encoding: utf-8 -*-
print "Este programa deduce si podeas votar ene estas elecciones \n \f programa desarrollado por NeoGeek"
edad = int(raw_input("dame tu edad"))
votar = "si" if edad > 17 else "no"
print "tu %s  podras votar en estas elecciones de este año" %votar
