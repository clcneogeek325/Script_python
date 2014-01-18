import pygtk
pygtk.require('2.0')
import gtk

class progreso:
    def destroy(self, widget):
        print "La aplicasion se ha cerrado-->...."
        gtk.main_quit()


    def __init__(self):
        self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.ventana.set_position(gtk.WIN_POS_CENTER)
        self.set_title("Barra progreasiva")
        self.set_size_request(400,400)
    
        self.boton = gtk.Button("hola")

        self.ventana.add()
        self.ventana.show_all()
    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = progreso()
    base.main()
