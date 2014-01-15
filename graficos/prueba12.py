import pygtk    # se importan las librerias gtk
pygtk.require('2.0')
import gtk

class Base: # se define la clase Base
    def destroy(self, widget, data=None):#se crea un metodo para cerrar la vetana o el proceso
	print "La ventana ha sido cerrado por un click"
        gtk.main_quit()
    
    def relabel(self,widget):
        self.label1.set_text("nuevo texto") 
   
    def myhide(self,widget):
        self.botton1.hide()

    def myshow(self,widget):
         self.botton1.show()

    def textchange(self, widget):
        self.window.set_title("El titulo ha sido cambiado")


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
 
        self.label1 = gtk.Label("new label")
 
        self.texto = gtk.Entry()
        self.texto.connect("changed", self.textchange)
            
        self.botton4 = gtk.Button("relabel")
        self.botton4.connect("clicked", self.relabel)

        self.box1 =gtk.HBox()
        self.box1.pack_start(self.botton1)
        self.box1.pack_start(self.botton2)
        self.box1.pack_start(self.botton3)
        self.box1.pack_start(self.label1)
        self.box1.pack_start(self.botton4)
        self.box1.pack_start(self.texto)
         
        self.window.add(self.box1)#se adiciona el box ala ventana
        self.window.show_all()#muestra la ventana
        self.window.connect("destroy", self.destroy)

    def main(self):#es el metodo main
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
 
