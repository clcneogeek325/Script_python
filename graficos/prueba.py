import pygtk    # se importan las librerias gtk
pygtk.require('2.0')
import gtk

class Base: # se define la clase Base
    def destroy(self, widget, data=None):#se crea un metodo para cerrar la vetana o el proceso
	print "La ventana ha sido cerrado por un click"
        gtk.main_quit()

    def __init__(self):# el metodo que tendra la ventana
        self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.ventana.set_position(gtk.WIN_POS_CENTER)#la ventana se crear en en certro de la pnatalla
        self.ventana.set_size_request(90, 200)#las dimensiones de la ventana
        
        self.cmdhola = gtk.Button("Hello World")
        self.cmdhola.connect("clicked", self.destroy)
        self.cmdhola.set_tooltip_text("Pulsa al boton si es que quieres sali de programa")
        

        self.caja1 = gtk.HBox()
        self.caja1.pack_start(self.cmdhola)

        

        self.caja = gtk.VBox()
        self.caja.pack_start(self.caja1)
       
        self.ventana.add(self.caja)
        self.ventana.show_all()
        self.ventana.show()#muestra la ventana
        self.ventana.connect("destroy", self.destroy)

    def main(self):#es el metodo main
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
 
