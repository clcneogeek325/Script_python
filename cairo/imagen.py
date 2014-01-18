#!/usr/bin/env python
import gtk, pygtk, cairo, screenlets
pygtk.require('2.0')

class dibujar:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(400,400)
	self.ventana.set_title("Dibujando un rectangulo")

	self.areaDibujo = gtk.DrawingArea()
	self.areaDibujo.connect("expose-event", self.dibujando)
	self.ventana.add(self.areaDibujo)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()


    def main(self):
	gtk.main()

    def dibujando(self, widget,areaDibujo ):
        self.ctx = self.areaDibujo.window.cairo_create()
	self.pix = gtk.gdk.pixbuf_new_from_file("20wallpapers-de-mujeres.jpg")
	screenlets.Drawing.draw_image(self.ctx,150,150, self.pix)




if __name__ == "__main__":
   objeto = dibujar()
   objeto.main()
