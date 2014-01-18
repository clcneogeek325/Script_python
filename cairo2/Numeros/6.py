#!/usr/bin/env python
import gtk, pygtk, cairo
pygtk.require('2.0')

class dibujar:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(200,200)
	self.ventana.set_title("Ejemplo de dibujo")

	self.areaDibujo = gtk.DrawingArea()
	self.areaDibujo.connect("expose-event", self.dibujando)
	self.ventana.add(self.areaDibujo)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()


    def main(self):
	gtk.main()

    def dibujando6(self, event, widget):
	ctx = widget.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(0,.20,0 ) # fondo azul
	ctx.rectangle(0, 0, 650, 200)#tamanio del fondo
	ctx.fill()
 
        # dibujando el texto
        ctx.select_font_face('Sans')#definiendo la fuente de las letras
        ctx.set_font_size(90) # definiendo el tamanio de la fuente
  	ctx.move_to(80, 130) # moviendo las letras hacien un punto
 	ctx.set_source_rgb(.50, .90, 0) # letras amarillas
 	ctx.show_text('6')#mostrando el texto
  	ctx.stroke() # commit to surface

if __name__ == "__main__":
   objeto = dibujar()
   objeto.main()
