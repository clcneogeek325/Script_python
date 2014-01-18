#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#  ClearCalendarScreenlet (c) Whise aka Helder Fraga
#  Abbreviated weekdays and first weekday fixed (c) Guido Tabbernuk 2011


import screenlets
from screenlets.options import StringOption, BoolOption, ColorOption
import cairo
import pango
import gtk
import gobject
import datetime
import time
import locale
from screenlets import Plugins
iCal = Plugins.importAPI('iCal')
import sys, os

# source: http://git.gnome.org/browse/hamster-applet/tree/src/hamster/utils/stuff.py?id=628ccaf8afbac987a2ebb3893b7110616a5087f4#n153
# Copyright (C) 2008-2010 Toms Bauģis <toms.baugis at gmail.com>
def locale_first_weekday():
	"""figure if week starts on monday or sunday, from"""
	first_weekday = 6 #by default settle on monday

	try:
		process = os.popen("locale first_weekday week-1stday")
		week_offset, week_start = process.read().split('\n')[:2]
		process.close()
		week_start = datetime.date(*time.strptime(week_start, "%Y%m%d")[:3])
		week_offset = datetime.timedelta(int(week_offset) - 1)
		beginning = week_start + week_offset
		first_weekday = int(beginning.strftime("%w"))
	except:
		print "WARNING - Failed to get first weekday from locale"

	return first_weekday

# use gettext for translation
import gettext

_ = screenlets.utils.get_translator(__file__)

def tdoc(obj):
	obj.__doc__ = _(obj.__doc__)
	return obj

@tdoc
class ClearCalendarScreenlet(screenlets.Screenlet):
	"""A simple multilingual iCalendar Screenlet with month preview, you can scroll through other months too and view monthly events."""
	
	# default meta-info for Screenlets
	__name__ = 'ClearCalendarScreenlet'
	__version__ = '0.4.4+'
	__author__ = 'Whise, robgig1088, tabbernuk'
	__desc__ = __doc__

	# internals
	__timeout = None
	__first_day = locale_first_weekday()
	__day_names = []


	__buttons_pixmap = None
	__buttons_alpha = 0
	__buttons_timeout = None
	__button_pressed = 0
	__month_shift = 0

	# settings
	update_interval = 10
	first_weekday = ''
	enable_buttons = True
	compact_calendar = True
	reader = iCal.ICalReader()
	event1 = ''

	font_color = (1,1,1, 0.8)
	today_color = (1,0,0, 0.8)
	event_color = (0,1,0, 0.8)
	today_event_color = (0,0,1, 0.8)
	background_color = (0,0,0, 0.8)
	showevents = True
	today=datetime.datetime.now().strftime("%F")
	mypath = sys.argv[0][:sys.argv[0].find('ClearCalendarScreenlet.py')].strip()
	if len(mypath)>0:
		mypath = mypath  + "/"
	icalpath = mypath + 'calendar.ics'
	p_layout = None
	# constructor
	def __init__(self, **keyword_args):
		screenlets.Screenlet.__init__(self, width=int(102*2), height=int(105*2),uses_theme=True, **keyword_args) 
		# get localized day names
		locale.setlocale(locale.LC_ALL, '');
		# we convert to unicode here for the first letter extraction to work well
		self.__day_names = [locale.nl_langinfo(locale.DAY_1 + i).decode() for i in range(7)] 
		self.__abday_names = [locale.nl_langinfo(locale.ABDAY_1 + i).decode() for i in range(7)] 
		self.first_weekday = self.__day_names[self.__first_day]
		# call super (and not show window yet)
		# set theme
		self.add_menuitem("icspath", _("Ics file path"))	
		self.add_menuitem("events", _("View events"))
		self.add_menuitem("mini", _("Toggle view events"))
		self.add_menuitem("update", _("Update events"))	
		self.theme_name = "default"
		# add settings
		self.add_options_group(_('iCalendar'), _('Calendar specific options'))
		self.add_option(StringOption(_('iCalendar'), 'first_weekday', self.first_weekday,
			_('First Weekday'), _('The day to be shown in the leftmost column'),
			choices = self.__day_names))
		self.add_option(BoolOption(_('iCalendar'), 'compact_calendar', self.compact_calendar, 
			_('Compact calendar'), _('Save space and show the days above 28th on the first line of calendar if they make a the 6th row')))
		self.add_option(BoolOption(_('iCalendar'), 'enable_buttons', self.enable_buttons, 
			_('Enable month shifting'), _('Enable buttons selecting another months')))
		self.add_option(StringOption(_('iCalendar'), 'icalpath', self.icalpath, _('iCalendar ics file path'), _('The full path where the .ics file is located, in local or url format.')), realtime=False)
		self.add_option(BoolOption(_('iCalendar'), 'showevents',bool(self.showevents), _('Show iCalendar events'),_('Show iCalendar events')),realtime=False)
		self.add_option(ColorOption(_('iCalendar'),'font_color', 
			self.font_color, _('Text color'), 'font_color'))
		self.add_option(ColorOption(_('iCalendar'),'background_color', 
			self.background_color, _('Back color(only with default theme)'), _('Only works with default theme')))
		self.add_option(ColorOption(_('iCalendar'),'today_color', 
			self.today_color, _('Today color'), 'today_color'))
		self.add_option(ColorOption(_('iCalendar'),'event_color', 
			self.event_color, _('Event day color'), 'event_color'))
		self.add_option(ColorOption(_('iCalendar'),'today_event_color', 
			self.today_event_color, _('Today event color'), 'today_event_color'))
		# init the timeout functions
		self.update_interval = self.update_interval
		self.enable_buttons = self.enable_buttons
		self.reader.readURL(self.icalpath)
		self.showevents = self.showevents
	# attribute-"setter", handles setting of attributes
	def __setattr__(self, name, value):
		# call Screenlet.__setattr__ in baseclass (ESSENTIAL!!!!)
		screenlets.Screenlet.__setattr__(self, name, value)
		# check for this Screenlet's attributes, we are interested in:
		if name == 'icalpath':
			self.reader = iCal.ICalReader()
			self.reader.readURL(self.icalpath)
			if self.window:
				self.redraw_canvas()
		if name == "update_interval":
			if value > 0:
				self.__dict__['update_interval'] = value
				if self.__timeout:
					gobject.source_remove(self.__timeout)
				self.__timeout = gobject.timeout_add(value 
						* 1000, self.update)
			else:
				# TODO: raise exception!!!
				pass
		elif name == 'first_weekday':
			self.__first_day\
				= self.__day_names.index(self.first_weekday)
			self.update()
		elif name == 'compact_calendar':
			self.update()
		elif name == 'enable_buttons':
			self.__dict__['enable_buttons'] = value
			if value == True and not self.__buttons_timeout:
				self.__buttons_timeout = gobject.timeout_add(100, 
						self.update_buttons)
			elif value == False and self.__buttons_timeout:
				gobject.source_remove(self.__buttons_timeout)
				self.__buttons_timeout = None
				self.__buttons_alpha = 0
				self.update()
	def on_init (self):
		print "Screenlet has been initialized."
		# add default menuitems
		self.add_default_menuitems()	
	
	def get_date_info(self):
		today = datetime.datetime.now()
		day = today.day
		month = today.month
		year = today.year
		# apply month shift
		if self.__month_shift:
			month += self.__month_shift
			if month > 12:
				year += int((month - 1) / 12)
				month -= (year - today.year) * 12
			elif month <= 0:
				year -= int((12 - month) / 12)
				month += (today.year - year) * 12
		# get first day of the updated month
		month_num = datetime.datetime.now().strftime("%m")
		first_day = datetime.date(year, month, 1)
		# get the month name
		month_name = first_day.strftime("%B")
		month_num = first_day.strftime("%m")
		# get the day count
		when = datetime.date(int(year), int(month), int(1))
		# get the first day of the month (mon, tues, etc..)
		first_day = when.strftime("%A")
		# find number of days in the month
		if month in (1, 3, 5, 7, 8, 10, 12):
			days_in_month = 31
		elif month <> 2:
			days_in_month = 30
		elif year%4 == 0:
			days_in_month = 29
		else:
			days_in_month = 28
		#find the first day of the month
		start_day = int(when.strftime("%u"))  
		if start_day == 7:				# and do calculations on it...
			start_day = 0   
		start_day = start_day + 1
	
		# return as array
		return [day, year, month_name, days_in_month, start_day,month_num]

	def on_map(self):
		if not self.__timeout:
			self.__timeout = gobject.timeout_add(self.__dict__['update_interval']
						* 1000, self.update)
		if self.__dict__['enable_buttons'] == True and not self.__buttons_timeout:
			self.__buttons_timeout = gobject.timeout_add(100, 
					self.update_buttons)
 
	def on_unmap(self):
		if self.__timeout:
			gobject.source_remove(self.__timeout)
			self.__timeout = None
		if self.__buttons_timeout:
			gobject.source_remove(self.__buttons_timeout)
			self.__buttons_timeout = None

	# timeout-functions
	def update(self):
		self.icalpath = self.icalpath
		self.redraw_canvas()
		return True

	def update_buttons(self):
		x, y = self.window.get_pointer()
		x /= (2*self.scale)
		y /= (2*self.scale)
		al_last = self.__buttons_alpha
		if x >= 0 and x < 100 and y >= 0 and y <= 15:	# top line
			self.__buttons_alpha = min(self.__buttons_alpha + 0.2, 1.0)
		else:
			self.__buttons_alpha = max(self.__buttons_alpha - 0.2, 0.0)
		if self.__buttons_alpha != al_last:
			self.redraw_canvas()
		return True

	def on_load_theme(self):
		self.init_buttons()

	def on_scale(self):

		if self.window:
			self.init_buttons()

	# redraw button buffer. FIXME: the pixmap is used to enable alpha-rendering of the SVGs.
	def init_buttons(self):
		if self.window is None or self.window.window is None:
			return
		if self.__buttons_pixmap:
			del self.__buttons_pixmap
		self.__buttons_pixmap = gtk.gdk.Pixmap(self.window.window, int(self.width 
			* (2*self.scale)), int(self.height * (2*self.scale)), -1)
		ctx = self.__buttons_pixmap.cairo_create()
		self.clear_cairo_context(ctx)
		ctx.scale(2 *self.scale, 2* self.scale)
		ctx.set_operator(cairo.OPERATOR_OVER)
		self.theme.render(ctx,'buttons-dim')
		ctx.translate(0, 50)	# bottom half
		self.theme.render(ctx,'buttons-press')
		del ctx

	def on_mouse_down(self, event):
		if self.enable_buttons and event.button == 1:
			if event.type == gtk.gdk.BUTTON_PRESS:
				return self.detect_button(event.x, event.y)
			else:
				return True
		return False

	def on_mouse_up(self, event):
		# do the active button's action
		if self.__button_pressed:
			if self.__button_pressed == 1:
				self.__month_shift -= 1
			elif self.__button_pressed == 2:
				self.__month_shift = 0
			elif self.__button_pressed == 3:
				self.__month_shift += 1
			self.__button_pressed = 0
			self.redraw_canvas()
		return False

	def detect_button(self, x, y):
		x /= (2*self.scale)
		y /= (2*self.scale)

		button_det = 0
		if y >= 5.5 and y <= 12.5:
			if x >= 8.5 and x <= 15.5:
				button_det = 1
			elif x >= 18.5 and x <= 25.5:
				button_det = 2
			elif x >= 28.5 and x <= 35.5:
				button_det = 3
		self.__button_pressed = button_det
		if button_det:
			self.redraw_canvas()
			return True	# we must return boolean for Screenlet.button_press
		else:
			return False

	def menuitem_callback(self, widget, id):
		screenlets.Screenlet.menuitem_callback(self, widget, id)

		if id == "events":
			screenlets.show_message(self,self.event1)
			self.redraw_canvas()
		if id=="icspath":
			self.show_edit_dialog()
			


		if id == "mini":
			self.showevents = not self.showevents
			self.redraw_canvas()
	
		if id=="update":
			
			self.update()
	
	def on_draw(self, ctx):
		# get data
		date = self.get_date_info() # [day, year, month_name, days_in_month, start_day]
		# set size
		ctx.scale(2*self.scale, 2*self.scale)
		# draw bg (if theme available)
		ctx.set_operator(cairo.OPERATOR_OVER)
		
		start_day = (int(date[4]) + 7 - self.__first_day)%7
		if start_day == 0: start_day = 7
		
		if self.theme:
			ctx.set_source_rgba(*self.background_color)
			if self.theme_name == 'default':
				if self.compact_calendar:
					self.draw_rounded_rectangle(ctx,0,1,8,100,88)
				else:
					if date[3] + start_day <= 36: # five weeks with spaces
						self.draw_rounded_rectangle(ctx,0,1,8,100,88)
					else:
						# more than 6 rows
						self.draw_rounded_rectangle(ctx,0,1,8,100,99)
			try:
				#FIXME:when there are 6 rows use 'date-bg2', otherwise 'date-bg'
				if self.compact_calendar:
					self.theme.render(ctx,'date-bg')
				else:
					if date[3] + start_day <= 36: # five weeks with spaces
						self.theme.render(ctx,'date-bg')
					else:
						# more than 6 rows
						self.theme.render(ctx,'date-bg2')
			except:pass
			#self.theme['date-border.svg'].render_cairo(ctx)
		# draw buttons and optionally the pressed one
		if self.p_layout == None :
	
			self.p_layout = ctx.create_layout()
		else:
		
			ctx.update_layout(self.p_layout)
		if self.__buttons_pixmap:
			ctx.save()
			ctx.rectangle(0, 0, 100, 15)
			ctx.clip()
			ctx.identity_matrix()
			ctx.set_source_pixmap(self.__buttons_pixmap, 0, 0)
			ctx.paint_with_alpha(self.__buttons_alpha)
			ctx.restore()
			if self.__button_pressed:
				ctx.save()
				ctx.rectangle(26.5 + self.__button_pressed * 10, 0, 10, 15)
				ctx.clip()
				ctx.identity_matrix()
				# use bottom half of the pixmap
				ctx.set_source_pixmap(self.__buttons_pixmap, 0, -50 * 2* self.scale)
				ctx.paint()
				ctx.restore()
				
		# draw the calendar foreground
		if self.theme:
			ctx.save()
			ctx.translate(5,5)
			if self.p_layout == None :
	
			       self.p_layout = ctx.create_layout()
		        else:
		
			       ctx.update_layout(self.p_layout)
			p_fdesc = pango.FontDescription()
			p_fdesc.set_family_static("Tahoma")
			p_fdesc.set_size(5 * pango.SCALE)
			self.p_layout.set_font_description(p_fdesc)      ### draw the month
			self.p_layout.set_width((self.width - 10) * pango.SCALE)
			self.p_layout.set_markup('<b>' + date[2] + '</b>')
			ctx.set_source_rgba(*self.font_color)
			
			
			#ctx.show_layout(self.p_layout)
		
			ctx.translate(-100,0)
			self.p_layout.set_width((self.width - 10) * pango.SCALE)
			self.p_layout.set_alignment(pango.ALIGN_RIGHT)
			self.p_layout.set_markup("<b>" + date[2]+' '+ str(date[1])+ '  </b>') ### draw the year
			ctx.set_source_rgba(*self.font_color)
			ctx.show_layout(self.p_layout)

			ctx.restore()
			ctx.save()

			ctx.translate(0, 15)
			#self.theme['header-bg.svg'].render_cairo(ctx)  #draw the header background
			ctx.translate(6, 0)
			p_fdesc.set_size(4 * pango.SCALE)
			self.p_layout.set_font_description(p_fdesc) 
			#Draw header
			self.p_layout.set_alignment(pango.ALIGN_CENTER);
			self.p_layout.set_width(10*pango.SCALE);
			self.event1 = ''
			for i in range(7):
				dayname = self.__abday_names[(i \
					+ self.__first_day) % 7]
				self.p_layout.set_markup("<b><span font_desc='Monospace'>" + dayname + '</span></b>') # use first letter
				ctx.set_source_rgba(*self.font_color)
				ctx.show_layout(self.p_layout)
				ctx.translate(13, 0)	# 6 + 6*13 + 6 = 100
			p_fdesc.set_size(6 * pango.SCALE)
			p_fdesc.set_family_static("FreeSans")

			self.p_layout.set_font_description(p_fdesc) 
			# Draw the day labels
			ctx.restore()
			row = 1

			day = (int(date[4]) + 7 - self.__first_day)%7
			if day == 0 :
				day = 7
			for x in range(date[3]):
				ctx.save()

				if row == 6:
					if self.compact_calendar: row = 1
				ctx.translate(6 + (day - 1)*13, 25 + 12*(row - 1))
				#print str(6 + (day - 1)*13)
				#print str( 25 + 12*(row - 1))
				if self.__month_shift == 0 and int(x)+1 == int(date[0]):
					ctx.set_source_rgba(*self.today_color)
					self.draw_rounded_rectangle(ctx,0,0,2,11,10)
				if self.showevents == True:
					for event in self.reader.events:
						
						myevent = str(event.startDate)
						myevent  = myevent[:myevent.find(' ')].strip()
	
						a = str(x +1)
						if len(a) == 1:
							a = '0' + a
					
						if myevent == str(date[1]) + '-' + str(date[5])+ '-' + str(a) :
							ctx.set_source_rgba(*self.event_color)
							self.draw_rounded_rectangle(ctx,0,0,2,11,10)
							if int(date[1]) >= int(self.today[:4]) or int(date[1]) >= int(self.today[:4]) and int(date[5]) >= int(self.today[5:7]) :
								
								self.event1 = self.event1 + '\n'+ str(date[1]) + '-' + str(date[5])+ '-' + str(a)+ ' - ' +str(event)
						if myevent == datetime.datetime.now().strftime("%F") and self.__month_shift == 0 and int(x)+1 == int(date[0]) :
							ctx.set_source_rgba(*self.today_event_color)
							self.draw_rounded_rectangle(ctx,0,0,2,11,10)

							self.event1 = self.event1 + '\n ' + _('Today') + ' - '+ str(event)
				self.p_layout.set_markup( str(x+1) )
	
				ctx.set_source_rgba(*self.font_color)
				ctx.show_layout(self.p_layout)
				if day == 7:
					day = 0
					row = row + 1
				day = day + 1
				ctx.restore()

	def show_edit_dialog(self):
		# create dialog
		dialog = gtk.Dialog(_("iCalendar ics path"), self.window)
		dialog.resize(300, 100)
		dialog.add_buttons(gtk.STOCK_OK, gtk.RESPONSE_OK, 
			gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		entrybox = gtk.Entry()
		entrybox.set_text(str(self.icalpath))
		dialog.vbox.add(entrybox)
		entrybox.show()	
		# run dialog
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			self.icalpath = entrybox.get_text()
			self.updated_recently = 1
		dialog.hide()
		self.update()

	def on_draw_shape(self,ctx):
		ctx.rectangle(0,0,self.width,self.height)
		ctx.fill()
		self.on_draw(ctx)
	

# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
	import screenlets.session
	screenlets.session.create_session(ClearCalendarScreenlet)
