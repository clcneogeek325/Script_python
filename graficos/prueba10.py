import pygtk    # se importan las librerias gtk
pygtk.require('2.0')
import gtk

class Base: # se define la clase Base
    def destroy(self, widget, data=None):#se crea un metodo para cerrar la vetana o el proceso
	print "La ventana ha sido cerrado por un click"
        gtk.main_quit()

    def myhide(self,widget):
        self.botton1.hide()

    def myshow(self,widget):
         self.botton1.show()

    def __init__(self):# el metodo que tendra la ventana
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)#posicion 
        self.window.set_size_request(600, 100)#las dimensiones de la ventana
        self.window.set_title("Mi primer interface Gtk en python")        



        self.botton1 = gtk.Button("Salir")#se crea un boton i sele pone nombre
        self.botton1.connect("clicked", self.destroy)#se conecta con el metodo destroi

        self.botton2 = gtk.Button("Esconder")#sele poner nombre al boton esconder
        self.botton2.connect("clicked", self.myhide)      
 
        self.botton3 = gtk.Button("mostrar")
        self.botton3.connect("clicked", self.myshow)
        
        self.box1 =gtk.VBox()
        self.box1.pack_start(self.botton1)
        self.box1.pack_start(self.botton2)
        self.box1.pack_start(self.botton3)
         
        self.window.add(self.box1)
        self.window.show_all()#muestra la ventana
        self.window.connect("destroy", self.destroy)

    def main(self):#es el metodo main
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
 
