#!/usr/bin/env python
import pygtk, gtk
pygtk.require('2.0')


class Base():
      def __init__(self):
          self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
          self.ventana.set_title("programa base ")
          self.ventana.set_size_request(100,300)
          self.ventana.set_border_width(10)         
          
          self.separador1 = gtk.HSeparator()
          self.separador2 = gtk.HSeparator()

          self.boton1 = gtk.Button("1")
          self.boton2 = gtk.Button("2")
          self.boton3 = gtk.Button("3")
          self.boton4 = gtk.Button("4")

          self.txtCuadro = gtk.TextView()

          self.sw = gtk.ScrolledWindow()
          self.sw.add(self.txtCuadro)
          self.sw.set_size_request(100,120)

          self.caja3 = gtk.HBox()
          self.caja3.pack_start(self.boton1)
          self.caja3.pack_start(self.boton2)
          self.caja4 = gtk.HBox()
          self.caja4.pack_start(self.boton3)
          self.caja4.pack_start(self.boton4)

          self.caja1 = gtk.VBox()
          self.caja1.pack_start(self.caja3)
          self.caja1.pack_start(self.caja4)
          self.caja1.pack_start(self.separador1)
          self.caja1.pack_start(self.separador2)

          self.caja2 = gtk.HBox()  
          self.caja2.pack_start(self.sw)



          self.caja = gtk.VBox()
          self.caja.pack_start(self.caja1)
          self.caja.pack_start(self.caja2)

          self.ventana.add(self.caja)
          self.ventana.connect("destroy", self.destroy)
          self.ventana.show_all()
          self.ventana.show()
      
      def destroy(self, widget):
          print "El programa s ha cerrado"
          gtk.main_quit()

      def iterar(self, widget):
          A = float(self.txt_A.get_text())
          C = float(self.txt_C.get_text())
          X = float(self.txt_X0.get_text())
          M = float(self.txt_M.get_text())
          

          for i in range(21):
              mul = (A * X)
              suma = (mul + C)
              resul = suma % M
              self.txtCuadro.set_text("")
              X = resul

          
      def main(self):
          gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
            
