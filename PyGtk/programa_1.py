import pygtk, gtk
pygtk.require('2.0')


class Base():
      def __init__(self):
          self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
          self.ventana.set_title("programa base ")
          self.ventana.set_size_request(800,250)
          self.ventana.set_border_width(10)         
          
          self.separadorI = gtk.HSeparator()
          self.separadorD = gtk.HSeparator()
          
          self.separador1 = gtk.HSeparator()
          self.separador2 = gtk.HSeparator()
          self.separador3 = gtk.HSeparator()
          self.separador4 = gtk.HSeparator()

          self.cmdIterar = gtk.Button("Sacar numero aleatorios")
          self.cmdIterar.connect("clicked", self.iterar)
          self.label_A = gtk.Label("a = ")  
          self.label_C = gtk.Label("C = ") 
          self.label_X0 = gtk.Label("X0 = ") 
          self.label_M = gtk.Label("M = ")
           
          self.txt_A = gtk.Entry()
          self.txt_C = gtk.Entry()
          self.txt_X0 = gtk.Entry()
          self.txt_M = gtk.Entry()

          self.txtCuadro = gtk.TextView()
          

          self.sw = gtk.ScrolledWindow()
          self.sw.add(self.txtCuadro)
          self.sw.set_size_request(100,120)

          self.caja1 = gtk.HBox()
          self.caja1.pack_start(self.sw)

          self.caja2 = gtk.HBox()
          self.caja2.pack_start(self.separadorI)
          self.caja2.pack_start(self.cmdIterar)
          self.caja2.pack_start(self.separadorD)

          self.caja3 = gtk.HBox()
          self.caja3.pack_start(self.label_A)
          self.caja3.pack_start(self.separador1)
          self.caja3.pack_start(self.txt_A)
          self.caja3.pack_start(self.label_C)
          self.caja3.pack_start(self.separador2)
          self.caja3.pack_start(self.txt_C)
          self.caja3.pack_start(self.label_X0)
          self.caja3.pack_start(self.separador3)
          self.caja3.pack_start(self.txt_X0)
          self.caja3.pack_start(self.label_M)
          self.caja3.pack_start(self.separador4)
          self.caja3.pack_start(self.txt_M)

          self.caja = gtk.VBox()
          self.caja.pack_start(self.caja2)
          self.caja.pack_start(self.caja3)
          self.caja.pack_start(self.caja1)

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
          
          mul1 = (A * X)
          suma1 = (mul1 + C)
          resul1 = suma1 % M
          X = resul1
          sX = str(X)

          bufer_texto = self.txtCuadro.get_buffer()
          bufer_texto.set_text(sX)
          
          cadena = bufer_texto.get_text(1,1)
          print cadena

        #  resul2 = 0

        #  while resul1 != resul2:
        #      mul = (A * X)
        #      suma2 = (mul2 + C)
        #      resul2 = suma2 % M
        #      X = resul2
        #      sX = str(X)
        #      cadena = bufer_texto.get_buffer()
        #      bufer_texto.set_text("")
        #      bufer_texto.set_text(cadena+sX)

          
      def main(self):
          gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
            
