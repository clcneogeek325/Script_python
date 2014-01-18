#!/usr/bin/env python
from reportlab.pdfgen import canvas

aux = canvas.Canvas("prueba.pdf")
aux.showPage()
aux.save()

print "el docuento se ha cread correctaente"
