#!/usr/bin/env python

import screenlets
from screenlets.options import StringOption, BoolOption#, IntOption, ColorOption, FontOption
import cairo
import gtk
import pango
#import time
from os import system
from datetime import datetime
import gobject

class DigitalClockScreenlet(screenlets.Screenlet):
   
   # default meta-info for Screenlets
   __name__ = 'DigitalClock'
   __version__ = '0.7'
   __author__ = 'Nemanja Jovicic'
   __desc__ = 'Display time/date and day of week'

   # internals
   __timeout = None

   # editable options and defaults
   __update_interval = 1 # every second
   
   

   use_ampm = True
   am= False
   pm= False
   day = 1
   date_on_click= True  #true - showing time, if clicked on screenlet shows date
                        #false - showing date, if clicked shows time
                        
   clicked=False        #true - if mouse button 1 clicked on screenlet 
   
   date_format_choices=['dd:mm.yy','yy:mm.dd','mm:yy.dd']
   date_format='dd:mm.yy'

   # constructor
   def __init__(self, **keyword_args):
      # call super
      screenlets.Screenlet.__init__(self, width=250, height=100, **keyword_args)
      self.x=250
      self.y=200
      # set theme
      self.theme_name = "default"
      
      self.add_menuitem("use_ampm", "Use AM/PM format")
      self.add_menuitem("date_time", "Date/Time on click")
      # add default menu items
      self.add_default_menuitems()
      

      #add custom option
      self.add_options_group('Look', 'Additional settings for the look of Digital Clock ...')
      #am/pm
      self.add_option(BoolOption('Look', 'use_ampm', self.use_ampm, 'Use AM/PM time format', 'Show time in AM/PM time format'))
      self.add_option(BoolOption('Look', 'date_on_click', self.date_on_click, 'Show time (on click date)', 'If checked shows time, and on click shows date, if not checked shows date, and on click shows time'))  
      self.add_option(StringOption('Look', 'date_format',self.date_format,'Date format','',choices=self.date_format_choices ))

      

      self.__timeout = gobject.timeout_add(self.__update_interval * 1000, self.update)

   def __setattr__(self, name, value):
      # call Screenlet.__setattr__ in baseclass (ESSENTIAL!!!!)
      screenlets.Screenlet.__setattr__(self, name, value)
      

   def update(self):
      gobject.idle_add(self.redraw_canvas)
      return True

   def on_draw(self, ctx):
      
      # if theme is loaded
      if self.theme:
         
         ctx.save()
         ctx.scale(self.scale , self.scale)
         ctx.translate(0, 0)
         self.theme.render(ctx, 'background')
         ctx.restore()

         
         ctx.scale(self.scale, self.scale)   
         
         # am-pm
         ctx.save()
         ctx.translate(188,4)   
         if self.am==True: self.theme.render(ctx, 'am')
         elif self.pm==True: self.theme.render(ctx, 'pm')
         ctx.restore()         
         ctx.save()
         
         self.day="d"+str(datetime.now().strftime("%u"))   
         ctx.translate(50,74)
         self.theme.render(ctx, self.day)
         ctx.restore()

         ctx.save()
         ctx.translate(15, 12)

         #if time_date[XX] == 'x' it shouldn't draw any number on this place
         time_date=self.get_time_date()
         if(time_date[0]!='x'): self.theme.render(ctx, time_date[0])      
         ctx.translate(40, 0)   
         if(time_date[1]!='x'): self.theme.render(ctx, time_date[1])
         ctx.translate(48, 0)   
         if(time_date[3]!='x'): self.theme.render(ctx, time_date[3])   
         ctx.translate(40, 0)   
         if(time_date[4]!='x'): self.theme.render(ctx, time_date[4])
         ctx.scale(.5,.5)
         ctx.translate(106, 66)   
         if(time_date[6]!='x'): self.theme.render(ctx, time_date[6])   
         ctx.translate(40, 0)   
         if(time_date[7]!='x'): self.theme.render(ctx, time_date[7])
         
         ctx.restore()

         ctx.save()
         ctx.translate(0, 0)
         self.theme.render(ctx, 'glass')
         ctx.restore()

   def on_draw_shape(self, ctx):
      if self.theme:
         self.on_draw(ctx)
   
   def menuitem_callback(self, widget, id):
      screenlets.Screenlet.menuitem_callback(self, widget, id)
      if id == "use_ampm":
         self.use_ampm = not self.use_ampm
         self.update()
         
      if id == "date_time":
         self.date_on_click = not self.date_on_click
         self.update()
   
   def get_time_date(self):
      #if (self.clicked == False and self.date_on_click == True) or (self.clicked == True and self.date_on_click == False)
      if self.clicked != self.date_on_click: #came from upper if
         if self.use_ampm == True:
            time = datetime.now().strftime("%H")
            if int(time)>12: 
            
               if int(time)-12<10:
                  time="x"+str(int(time)-12)
               else: 
                  time=str(int(time)-12)
               self.pm=True
               self.am=False
            else: 
               self.am=True
               self.pm=False
            time+=datetime.now().strftime(":%M:%S")
            
         else:
            time = datetime.now().strftime("%H:%M:%S")
            self.am = False
            self.pm = False
      else:
         day=datetime.now().strftime("%d")
         month=datetime.now().strftime("%m")
         year=datetime.now().strftime("%y")

         if int(day)<10:
            day=day[1]+"x"
                     
         if int(month)<10:
            month=month[1]+"x"
         
         if self.date_format == 'mm:yy.dd':
            time = month+":"+year+"."+day
         elif self.date_format == 'yy:mm.dd':
            time = year+":"+month+"."+day
         else:
            time = day+":"+month+"."+year

      return time

   def on_mouse_down(self, event):
      if event.button == 1:
         self.clicked=True #not self.clicked
         self.update()
      return False

   #if mouse is moved after click self.clicked=False, and then screenlet shows
   #time or date depending on self.date_on_click        
   def on_mouse_move(self, event):
      self.clicked=False


   
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
   import screenlets.session
   screenlets.session.create_session(DigitalClockScreenlet)
