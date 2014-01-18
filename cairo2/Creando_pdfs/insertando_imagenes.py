#!/usr/bin/env python
from reportlab.pdfgen import canvas

pdf = canvas.Canvas("insertando_imagenes.pdf")

pdf.drawImage("Linux-Python.png" ,50,200,400,400)
pdf.showPage()
pdf.save()

