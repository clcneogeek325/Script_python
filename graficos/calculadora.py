import  pygtk, gtk
pygtk.require('2.0')

class Calculadora:
    def destroy(self, widget, data=None):
        print "La aplicasion ha terminado"
        gtk.main_quit()

    def __init__(self):
        self.wx = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.wx.set_position(gtk.WIN_POS_CENTER)
        self.wx.set_size_request(400,200)

        self.texto = gtk.Entry()

        self.cmd1 = gtk.Button("1")
        self.cmd1.connect("clicked", self.destroy)

        self.cmd2 = gtk.Button("2")

        self.cmd3 = gtk.Button("3")

        self.cmd4 = gtk.Button("4")

        self.cmd5 = gtk.Button("5")

        self.cmd6 = gtk.Button("6")
       
        self.cmd7 = gtk.Button("7")
       
        self.cmd8 = gtk.Button("8")
        
        self.cmd9 = gtk.Button("9")

        self.cmd0 = gtk.Button("0")

        self.cmdsumar = gtk.Button("+")

        self.cmdrestar = gtk.Button("-")

        self.cmdmultiplicar = gtk.Button("*")

        self.cmddividir = gtk.Button("/")
       
        
        
        self.box2 = gtk.HBox()
        self.box2.pack_start(self.texto)
       
        self.box3 = gtk.VBox()
        self.box3.pack_start(self.cmd1)
        self.box3.pack_start(self.cmd2)
        self.box3.pack_start(self.cmd3)
        self.box3.pack_start(self.cmd4)
       
        self.box4 = gtk.VBox()
        self.box4.pack_start(self.cmd5)
        self.box4.pack_start(self.cmd6)
        self.box4.pack_start(self.cmd7)
       
        self.box5 = gtk.VBox()
        self.box5.pack_start(self.cmd8)
        self.box5.pack_start(self.cmd9)
        self.box5.pack_start(self.cmdsumar)
        
        self.box6 = gtk.VBox()
        self.box6.pack_start(self.cmdrestar)
        self.box6.pack_start(self.cmddividir)
        self.box6.pack_start(self.cmdmultiplicar)
       
        self.box gtk.HBox()
        
        self.wx.add(self.box)
        self.wx.show_all()
        self.wx.connect("destroy", self.destroy)


    def main(self):
        gtk.main()


if __name__  == "__main__":
    cal = Calculadora()
    cal.main()
