import pygtk    # se importan las librerias gtk
pygtk.require('2.0')
import gtk
import os

class Base: # se define la clase Base
    def destroy(self, widget, data=None):#se crea un metodo para cerrar la vetana o el proceso
	print "La aplicasion ha finalizado"
        gtk.main_quit()



    def cambiar_imagen(self, widget):
        self.imagen.set_from_file("Pallazo.png")

    def nombre_imagenes(self, widget):
        archivos = os.popen('ls').read()
        lista_archivos = archivos.split() 
        for x in lista_archivos:
          print x        
    def abrir_imagen(self, widget):
        dialogo = gtk.FileChooserDialog("Seleccione la imagen",
               None, gtk.FILE_CHOOSER_ACTION_OPEN,
               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
               gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        dialogo.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("Imagenes")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.jpeg")
        dialogo.add_filter(filter)
       
        response = dialogo.run()
        if response == gtk.RESPONSE_OK:
            self.pixeles = gtk.gdk.pixbuf_new_from_file(dialogo.get_filename())
            self.pixeles = self.pixeles.scale_simple(600, 400 , gtk.gdk.INTERP_BILINEAR)
            self.imagen = gtk.image_new_from_pixbuf(self.pixeles)
        elif response == gtk.RESPONSE_CANCEL:
            print "No se ha selecionado niguna mimagen"
            raise SystemExit
        dialogo.destroy()

    def textchange(self, widget):
        self.window.set_title(widget.get_text())
        self.label1.set_text(widget.get_text())
   
    def clear_text(self, widget):
        self.texto.set_text("")
   
    def combo_text(self, widget):
        self.texto.set_text(widget.get_active_text())
        

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER) 
        self.window.set_size_request(600, 600)
        self.window.set_title("Mi primer interface Gtk en python")
        self.window.set_border_width(10)

        self.botton1 = gtk.Button("Salir")
        self.botton1.connect("clicked", self.destroy)
        self.botton1.set_tooltip_text("Este boton es para sali") 

        self.botton2 = gtk.Button("Anterior")
        self.botton2.connect("clicked", self.nombre_imagenes)
 
        self.botton3 = gtk.Button("Siguiente")
        self.botton3.connect("clicked", self.cambiar_imagen)
 
 
        self.texto = gtk.Entry()
        self.texto.connect("changed", self.textchange)
        self.texto.set_tooltip_text("Al escribir en el cuadro de texto se cambiara el titulo") 
            
        self.botton4 = gtk.Button("Eliminar")
       
        self.boton5 = gtk.Button("Limpiar texto")
        self.boton5.connect("clicked", self.clear_text)

        self.boton6 = gtk.Button("Abri imagen")
        self.boton6.connect("clicked", self.abrir_imagen)
        self.label1 = gtk.Label("new label")

        self.imagen = gtk.Image()
        self.imagen.set_from_file("look-image.jpg")

        self.box1 = gtk.HBox()
        self.box1.pack_start(self.botton1)
        self.box1.pack_start(self.botton2)
        self.box1.pack_start(self.botton3)
        self.box1.pack_start(self.botton4)
        self.box1.pack_start(self.boton5)
         
        self.box3 = gtk.HBox()
        self.box3.pack_start(self.texto)
        self.box3.pack_start(self.boton6)
      
        self.box2 = gtk.VBox()
        self.box2.pack_start(self.box1)
        self.box2.pack_start(self.label1)
        self.box2.pack_start(self.box3)
        self.box2.pack_start(self.imagen)

        self.window.add(self.box2)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
 
