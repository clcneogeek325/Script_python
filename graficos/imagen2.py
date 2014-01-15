import pygtk    # se importan las librerias gtk
pygtk.require('2.0')
import gtk

class Base: # se define la clase Base
    def destroy(self, widget, data=None):#se crea un metodo para cerrar la vetana o el proceso
	print "La ventana ha sido cerrado por un click"
    
    def cambiar(self, widget):
        self.imagen = gtk.Image()
        self.imagen.set_from_file("newtux.png")



    def __init__(self):# el metodo que tendra la ventana
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)#posicion 
        self.window.set_size_request(600, 600)#las dimensiones de la ventana


        self.window.set_title("Mi primer interface Gtk en python")

        self.botton1 = gtk.Button("Salir")#se crea un boton i sele pone nombre
        self.botton1.connect("clicked", self.destroy)#se conecta con el metodo destroi
        self.window.set_tooltip_text("Al dar click en este boton la aplicasion ce cerrar")

        self.botton2 = gtk.Button("Cambiar imagen")#sele poner nombre al boton esconder
        self.botton2.connect("clicked", self.cambiar)

        self.imagen = gtk.Image()
        self.imagen.set_from_file("look-image.jpg")

        self.box1 = gtk.HBox()
        self.box1.pack_start(self.imagen)
       
        self.box2 = gtk.HBox()

        self.box2.pack_start(self.botton1)
        self.box2.pack_start(self.botton2)
         
        self.box = gtk.HBox()
        self.box.pack_start(self.box1)
        self.box.pack_start(self.box2)


        self.window.add(self.box)#se adiciona el box ala ventana
        self.window.show_all()#muestra la ventana
        self.window.connect("destroy", self.destroy)

    def main(self):#es el metodo main
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
 
