#!/usr/bin/env python
import pygtk    # se importan las librerias gtk
pygtk.require('2.0')
import gtk
import os

class Base:
    def destroy(self, widget, data=None):
	print "La ventana ha sido cerrado por un click"
        gtk.main_quit()


    def numero1(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("1")
        else:
	    self.texto.set_text(self.texto.get_text() + "1")

    def numero2(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("2")
        else:
	    self.texto.set_text(self.texto.get_text() + "2")

    def numero3(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("3")
        else:
	    self.texto.set_text(self.texto.get_text() + "3")

    def numero4(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("4")
        else:
	    self.texto.set_text(self.texto.get_text() + "4")
        
    def numero5(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("5")
        else:
	    self.texto.set_text(self.texto.get_text() + "5")

    def numero6(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("6")
        else:
	    self.texto.set_text(self.texto.get_text() + "6")

    def numero7(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("7")
        else:
	    self.texto.set_text(self.texto.get_text() + "7")

    def numero8(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("8")
        else:
	    self.texto.set_text(self.texto.get_text() + "8")

    def numero9(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("9")
        else:
	    self.texto.set_text(self.texto.get_text() + "9")

    def numero0(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("0")
        else:
	    self.texto.set_text(self.texto.get_text() + "0")

    def suma(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("+")
        else:
	    self.texto.set_text(self.texto.get_text() + "+")

    def resta(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("-")
        else:
	    self.texto.set_text(self.texto.get_text() + "-")

    def dividir(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("/")
        else:
	    self.texto.set_text(self.texto.get_text() + "/")

    def multiplicar(self, texto):
	numero = self.texto.get_text()
	if numero == "":
	    self.texto.set_text("*")
        else:
	    self.texto.set_text(self.texto.get_text() + "*")

    def borrar(self, texto):
        self.texto.set_text("")

    def resultado(self, texto):
	try:
	    self.texto.set_text(str(eval(self.texto.get_text())))
        except:
	    os.popen('zenity --info --text "Pendejo que no sabes hacer operaciones basicas??????"')


    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Calculadora")

        self.window.set_size_request(365, 300)

        self.button1 = gtk.Button("1")
        self.button1.set_size_request(50,50)
	self.button1.connect("clicked", self.numero1)

        self.button2 = gtk.Button("2") 
        self.button2.set_size_request(50,50)
	self.button2.connect("clicked", self.numero2)

        self.button3 = gtk.Button("3") 
        self.button3.set_size_request(50,50)
	self.button3.connect("clicked", self.numero3)

        self.button4 = gtk.Button("4") 
        self.button4.set_size_request(50,50)
	self.button4.connect("clicked", self.numero4)

        self.button5 = gtk.Button("5") 
        self.button5.set_size_request(50,50)
	self.button5.connect("clicked", self.numero5)

        self.button6 = gtk.Button("6") 
        self.button6.set_size_request(50,50)
	self.button6.connect("clicked", self.numero6)

        self.button7 = gtk.Button("7") 
        self.button7.set_size_request(50,50)
	self.button7.connect("clicked", self.numero7)

        self.button8 = gtk.Button("8") 
        self.button8.set_size_request(50,50)
	self.button8.connect("clicked", self.numero8)


        self.button9 = gtk.Button("9") 
        self.button9.set_size_request(50,50)
	self.button9.connect("clicked", self.numero9)

        self.button0 = gtk.Button("0") 
        self.button0.set_size_request(50,50)
	self.button0.connect("clicked", self.numero0)

        self.buttonsumar = gtk.Button("+") 
        self.buttonsumar.set_size_request(50,50)
	self.buttonsumar.connect("clicked", self.suma)

        self.buttonrestar = gtk.Button("-") 
        self.buttonrestar.set_size_request(50,50)
	self.buttonrestar.connect("clicked", self.resta)
       
        self.buttonmultiplicar = gtk.Button("*") 
        self.buttonmultiplicar.set_size_request(50,50)
	self.buttonmultiplicar.connect("clicked", self.multiplicar)

        self.buttondividir = gtk.Button("/") 
        self.buttondividir.set_size_request(50,50)
	self.buttondividir.connect("clicked", self.dividir)
       
        self.buttonborrar = gtk.Button("Limpiar")
        self.buttonborrar.set_size_request(80,50)
	self.buttonborrar.connect("clicked", self.borrar)

	self.botonResultado  =gtk.Button("Resultado")
	self.botonResultado.connect("clicked", self.resultado)
        self.botonResultado.set_size_request(80,50)


        self.texto = gtk.Entry()

        fixed = gtk.Fixed()
        fixed.put(self.button1, 10, 80)        
        fixed.put(self.button2, 70, 80)
        fixed.put(self.button3, 130, 80)
      
        fixed.put(self.button4, 10, 140)
        fixed.put(self.button5, 70, 140)
        fixed.put(self.button6, 130, 140)
     
        fixed.put(self.button7, 10, 200)
        fixed.put(self.button8, 70, 200)
        fixed.put(self.button9, 130, 200)

        fixed.put(self.button0, 190, 200)
	fixed.put(self.botonResultado, 250, 200)
        fixed.put(self.buttonsumar, 210, 80)
        fixed.put(self.buttonrestar, 280, 80)

        fixed.put(self.buttonmultiplicar, 210, 140)
        fixed.put(self.buttondividir, 280, 140)
        
        fixed.put(self.texto, 10, 30)
        fixed.put(self.buttonborrar,210 , 25)
        
        self.window.add(fixed)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
 
