#!/usr/bin/env python

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

#  SysmonitorScreenlet (c) Whise <helder.fraga@hotmail.com>
# 
# Change Log
#
#  2011-05-07  shofi.islam@gmail.com
#	1) For multiple CPUs renumbered sequence from CPU1 to CPU4 to CPU0 to CPU3. Change arrays accordingly.
#	2) Corrected positioning of CPU meters 


import screenlets
from screenlets.options import StringOption , BoolOption , IntOption, ColorOption, FontOption, ImageOption
from screenlets import DefaultMenuItem
from screenlets import sensors
import pango
import gobject
import gtk
import os
import decimal

# use gettext for translation
import gettext

_ = screenlets.utils.get_translator(__file__)

def tdoc(obj):
	obj.__doc__ = _(obj.__doc__)
	return obj

@tdoc
class SysmonitorScreenlet (screenlets.Screenlet):
	"""A simple system monitor Screenlet based in conky"""
	
	# default meta-info for Screenlets (should be removed and put into metainfo)
	__name__	= 'SysmonitorScreenlet'
	__version__	= '0.1.7'
	__author__	= 'Whise'
	__desc__	= __doc__	# set description to docstring of class
	
	# editable options (options that are editable through the UI)

	fontsize = 10
	expand = True
	color_text =(1.0, 1.0, 1.0, 0.7)
	color_background =(0.0, 0.0, 0.0, 0.7)
	color_graph =(1.0, 1.0, 1.0, 0.2)
	font= "FreeSans"
	username = ''
	hostname = ''
	date = ''
	time = ''
	kernel = ''
	distro = ''
	avg_load = ''
	cpu_nb = 0
	old_cpu = [0,0,0,0]
	new_cpu = [0,0,0,0]
	cpu_load = [0,0,0,0]
	distroshort = ''
	cpu_name= ''
	mem_used = 0
	swap_used = 0
	up = 0
	down = 0
	old_up = 0
	old_down = 0
	upload = 0
	download =0
	ip = ''
	disks = []
	disk = []
	bat_list= []
	bat_data=[]
	bat_load = 0
	bat_rate = 0
	bat_current = 0
	bat_state = ''
	wire_list = []
	wire_data = []
	newheight = gtk.gdk.screen_height()
	show_logo = True
	show_frame = True
	starty = 0
	number = 0
	_update_interval = 1
	font1 = 'FreeSans'
	image_filename = ''
	use_bg_image = False
	use_mil_time = True

	#Sensors to display
	show_time = True
	show_date = True
	show_username = True
	show_distro = True
	show_kernel = True
	show_cpuname = True
	show_cpus = True
	show_load = True
	show_mem = True
	show_swap = True
	show_ip = True
	show_updown = True
	show_disks = True
	show_bat_wir = True
	show_processes = True
	show_uptime = True



	# constructor
	def __init__ (self, **keyword_args):
		#call super (width/height MUST match the size of graphics in the theme)
		screenlets.Screenlet.__init__(self, width=180, height=self.newheight, 
			uses_theme=True,ask_on_option_override=False, **keyword_args)
		# set theme
		self.get_constants()
		self.theme_name = "default"
		# add option group
		self.add_options_group(_('Sysmonitor'), _('Options ...'))
		# add editable option to the groupSysmonitor

		self.add_option(BoolOption(_('Sysmonitor'),'expand', 
			self.expand, _('Expand height'), 
			_('Expand height to screen height')))

		self.add_option(BoolOption(_('Sysmonitor'),'show_logo', 
			self.show_logo, _('Show distro logo if available'), 
			_('Show distro logo if available')))

		self.add_option(BoolOption(_('Sysmonitor'),'show_frame', 
			self.show_frame, _('Show frame'), 
			_('Show frame window')))

		self.add_option(IntOption(_('Sysmonitor'), 'update_interval',self.update_interval, _('Update Interval'),'',min=1, max=60))

		self.add_option(IntOption(_('Sysmonitor'), 'starty',self.starty, _('Y position to start the text'),'',min=0, max=500))

		self.add_option(FontOption(_('Sysmonitor'),'font', 
			self.font, _('Text Font'), 
			_('Text font')))

		self.add_option(ColorOption(_('Sysmonitor'),'color_text', 
			self.color_text, _('Text color'), ''))

		self.add_option(ColorOption(_('Sysmonitor'),'color_background', 
			self.color_background, _('Background Color'), 
			''))
		self.add_option(ColorOption(_('Sysmonitor'),'color_graph', 
			self.color_graph, _('Graphs Color'), 
			''))
		self.add_options_group(_('Backgound'), _('Options ...'))
		self.add_option(BoolOption(_('Backgound'),'use_bg_image', 
			self.use_bg_image, _('Use Background image'), 
			'use_bg_image'))
		self.add_option(BoolOption(_('Sysmonitor'),'use_mil_time',
			self.use_mil_time, _('24 hour clock'),
			_('24 hour clock')))
		self.add_option(ImageOption(_('Backgound'), 'image_filename', 
			self.image_filename, _('Background image'),
			_('Background image'))) 

		self.add_options_group(_('Sensors'), _('Options ...'))

		self.add_option(BoolOption(_('Sensors'),'show_time', 
			self.show_time, _('Show time'), 
			_('Show Sensor')))

		self.add_option(BoolOption(_('Sensors'),'show_date', 
			self.show_date, _('Show date'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_username', 
			self.show_username, _('Show username'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_distro', 
			self.show_distro, _('Show distro'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_kernel', 
			self.show_kernel, _('Show kernel'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_cpuname', 
			self.show_cpuname, _('Show Cpu name'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_cpus', 
			self.show_cpus, _('Show Cpus'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_load', 
			self.show_load, _('Show Load'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_mem', 
			self.show_mem, _('Show Memory'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_swap', 
			self.show_swap, _('Show Swap'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_ip', 
			self.show_ip, _('Show Ip'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_updown', 
			self.show_updown, _('Show Upload Download'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_disks', 
			self.show_disks, _('Show Disks'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_bat_wir', 
			self.show_bat_wir, _('Show battery and wifi'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_processes', 
			self.show_processes, _('Show Processes'), 
			_('Show Sensor')))
		self.add_option(BoolOption(_('Sensors'),'show_uptime', 
			self.show_uptime, _('Show Uptime'), 
			_('Show Sensor')))
		# ADD a 1 second (1000) TIMER
		self.timer = None

		#Also add options from xml file for example porpuse

	# getter and setter methods to be used by the update_interval property
	def get_update_interval(self):
		return self._update_interval

	def set_update_interval(self, new_interval):
		if new_interval < 1: new_interval = 1
		if new_interval != self._update_interval:
			if self.timer:
				gobject.source_remove(self.timer)
			self.timer = gobject.timeout_add(int(new_interval * 1000), self.update)
			self._update_interval = new_interval

	# create an update_interval property that controls restarting the update timer
	update_interval = property(get_update_interval, set_update_interval)

	def get_constants(self):
		self.username = sensors.sys_get_username()
		self.hostname = sensors.sys_get_hostname ()
		self.kernel = sensors.sys_get_kernel_version()
		self.distro = sensors.sys_get_distrib_name()
		self.distroshort = sensors.sys_get_distroshort()
		self.cpu_nb = sensors.cpu_get_nb_cpu()
		self.cpu_name = sensors.cpu_get_cpu_name()

	def get_variables(self):
		if self.show_time: 
			if self.use_mil_time:
				self.time = sensors.cal_get_time24() + ':' + str(sensors.cal_get_second())
			else:
				self.time = sensors.cal_get_local_time()
		if self.show_date: self.date = sensors.cal_get_day_name() + ' '+  sensors.cal_get_local_date()
		if self.show_load: self.avg_load = sensors.sys_get_average_load()
		if self.show_cpus:
			for i in range (0,self.cpu_nb):  #Sets CPU info
				self.new_cpu[i]=sensors.cpu_get_load(i)

				self.cpu_load[i] = (self.new_cpu[i]-self.old_cpu[i])/self.update_interval
				
				self.old_cpu[i] = self.new_cpu[i]
				try:
					if self.cpu_load[i] > 99: self.cpu_load[i] = 99
					elif self.cpu_load[i] < 0: self.cpu_load[i]=0
				except : pass

		if self.show_mem: self.mem_used = sensors.mem_get_usage()
		if self.show_swap: self.swap_used = sensors.mem_get_usedswap()
		if self.show_ip: self.ip = sensors.net_get_ip()
		if self.show_updown: 
			self.up = sensors.net_get_updown()[0]
			self.down = sensors.net_get_updown()[1]
			self.upload = (self.up - self.old_up)/self.update_interval
			self.download = (self.down - self.old_down)/self.update_interval
			self.old_up = self.up
			self.old_down = self.down
		if self.show_disks:
			self.disks = sensors.disk_get_disk_list()
		if self.show_bat_wir:
			self.bat_list = sensors.bat_get_battery_list()
			if self.bat_list:
				self.bat_data = sensors.bat_get_data(self.bat_list[0])
				try:
					self.bat_load = (self.bat_data[1]*100)/self.bat_data[2]
				except: self.bat_load = 0
				self.bat_rate = self.bat_data[5]
				self.bat_state = self.bat_data[3]
			self.wire_list = sensors.wir_get_interfaces()
			if self.wire_list:
				self.wire_data = sensors.get_wireless_stats(self.wire_list[0])


	def update (self):
		self.get_variables()
		self.redraw_canvas()
		return True # keep running this event	

	def on_map(self):
		if not self.timer:
			self.timer = gobject.timeout_add( self.update_interval*1000, self.update)
		self.update()

	def on_unmap(self):
		if self.timer:
			gobject.source_remove(self.timer)
			self.timer = None

	def on_drop (self, x, y, sel_data, timestamp):
		"""Called when a selection is dropped on this Screenlet."""
		return False
		
	def on_focus (self, event):
		"""Called when the Screenlet's window receives focus."""
		pass
	
	def on_hide (self):
		"""Called when the Screenlet gets hidden."""
		pass

	def on_init (self):
		"""Called when the Screenlet's options have been applied and the 
		screenlet finished its initialization. If you want to have your
		Screenlet do things on startup you should use this handler."""
		print 'i just got started'
		# add  menu items from xml file

		print self.date
		#self.add_default_menuitems(DefaultMenuItem.XML)
		# add menu item
		#self.add_menuitem("at_runtime", "A")
		# add default menu items
		self.add_default_menuitems()
		
		self.height = self.newheight

	def on_key_down (self, keycode, keyvalue, event=None):
		"""Called when a key is pressed within the screenlet's window."""
		pass
	
	def on_load_theme (self):
		"""Called when the theme is reloaded (after loading, before redraw)."""
		pass
	
	def on_menuitem_select (self, id):
		"""Called when a menuitem is selected."""
		pass
	
	def on_mouse_down (self, event):
		"""Called when a buttonpress-event occured in Screenlet's window. 
		Returning True causes the event to be not further propagated."""
		return False
	
	def on_mouse_enter (self, event):
		"""Called when the mouse enters the Screenlet's window."""
	        #self.theme.show_tooltip("this is a tooltip , it is set to shows on mouse hover",self.x+self.mousex,self.y+self.mousey)

		
	def on_mouse_leave (self, event):
		"""Called when the mouse leaves the Screenlet's window."""
	        #self.theme.hide_tooltip()


	def on_mouse_move(self, event):
		"""Called when the mouse moves in the Screenlet's window."""

		pass

	def on_mouse_up (self, event):
		"""Called when a buttonrelease-event occured in Screenlet's window. 
		Returning True causes the event to be not further propagated."""
		return False
	
	def on_quit (self):
		"""Callback for handling destroy-event. Perform your cleanup here!"""

		return True
		
	def on_realize (self):
		""""Callback for handling the realize-event."""
	
	def on_scale (self):
		"""Called when Screenlet.scale is changed."""
		pass
	
	def on_scroll_up (self):
		"""Called when mousewheel is scrolled up (button4)."""
		pass

	def on_scroll_down (self):
		"""Called when mousewheel is scrolled down (button5)."""
		pass
	
	def on_show (self):
		"""Called when the Screenlet gets shown after being hidden."""
		pass
	
	def on_switch_widget_state (self, state):
		"""Called when the Screenlet enters/leaves "Widget"-state."""
		pass
	
	def on_unfocus (self, event):
		"""Called when the Screenlet's window loses focus."""
		pass
	
	def on_draw (self, ctx):
		self.get_variables()
		# if theme is loaded
		#self.font =  self.font.strip(' ')
		if self.font.find(' ') != -1:
			self.font1 =  self.font.strip().split(' ')[0]
			try : self.fontsize = int(self.font.strip().split(' ')[2])
			except:
				try: self.fontsize = int(self.font.strip().split(' ')[1])
				except : self.fontsize = 10
		if self.theme:
			# set scale rel. to scale-attribute
			ctx.scale(self.scale, self.scale)
			if self.show_logo:
				if os.path.exists (self.get_screenlet_dir() + '/themes/'+ self.theme_name + '/' + self.distroshort.lower() + '.svg') or os.path.exists (self.get_screenlet_dir() + '/themes/'+ self.theme_name + '/' +self.distroshort.lower() + '.png'):
					ctx.translate(0,20)
					try:
						self.theme.render(ctx,self.distroshort.lower())
					except:pass
					ctx.translate(0,-20)
			#DRAW BACKGROUND ALWAYS
			if self.show_frame:
				ctx.set_source_rgba(0, 0, 0,0.7)	
				self.draw_rectangle(ctx,0,0,self.width,self.height,False)
				ctx.set_source_rgba(89/255, 89/255, 89/255,0.43)	
				ctx.translate (1,1)
				self.draw_rectangle(ctx,0,0,self.width-2,self.height-2,False)

				ctx.set_source_rgba(229/255, 229/255, 229/255,76/255)	
				ctx.translate (1,1)
				self.draw_rectangle(ctx,0,0,self.width-2,self.height-2)
				ctx.translate (-2,-2)
			
			#DRAW BACKGROUND USER SELECTED
			if self.use_bg_image:
				if len(self.image_filename) > 0: 
				# replace the /usr in the filename's path with the correct prefix
					self.draw_scaled_image(ctx,0,0, self.image_filename, self.width, self.height)
				else:
					self.draw_scaled_image(ctx,0,0, self.theme.path + "/bg.png", self.width, self.height)
					
			ctx.set_source_rgba(self.color_background[0], self.color_background[1], self.color_background[2],self.color_background[3])	
			self.draw_rectangle(ctx,0,0,self.width,self.height)
			ctx.set_source_rgba(self.color_text[0], self.color_text[1], self.color_text[2],self.color_text[3])
			#DRAW TEXT
			m = self.starty
			m = m + 15
			if self.show_time:
				self.draw_text(ctx, ' ' + self.time, 0, m, self.font1, self.fontsize + 8,  self.width,pango.ALIGN_CENTER)
				m = m + 30
			if self.show_date:
				self.draw_text(ctx, self.date, 0, m, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
				m = m + 40
			if self.show_username:

				self.draw_text(ctx, self.username + '@' + self.hostname, 0, m, self.font1, self.fontsize + 1,  self.width,pango.ALIGN_CENTER)
				m = m + 25
			if self.show_distro:
				self.draw_text(ctx, self.distro, 0, m, self.font1, self.fontsize + 1,  self.width,pango.ALIGN_CENTER)
				m = m + 30
			if self.show_kernel:
				self.draw_text(ctx, 'kernel: ' + self.kernel, 0, m, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
				m = m + 40
			if self.show_cpuname:
				self.draw_text(ctx, self.cpu_name, 0, m, self.font1, self.fontsize - 2,  self.width,pango.ALIGN_CENTER)
				m = m + 35
			if self.show_cpus:			
				ctx.save()
				if self.cpu_nb == 1: #For a single CPU show meter at centre 
					ctx.save()
					ctx.translate(65,m)
					ctx.set_source_rgba(self.color_background[0], self.color_background[1], self.color_background[2],0.2)	
					a = (40* self.cpu_load[0])/100
					self.draw_rounded_rectangle(ctx,0,0,10,50,50)
					ctx.translate(5,5)
					ctx.translate (0,40-a)
					ctx.set_source_rgba(self.color_graph[0], self.color_graph[1], self.color_graph[2],self.color_graph[3])	
					self.draw_rectangle(ctx,0,0,40,a)
					ctx.translate(75,-5-(40-a))
					ctx.set_source_rgba(self.color_text[0], self.color_text[1], self.color_text[2],self.color_text[3])
					self.draw_text(ctx, _('CPU') , -75-70, 0, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
					self.draw_text(ctx,str(self.cpu_load[0])+ '%', -75-70, 30, self.font1, self.fontsize - 2,  self.width,pango.ALIGN_CENTER)

					ctx.restore()
					m = m + 40
				if self.cpu_nb >= 2:  #For multiple CPUS, show 2 per row up to 4. 
					ctx.translate(25,m)
					a = (40* self.cpu_load[0])/100
					ctx.set_source_rgba(self.color_background[0], self.color_background[1], self.color_background[2],0.2)	
					ctx.save()
					self.draw_rounded_rectangle(ctx,0,0,10,50,50)
					ctx.translate(5,5)
					ctx.translate (0,40-a)
					ctx.set_source_rgba(self.color_graph[0], self.color_graph[1], self.color_graph[2],self.color_graph[3])	
					self.draw_rectangle(ctx,0,0,40,a)
					ctx.translate(75,-5-(40-a))
					ctx.restore()
					ctx.set_source_rgba(self.color_text[0], self.color_text[1], self.color_text[2],self.color_text[3])
					self.draw_text(ctx, _('CPU 1') , -65, 0, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
					self.draw_text(ctx,str(self.cpu_load[0])+ '%', -65, 30, self.font1, self.fontsize - 2,  self.width,pango.ALIGN_CENTER)
		
					ctx.translate(75,0)
					a = (40* self.cpu_load[1])/100
					ctx.set_source_rgba(self.color_background[0], self.color_background[1], self.color_background[2],0.2)
					ctx.save()
					self.draw_rounded_rectangle(ctx,0,0,10,50,50)
					ctx.translate(5,5)
					ctx.translate (0,40-a)
					ctx.set_source_rgba(self.color_graph[0], self.color_graph[1], self.color_graph[2],self.color_graph[3])
					self.draw_rectangle(ctx,0,0,40,a)
					ctx.restore()
					ctx.set_source_rgba(self.color_text[0], self.color_text[1], self.color_text[2],self.color_text[3])
					self.draw_text(ctx, _('CPU 2') , -65, 0, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
					self.draw_text(ctx,str(self.cpu_load[1])+ '%' , -65, 30, self.font1, self.fontsize - 2,  self.width,pango.ALIGN_CENTER)
					#ctx.restore()
					m = m + 40
					d = 4
					if self.cpu_nb == 4:#self.cpu_nb
						ctx.save()
						m = m +20   
						ctx.translate (-75,60)  #-ve value to align with CPU1
						a = (40* self.cpu_load[2])/100
						ctx.set_source_rgba(self.color_background[0], self.color_background[1], self.color_background[2],0.2)	
						ctx.save()
						self.draw_rounded_rectangle(ctx,0,0,10,50,50)
						ctx.translate(5,5)
						ctx.translate (0,40-a)
						ctx.set_source_rgba(self.color_graph[0], self.color_graph[1], self.color_graph[2],self.color_graph[3])	
						self.draw_rectangle(ctx,0,0,40,a)
						ctx.translate(75,-5-(40-a))
						ctx.restore()
						ctx.set_source_rgba(self.color_text[0], self.color_text[1], self.color_text[2],self.color_text[3])
						self.draw_text(ctx, _('CPU 3') , -65, 0, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
						self.draw_text(ctx,str(self.cpu_load[2])+ '%', -65, 30, self.font1, self.fontsize - 2,  self.width,pango.ALIGN_CENTER)

						ctx.translate(75,0)
						a = (40* self.cpu_load[3])/100
						ctx.set_source_rgba(self.color_background[0], self.color_background[1], self.color_background[2],0.2)
						ctx.save()
						self.draw_rounded_rectangle(ctx,0,0,10,50,50)
						ctx.translate(5,5)
						ctx.translate (0,40-a)
						ctx.set_source_rgba(self.color_graph[0], self.color_graph[1], self.color_graph[2],self.color_graph[3])
						self.draw_rectangle(ctx,0,0,40,a)
						ctx.restore()
						ctx.set_source_rgba(self.color_text[0], self.color_text[1], self.color_text[2],self.color_text[3])
						self.draw_text(ctx, _('CPU 4') , -65, 0, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
						self.draw_text(ctx,str(self.cpu_load[3])+ '%' , -65, 30, self.font1, self.fontsize - 2,  self.width,pango.ALIGN_CENTER)
#						self.draw_rounded_rectangle(ctx,0,0,10,50,50)
						ctx.restore()
						m = m + 40
				ctx.restore()
				m = m + 20
			else: m = m + 10
			if self.show_load:
				ctx.set_source_rgba(self.color_text[0], self.color_text[1], self.color_text[2],self.color_text[3])
				self.draw_text(ctx, _('Load : ') + self.avg_load, 0, m, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
				m = m +20
			if self.show_mem:
				ctx.save()
				ctx.set_source_rgba(self.color_text[0], self.color_text[1], self.color_text[2],self.color_text[3])
				self.draw_text(ctx, _('Ram ') + str(self.mem_used) + '%', 0, m, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
				ctx.translate(0,m)
				ctx.translate(20,15)
				ctx.set_source_rgba(self.color_background[0], self.color_background[1], self.color_background[2],0.2)
				self.draw_rectangle(ctx,0,0,140,5)
				ctx.set_source_rgba(self.color_graph[0], self.color_graph[1], self.color_graph[2],self.color_graph[3])
				self.draw_rectangle(ctx,0,0,(self.mem_used*100)/140,5)
				ctx.translate(-20,-15)
				ctx.restore()
				m = m +20
			if self.show_swap:
				ctx.save()
				ctx.set_source_rgba(self.color_text[0], self.color_text[1], self.color_text[2],self.color_text[3])
				self.draw_text(ctx,_('Swap ') + str(self.swap_used)+ "%", 0, m, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
				ctx.translate(0,m)
				ctx.translate(20,15)
				ctx.set_source_rgba(self.color_background[0], self.color_background[1], self.color_background[2],0.2)
				self.draw_rectangle(ctx,0,0,140,5)
				ctx.set_source_rgba(self.color_graph[0], self.color_graph[1], self.color_graph[2],self.color_graph[3])
				self.draw_rectangle(ctx,0,0,(self.swap_used*100)/140,5)
				ctx.translate(-20,-15)
				ctx.restore()
				m = m +30
			if self.show_ip:
				ctx.set_source_rgba(self.color_text[0], self.color_text[1], self.color_text[2],self.color_text[3])
				self.draw_text(ctx, _('IP : ') + self.ip, 0, m, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
				m = m +25
			if self.show_updown:
				self.draw_text(ctx, _('Upload - ') + str(decimal.Decimal(str(self.upload)).quantize(decimal.Decimal(10)**-1)) + _(' KB/sec'), 0, m, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
				m = m +20

				self.draw_text(ctx, _('Download - ') + str(decimal.Decimal(str(self.download)).quantize(decimal.Decimal(10)**-1)) + _(' KB/sec'), 0, m, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
				m = m +30

			if self.show_disks:
				ctx.save()
				for i in self.disks:
					a = sensors.disk_get_usage(i)
					if a is not None:
						ctx.set_source_rgba(self.color_text[0], self.color_text[1], self.color_text[2],self.color_text[3])
						self.draw_text(ctx,a[5]+  ' ' + a[4], 0, m, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)
						ctx.translate(0,m)
						ctx.translate(20,15)
						ctx.set_source_rgba(self.color_background[0], self.color_background[1], self.color_background[2],0.2)
						self.draw_rectangle(ctx,0,0,140,5)
						ctx.set_source_rgba(self.color_graph[0], self.color_graph[1], self.color_graph[2],self.color_graph[3])

						self.draw_rectangle(ctx,0,0,(int(a[4].replace('%',''))*140)/100,5)
						ctx.translate(-20,-15)
						m = m +20
						ctx.restore()
						ctx.save()
				m = m + 10
				ctx.restore()

			if self.show_bat_wir:
				
				if self.bat_list and self.bat_data !=[] and self.wire_list:
					ctx.save()
					ctx.translate(25,m)
					a = (40*self.bat_load)/100
	
					ctx.set_source_rgba(self.color_background[0], self.color_background[1], self.color_background[2],0.2)	
					ctx.save()
					self.draw_rounded_rectangle(ctx,0,0,10,50,50)

					ctx.translate(5,5)
					ctx.translate (0,40-a)
					ctx.set_source_rgba(self.color_graph[0], self.color_graph[1], self.color_graph[2],self.color_graph[3])		
					self.draw_rectangle(ctx,0,0,40,a)
					ctx.translate(75,-5-(40-a))
					ctx.restore()
					ctx.set_source_rgba(self.color_text[0], self.color_text[1], self.color_text[2],self.color_text[3])
					self.draw_text(ctx, self.bat_list[0] , -65, 0, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)

					self.draw_text(ctx,str(self.bat_load) + '%', -65, 30, self.font1, self.fontsize - 2,  self.width,pango.ALIGN_CENTER)

					ctx.translate(75,0)



					a = (40* int(self.wire_data['percentage']))/100

					ctx.set_source_rgba(self.color_background[0], self.color_background[1], self.color_background[2],0.2)
					ctx.save()
					self.draw_rounded_rectangle(ctx,0,0,10,50,50)

					ctx.translate(5,5)
					ctx.translate (0,40-a)
					ctx.set_source_rgba(self.color_graph[0], self.color_graph[1], self.color_graph[2],self.color_graph[3])
					self.draw_rectangle(ctx,0,0,40,a)
					ctx.restore()
					ctx.set_source_rgba(self.color_text[0], self.color_text[1], self.color_text[2],self.color_text[3])
					self.draw_text(ctx, self.wire_list[0] , -65, 0, self.font1, self.fontsize,  self.width,pango.ALIGN_CENTER)

					self.draw_text(ctx,str( int(self.wire_data['percentage']))+ '%' , -65, 30, self.font1, self.fontsize - 2,  self.width,pango.ALIGN_CENTER)
					b=0
					if str(self.bat_state) == 'discharging':
						b=5
						bat_remaining = float(self.bat_current)/float(self.bat_rate)
						ctx.translate(-35,15)
						self.draw_text(ctx,str(int(bat_remaining)) + _(' hours ') + str(int(bat_remaining * 60 % 60)) + _(' minutes'), -65, 30, self.font1, self.fontsize-2,self.width,pango.ALIGN_CENTER)
					ctx.restore()
					m=m+b	
				m = m + 60
			if self.show_processes:
				self.draw_text(ctx,str( sensors.process_get_top().replace(' ','-')) , 0, m, self.font1, self.fontsize - 3,  self.width -10,pango.ALIGN_CENTER)
				m = m + 150
			if self.show_uptime:
				self.draw_text(ctx,_('Uptime: ') + str( sensors.sys_get_uptime()) , 0, m, self.font1, self.fontsize +5,  self.width -10,pango.ALIGN_CENTER)
			m = m + 40
			if self.height != m and self.expand == False:
				self.height = m
#							ctx.translate(-20,-15)self.draw_text(ctx, self.theme_name, 0, 50, self.font1, self.fontsize,  self.width,pango.ALIGN_LEFT)

#			self.draw_text(ctx, 'mouse x ' + str(self.mousex ) + ' \n mouse y ' + str(self.mousey ) , 0, 170, self.font1, self.fontsize,  self.width,pango.ALIGN_LEFT)


			# render svg-file

			# render png-file
			#ctx.set_source_surface(self.theme['example-test.png'], 0, 0)
			#ctx.paint()
	
	def on_draw_shape (self, ctx):
		if self.theme:
			ctx.set_source_rgba(0, 0, 0,1)	
			self.draw_rectangle(ctx,0,0,self.width,self.height)
	
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
	# create new session
	import screenlets.session
	screenlets.session.create_session(SysmonitorScreenlet)

