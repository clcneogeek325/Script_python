#18.2.2.Alarm hide

from Tkinter import *

class Alarm(Frame):                             
    def repeater(self):                          

        self.bell()                              
        if self.shown:
            self.stopper.pack_forget()           
        else:                                    
            self.stopper.pack()
        self.shown = not self.shown              
        self.after(self.msecs, self.repeater)    
    def __init__(self, msecs=1000):              
        self.shown = 0
        Frame.__init__(self)
        self.msecs = msecs
        self.pack()
        stopper = Button(self, text='Stop the beeps!', command=self.quit)
        stopper.pack()
        self.stopper = stopper
        self.repeater()
 
Alarm(msecs=500).mainloop()
