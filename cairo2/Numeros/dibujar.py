#!/usr/bin/env python
import gobject
import gtk, pygtk, cairo
from math import pi

pygtk.require('2.0')

class dibujar:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(300,320)
	self.ventana.set_title("Ejemplo de dibujo")

	self.areaDibujo = gtk.DrawingArea()
	self.areaDibujo.set_size_request(250,250)
	self.boton1 = gtk.Button("1")
	self.boton2 = gtk.Button("2")
	self.boton3 = gtk.Button("3")
	self.boton4 = gtk.Button("4")
	self.boton5 = gtk.Button("5")
	self.boton6 = gtk.Button("6")
	self.boton7 = gtk.Button("7")
	self.boton8 = gtk.Button("8")
	self.boton9 = gtk.Button("9")
	self.boton0 = gtk.Button("0")


	self.boton1.connect("clicked", self.dibujando1)
	self.boton2.connect("clicked", self.dibujando2)
	self.boton3.connect("clicked", self.dibujando3)
	self.boton4.connect("clicked", self.dibujando4)
	self.boton5.connect("clicked", self.dibujando5)
	self.boton6.connect("clicked", self.dibujando6)
	self.boton7.connect("clicked", self.dibujando7)
	self.boton8.connect("clicked", self.dibujando8)
	self.boton9.connect("clicked", self.dibujando9)
	self.boton0.connect("clicked", self.dibujando0)


	
	self.caja1 = gtk.HBox() 
	self.caja1.pack_start(self.boton1)
	self.caja1.pack_start(self.boton2)
	self.caja1.pack_start(self.boton3)
	self.caja1.pack_start(self.boton4)
	self.caja1.pack_start(self.boton5)
	self.caja1.pack_start(self.boton6)
	self.caja1.pack_start(self.boton7)
	self.caja1.pack_start(self.boton8)
	self.caja1.pack_start(self.boton9)
	self.caja1.pack_start(self.boton0)

	self.caja = gtk.VBox()
	self.caja.pack_start(self.areaDibujo)
        self.caja.pack_start(self.caja1)



	self.ventana.add(self.caja)
	self.areaDibujo.connect("expose-event", self.dibujando)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()


    def main(self):
	gtk.main()

    def dibujando(self, event, widget):
	ctx = widget.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(0.5,0.5,0.5 ) # fondo azul
	ctx.rectangle(0, 0, 300, 300)#tamanio del fondo
	ctx.fill()

	ctx.set_source_rgb(0, 0, 0)
	ctx.rectangle(25, 25, 250,250)
        ctx.fill()

	# draw a rectangle
	ctx.set_source_rgb(1, 1, 1)
	ctx.rectangle(30, 30, 240,240)
        ctx.fill()

	ctx.set_source_rgb(1,0,0)
	ctx.arc(150,150,95,95,365*74)
	ctx.fill()

	ctx.set_source_rgb(1,1,1)
	ctx.arc(150,150,90,90,365*74)
	ctx.fill()

	ctx.set_source_rgb(0,0,.8)
	ctx.rectangle(110,120,5,35)
	ctx.fill()

	ctx.set_source_rgb(0,0,.8)
	ctx.rectangle(180,120,5,35)
	ctx.fill()

	ctx.set_source_rgb(0.5,0,0)
	ctx.rectangle(130,190,45,5)
	ctx.fill()


    def dibujando1(self, areaDibujo):
	ctx = self.areaDibujo.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(1,1,1 ) # fondo azul
	ctx.rectangle(0, 0, 300, 300)#tamanio del fondo
	ctx.fill()
 
        # dibujando el texto
        ctx.select_font_face('Ubuntu')#definiendo la fuente de las letras
        ctx.set_font_size(150) # definiendo el tamanio de la fuente
  	ctx.move_to(100, 190) # moviendo las letras hacien un punto
 	ctx.set_source_rgb(.50, .90, 0) # letras amarillas
 	ctx.show_text('1')#mostrando el texto
  	ctx.stroke() # commit to surface
   

    def dibujando2(self, areaDibujo):
	ctx = self.areaDibujo.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(1,1,1 ) # fondo azul
	ctx.rectangle(0, 0, 300, 300)#tamanio del fondo
	ctx.fill()
 
        # dibujando el texto
        ctx.select_font_face('Sans')#definiendo la fuente de las letras
        ctx.set_font_size(150) # definiendo el tamanio de la fuente
  	ctx.move_to(100, 190) # moviendo las letras hacien un punto
 	ctx.set_source_rgb(.50, .90, 0) # letras amarillas
 	ctx.show_text('2')#mostrando el texto
  	ctx.stroke() # commit to surface
     
    def dibujando3(self, areaDibujo):
	ctx = self.areaDibujo.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(1,1,1 ) # fondo azul
	ctx.rectangle(0, 0, 300, 300)#tamanio del fondo
	ctx.fill()
 
        # dibujando el texto
        ctx.select_font_face('Sans')#definiendo la fuente de las letras
        ctx.set_font_size(150) # definiendo el tamanio de la fuente
  	ctx.move_to(100, 190) # moviendo las letras hacien un punto
 	ctx.set_source_rgb(.50, .90, 0) # letras amarillas
 	ctx.show_text('3')#mostrando el texto
  	ctx.stroke() # commit to surface

    def dibujando4(self, areaDibujo):
	ctx = self.areaDibujo.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(1,1,1 ) # fondo azul
	ctx.rectangle(0, 0, 300, 300)#tamanio del fondo
	ctx.fill()
 
        # dibujando el texto
        ctx.select_font_face('Sans')#definiendo la fuente de las letras
        ctx.set_font_size(150) # definiendo el tamanio de la fuente
  	ctx.move_to(100, 190) # moviendo las letras hacien un punto
 	ctx.set_source_rgb(.50, .90, 0) # letras amarillas
 	ctx.show_text('4')#mostrando el texto
  	ctx.stroke() # commit to surface


    def dibujando5(self, areaDibujo):
	ctx = self.areaDibujo.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(1,1,1 ) # fondo azul
	ctx.rectangle(0, 0, 300, 300)#tamanio del fondo
	ctx.fill()
 
        # dibujando el texto
        ctx.select_font_face('Sans')#definiendo la fuente de las letras
        ctx.set_font_size(150) # definiendo el tamanio de la fuente
  	ctx.move_to(100, 190) # moviendo las letras hacien un punto
 	ctx.set_source_rgb(.50, .90, 0) # letras amarillas
 	ctx.show_text('5')#mostrando el texto
  	ctx.stroke() # commit to surface

    def dibujando6(self, areaDibujo):
	ctx = self.areaDibujo.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(1,1,1 ) # fondo azul
	ctx.rectangle(0, 0, 300, 300)#tamanio del fondo
	ctx.fill()
 
        # dibujando el texto
        ctx.select_font_face('Sans')#definiendo la fuente de las letras
        ctx.set_font_size(150) # definiendo el tamanio de la fuente
  	ctx.move_to(100, 190) # moviendo las letras hacien un punto
 	ctx.set_source_rgb(.50, .90, 0) # letras amarillas
 	ctx.show_text('6')#mostrando el texto
  	ctx.stroke() # commit to surface

    def dibujando7(self, areaDibujo):
	ctx = self.areaDibujo.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(1,1,1 ) # fondo azul
	ctx.rectangle(0, 0, 300, 300)#tamanio del fondo
	ctx.fill()
 
        # dibujando el texto
        ctx.select_font_face('Sans')#definiendo la fuente de las letras
        ctx.set_font_size(150) # definiendo el tamanio de la fuente
  	ctx.move_to(100, 190) # moviendo las letras hacien un punto
 	ctx.set_source_rgb(.50, .90, 0) # letras amarillas
 	ctx.show_text('7')#mostrando el texto
  	ctx.stroke() # commit to surface

    def dibujando8(self, areaDibujo):
	ctx = self.areaDibujo.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(1,1,1 ) # fondo azul
	ctx.rectangle(0, 0, 300, 300)#tamanio del fondo
	ctx.fill()
 
        # dibujando el texto
        ctx.select_font_face('Sans')#definiendo la fuente de las letras
        ctx.set_font_size(150) # definiendo el tamanio de la fuente
  	ctx.move_to(100, 190) # moviendo las letras hacien un punto
 	ctx.set_source_rgb(.50, .90, 0) # letras amarillas
 	ctx.show_text('8')#mostrando el texto
  	ctx.stroke() # commit to surface

    def dibujando9(self, areaDibujo):
	ctx = self.areaDibujo.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(1,1,1 ) # fondo azul
	ctx.rectangle(0, 0, 300, 300)#tamanio del fondo
	ctx.fill()
 
        # dibujando el texto
        ctx.select_font_face('Sans')#definiendo la fuente de las letras
        ctx.set_font_size(150) # definiendo el tamanio de la fuente
  	ctx.move_to(100, 190) # moviendo las letras hacien un punto
 	ctx.set_source_rgb(.50, .90, 0) # letras amarillas
 	ctx.show_text('9')#mostrando el texto
  	ctx.stroke() # commit to surface

    def dibujando0(self, areaDibujo):
	ctx = self.areaDibujo.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(1,1,1 ) # fondo azul
	ctx.rectangle(0, 0, 300, 300)#tamanio del fondo
	ctx.fill()
 
        # dibujando el texto
        ctx.select_font_face('Sans')#definiendo la fuente de las letras
        ctx.set_font_size(150) # definiendo el tamanio de la fuente
  	ctx.move_to(100, 190) # moviendo las letras hacien un punto
 	ctx.set_source_rgb(.50, .90, 0) # letras amarillas
 	ctx.show_text('0')#mostrando el texto
  	ctx.stroke() # commit to surface

if __name__ == "__main__":
   objeto = dibujar()
   objeto.main()
