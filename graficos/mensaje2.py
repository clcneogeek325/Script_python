#!/usr/bin/env python
import gtk
 
di = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                  type = gtk.MESSAGE_INFO,
                  buttons = gtk.BUTTONS_OK,
                  message_format = ("Acaso estas pendejo eres un idiota"))
di.set_title("Mensaje")
di.run()
di.destroy()

 

