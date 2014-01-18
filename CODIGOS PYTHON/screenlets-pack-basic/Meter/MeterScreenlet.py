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

#SensorScreenlet (c) Whise <helder.fraga@hotmail.com>

import screenlets
from screenlets import sensors
from screenlets.options import FloatOption, BoolOption, StringOption, IntOption, ColorOption
import cairo
import pango
import sys
import gobject
#use gettext for translation
import gettext

_ = screenlets.utils.get_translator(__file__)

def tdoc(obj):
	obj.__doc__ = _(obj.__doc__)
	return obj

@tdoc
class MeterScreenlet(screenlets.Screenlet):
	"""Sensors Screenlet."""

	# default meta-info for Screenlets
	__name__ = 'MeterScreenlet'
	__version__ = '0.1.2+'
	__author__ = 'Helder Fraga aka Whise ,default theme by RYX'
	__desc__ = __doc__




	__timeout = None

	# settings
	update_interval = 1
	nb_points=50
	show_text = True
	show_graph = True
	text_prefix = '<span size="xx-small" rise="10000">% </span><b>'
	text_suffix = '</b>'
	loads=[]
	old_idle=0
	linear = ''
	color_high = (1,0,0,1)
	color_medium =(0, 0, 1, 1)
	color_low = (0, 1, 0, 1)
	graph_type = 'Graph'
	sensor_list = []
	sensor = 'CPU0'
	load = 0
	old_cpu = 0
	new_cpu = 0
	wire_list = []
	wire_data = []
	background_color = (0,0,0, 0.8)

	label = "CPU0"

	loads=[]
	old_idle=0
	nb_points=50
	show_graph = True
	text_prefix = '<span size="xx-small" rise="10000">% </span><b>'
	text_suffix = '</b>'
	loads=[]
	old_idle=0
	linear = ''
	color_high = (1,0,0,1)
	color_medium =(0, 0, 1, 1)
	color_low = (0, 1, 0, 1)
	graph_type = 'Graph'
	sensor_list = []
	sensor = 'CPU0'
	load = 0
	old_cpu = 0
	new_cpu = 0
	wire_list = []
	wire_data = []
	background_color = (0,0,0, 0.8)

	
	# constructor
	def __init__(self,**keyword_args):
		screenlets.Screenlet.__init__(self, width=100, height=100, 
			uses_theme=True, **keyword_args)
		
		self.loads=[]
		self.old_idle=0
		self.nb_points=50
		self.show_graph = True
		self.text_prefix = '<span size="xx-small" rise="10000">% </span><b>'
		self.text_suffix = '</b>'
		self.loads=[]
		self.old_idle=0
		self.linear = ''
		self.color_high = (1,0,0,1)
		self.color_medium =(0, 0, 1, 1)
		self.color_low = (0, 1, 0, 1)
		self.graph_type = 'Graph'
		self.sensor_list = []
		self.load = 0
		self.old_cpu = 0
		self.new_cpu = 0
		self.wire_list = []
		self.wire_data = []
		
		for i in range(self.nb_points):
			self.loads.append(0)
		
		if self.sensor_list ==[]:
			for i in range (0,sensors.cpu_get_nb_cpu()+1): 
				self.sensor_list.append(_('CPU') + str(i))

			self.sensor_list.append(_('RAM'))
			self.sensor_list.append(_('SWAP'))
			
			for bat in sensors.bat_get_battery_list():
				if bat:
					self.sensor_list.append(str(bat))
			for i in sensors.disk_get_disk_list():
				self.sensor_list.append(str(i))
			
			if sensors.sensors_get_sensors_list():
				for i in sensors.sensors_get_sensors_list():
					self.sensor_list.append(str(i))
					
			self.wire_list = sensors.wir_get_interfaces()
			
			if self.wire_list !=[]:
				self.sensor_list.append(_('Wifi ')+ self.wire_list[0])
		
		# set default theme
		self.theme_name = "default"
		
		# add settings
		self.add_options_group(_('Sensors'), _('CPU-Graph specific options'))

		self.add_option(BoolOption(_('Sensors'), 'show_text',
			True, _('Show Text'), _('Show the text on the CPU-Graph.')))

		self.add_option(StringOption(_('Sensors'), 'sensor', _('CPU0'), _('Sensor to Display'),
			'', choices=self.sensor_list))
			
		self.add_option(StringOption(_('Sensors'), 'label',
			'', _('Label to Display'),
			_('Leave empty if you want to display name of sensor instead of custom name')))
			
		self.add_option(ColorOption(_('Sensors'),'background_color', 
			(0,0,0, 0.8), _('Back color(only with default theme)'), 'only works with default theme'))
		
		# add default menutimes
		self.add_default_menuitems()

		# init the timeout function
		self.__timeout = gobject.timeout_add(1000, self.update)

	# attribute-"setter", handles setting of attributes
	def __setattr__(self, name, value):
		# important: call Screenlet.__setattr__ in baseclass
		screenlets.Screenlet.__setattr__(self, name, value)
		
		# check for this Screenlet's attributes, we are interested in:
		if name == "nb_points":
			if value > 1:
				if len(self.loads)> value:
					self.loads=self.loads[len(self.loads)-value:]
				elif len(self.loads)< value:
					for i in range(value-len(self.loads)):
						self.loads.insert(0,0)
				self.__dict__['nb_points'] = value
			else:
				# TODO: raise exception!!!
				self.__dict__['nb_points'] = 2

	# timeout-function
	def update(self):
		if self.sensor.startswith(_('CPU')):
			self.new_cpu=sensors.cpu_get_load(int(self.sensor[3]))

			self.load = int(self.new_cpu-self.old_cpu)
			
			self.old_cpu = self.new_cpu
		elif self.sensor.startswith(_('RAM')):
			self.load = sensors.mem_get_usage()

		elif self.sensor.startswith(_('SWAP')):
			self.load = sensors.mem_get_usedswap()

		elif self.sensor.startswith(_('BAT')) or self.sensor.startswith('C1'): #temporary workaround for batteries in HP NC4200 TODO: do not use name of sensor to recognize type?
			bat_data = sensors.bat_get_data(self.sensor)
			try:
				self.load = (bat_data[1]*100)/bat_data[2]
			except: self.load = 0
		elif self.sensor.endswith('C'):

			self.sensor = str(self.sensor.split(':')[0]) + ':' + str(sensors.sensors_get_sensor_value(self.sensor.split(':')[0]))
			self.load = 0
		elif self.sensor.endswith('RPM'):
			self.sensor = str(self.sensor.split(':')[0]) + ':' +str(sensors.sensors_get_sensor_value(self.sensor.split(':')[0]))
			self.load = 0
		elif self.sensor.endswith('V'):
			self.sensor = str(self.sensor.split(':')[0]) + ':' +str(sensors.sensors_get_sensor_value(self.sensor.split(':')[0]))
			self.load = 0
		elif self.sensor.endswith(_('Custom Sensors')):
			pass			
		elif self.sensor.startswith(_('Wifi')):
			if self.wire_list != []:
				self.wire_data = sensors.wir_get_stats(self.wire_list[0])
				
				a = str(self.wire_data['essid']).find('off/any')
				if a != -1:
					self.sensor = _('Wifi ') + str(self.wire_list[0])
				else:
					self.sensor = _('Wifi ')  + str(self.wire_data['essid'])
				self.load = int(str(self.wire_data['percentage']).replace('%',''))
		elif self.sensor and self.sensor in sensors.disk_get_disk_list():
			# only get here when requested sensor is in the list of available disks
 			self.load = int(sensors.disk_get_usage(self.sensor)[4].replace('%',''))
		else:
			try:
				self.sensor = str(self.sensor.split(':')[0]) + ':' + str(sensors.sensors_get_sensor_value(self.sensor.split(':')[0]))
			except:			
				pass
			self.load = 0
		
		if self.load >= 100:
			self.load = 99
		elif self.load < 0:
			self.load=0

		self.redraw_canvas()
		return True

	def on_draw(self, ctx):
		del(self.loads[0])
		self.loads.append(self.load)
		# set size
		ctx.scale(self.scale, self.scale)
		# draw bg (if theme available)
		ctx.set_operator(cairo.OPERATOR_OVER)
		if self.theme:
			ctx.set_source_rgba(*self.background_color)
			if self.theme_name == 'default':self.draw_rounded_rectangle(ctx,6.3,7,9,84.1,80.1)
			self.theme.render(ctx, 'cpumeter-bg')
			
			# draw text
			if len(str(self.load))==1:
				self.load = "0" + str(self.load)
			ctx.set_source_rgba(1, 1, 1, 0.9)
			if self.sensor.endswith('RPM') or self.sensor.endswith('C') or self.sensor.endswith('V')or self.sensor.find(':') != -1:
				if self.label:
					upper_line = self.label
				else:
					upper_line = str(self.sensor.split(':')[0])[:9]
				text = '<small><small><small><small>' + upper_line+'</small></small></small></small>\n'+str(self.sensor.split(':')[1])
			else:
				if self.label:
					upper_line = self.label
				else:
					upper_line = self.sensor[:9]
				text = '<small><small><small><small>' +upper_line +'</small></small></small></small>\n'+self.text_prefix + str(self.load) + self.text_suffix
	
			h = (float(self.load) / 100.0) * 70.0
			ctx.save()
			ctx.rectangle(20, 10+(70-h), 60, h)
			ctx.clip()
			ctx.new_path()
			self.theme.render(ctx, 'cpumeter-graph')
			ctx.restore()
			# draw text
			if self.show_text:
				self.draw_text(ctx,text, 15, 20, 'FreeSans', 25,  self.width,pango.ALIGN_LEFT)
			self.theme.render(ctx, 'cpumeter-glass')

	def on_draw_shape(self,ctx):
		if self.theme:
			ctx.scale(self.scale, self.scale)
			self.draw_rectangle(ctx,0,0,self.width,self.height)
			self.on_draw(ctx)


# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
	import screenlets.session
	screenlets.session.create_session(MeterScreenlet)
