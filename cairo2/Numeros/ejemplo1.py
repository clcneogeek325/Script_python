import gtk, pygtk, cairo
pygtk.require('2.0')


ventana = gtk.Window( gtk.WINDOW_TOPLEVEL)
ventana.set_position( gtk.WIN_POS_CENTER)
ventana.set_size_request (400,400)
area = gtk.DrawingArea()
area.set_size_request(400,300)
caja = gtk.VBox()
texto = gtk.Entry()
caja.pack_start(area)
caja.pack_start(texto)
ventana.show_all()
ventana.connect("destroy", gtk.main_quit)

if __name__ == "__main__":
	gtk.main()
