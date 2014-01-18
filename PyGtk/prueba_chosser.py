#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pygtk, gtk
pygtk.require('2.0')

if gtk.pygtk_version < (2,3,90):
    print "Por fabor atualiza pygtk"
    raise SystemExit

dialogo = gtk.FileChooserDialog("Seleccione la imagen", None, 
gtk.FILE_CHOOSER_ACTION_OPEN,
(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
gtk.STOCK_OPEN, gtk.RESPONSE_OK))

dialogo.set_default_response(gtk.RESPONSE_OK)

filter = gtk.FileFilter()
filter.set_name("All files")
filter.add_pattern("*")
dialogo.add_filter(filter)

response = dialogo.run()

if response == gtk.RESPONSE_OK:
    print dialogo.get_filename(), 'selecionado...'
elif response == gtk.RESPONSE_CANCEL:
   print "Cerrado i cancelado"
   dialog.destroy()

