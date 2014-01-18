#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gtk

class ventana:
      def __init__(self):
          self.ventana = gtk.Window()
          self.ventana.connect("destroy" , gtk.main_quit())
          self.ventana.show()

objeto= ventana()
objeto.gtk.main()

