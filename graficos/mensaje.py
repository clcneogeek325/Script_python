import gtk
 
di = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                  type = gtk.MESSAGE_QUESTION,
                  buttons = gtk.BUTTONS_YES_NO,
                  message_format = ("Acaso estas bien?"))
di.run()
di.destroy()

 

