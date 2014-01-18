#!/usr/bin/env python
from reportlab.pdfgen import canvas

pdf = canvas.Canvas("Insertando_texto.pdf")

pdf.drawString(50,200,"Que pedo este es u ejejmplo de como escribir en un pdf")
pdf.showPage()
pdf.save()

print "El fdd se ha genrado correctamente"
