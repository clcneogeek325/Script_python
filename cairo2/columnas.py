import gtk

class tablas:
    def __init__(self):
	self.ventana = gtk.Window( gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position( gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(500,500)

	self.treestore = gtk.TreeView()
	self.ventana.add(self.treestore)
	self.ventana.show_all()
	self.ventana.connect("destroy", gtk.main_quit)

    def main(self):
	gtk.main()

if __name__ == "__main__":
    app = tablas()
    app.main()
