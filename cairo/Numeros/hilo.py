#!/usr/bin/env python
import threading
import time
import gobject
import gtk




gobject.threads_init()

class MyThread(threading.Thread):
     def __init__(self, label):
         super(MyThread, self).__init__()
         self.label = label
         self.quit = False

     def update_label(self, counter):
         self.label.set_text(str(counter))
         return False

     def run(self):
         counter = 0
         while not self.quit:
             counter += 1
             gobject.idle_add(self.update_label, counter)
             time.sleep(1)

w = gtk.Window(gtk.WINDOW_TOPLEVEL)
w.set_position(gtk.WIN_POS_CENTER)
w.set_size_request(100,100)
l = gtk.Label()
w.add(l)
w.show_all()
w.connect("destroy", lambda _: gtk.main_quit())
t = MyThread(l)
t.start()

gtk.main()
t.quit = True
