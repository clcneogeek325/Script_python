#!/usr/bin/env python

#
# TrashScreenlet (C) 2008 Natan Yellin
# Based on the original screenlet (C) 2007 Helder Fraga
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

import screenlets
from screenlets.options import  BoolOption,IntOption
import cairo
import datetime
import pango
import os
import gtk
import gobject
import urllib

# use gettext for translation
import gettext

_ = screenlets.utils.get_translator(__file__)

def tdoc(obj):
	obj.__doc__ = _(obj.__doc__)
	return obj

@tdoc
class TrashScreenlet(screenlets.Screenlet):
	"""A Screenlet that shows information about your trash folder"""
	
	# default meta-info for Screenlets
	__name__ = 'TrashScreenlet'
	__version__ = '0.2.2+'
	__author__ = 'Helder Fraga aka Whise'
	__desc__ = __doc__
	
	TRASH_DIRS = [os.environ['HOME'] + '/.local/share/Trash/files',
		os.environ['HOME'] + '/.Trash']
	
	style = False
	show_count = True
	auto_empty = False
	auto_empty_size = 1000
	if os.path.exists(os.environ['HOME'] +'/.local/share/Trash/files') and os.path.isdir(os.environ['HOME'] +'/.local/share/Trash/files'):
		trash_folder = os.environ['HOME'] +'/.local/share/Trash/files'
	else:
		trash_folder = os.environ['HOME'] + '/.Trash'
	item_count = 0

	def __init__(self, **keyword_args):
		screenlets.Screenlet.__init__(self, width=128, height=160,
			drag_drop=True, **keyword_args)
		
		# set default theme name
		self.theme_name = "default"
		
		# init other attributes
		self.item_count = 0
		
		self.add_options_group(_('Options'), _('Options'))
		self.add_option(BoolOption(_('Options'), 'style', False, 
			_('Use gtk style'), _('Use gtk icon'), callback=self.redraw_canvas_and_update_shape))	
		self.add_option(BoolOption(_('Options'), 'show_count', True, 
			_('Show item count'), _('Show item count')))	
		self.add_option(BoolOption(_('Options'), 'auto_empty', False, 
			_('Auto empty trash'),
			_('Automatically empty trash when the limit is exceded')))
		self.add_option(IntOption(_('Options'), 'auto_empty_size', 1000,
			_('Auto empty limit'),  _('Automatically empty trash when there\
			are this many items in the trash. (Only if the above option\
			is checked.)'), min=1,max = 100000))
		
		# TODO: Monitor the trash directories and call self.update when
		# they change instead of calling self.update once every second
		self.update()
		self.refresh_timeout = gobject.timeout_add(1000, self.update)
		
		# Redraw and update the shape if the icon theme changes
		# TODO: Only redraw if self.style is True
#		screenlets.drawing.icon_theme.connect("changed",
#			self.redraw_canvas_and_update_shape)

	def on_init (self):
		print "Screenlet has been initialized."
		# add default menuitems
		self.add_menuitem("Empty", _("Empty Trash"))
		self.add_menuitem("Open", _("Examine Trash"))
		self.add_default_menuitems()

	# callback for when an item is dragged and then dropped on the applet
	def on_drop (self, x, y, sel_data, timestamp):
		# If the trash folder doesn't exist then just return
		# TODO: Create the trash folder when it doesn't exist.
		if self.trash_folder is None:
			screenlets.show_error(None, _('File(s) could not be moved to trash.'))
			return
			
		filename = ''
		
		# get text from selection data
		try:
			txt = unicode.encode(sel_data.get_text(), 'utf-8')
		except:
			txt = sel_data.get_text()
		
		txta = urllib.unquote(txt)
		txta = str(txta).split('\n')
		
		for txt in txta:
			if txt and txt != '':
				# if it is a filename, use it
				if txt.startswith('file://'):
					filename = txt[7:]
				else:
					screenlets.show_error(self, _('Invalid string: %s.') % txt)
			else:
				# else get uri-part of selection
				uris = sel_data.get_uris()
				if uris and len(uris)>0:
					filename = uris[0][7:]
					
			if filename != '':
				if self.trash_folder==self.TRASH_DIRS[0]:
					infofile=os.environ['HOME'] + '/.local/share/Trash/info/'+ os.path.basename(filename)+'.trashinfo'
					count=1
					while os.path.exists(infofile):
						count=count+1
						infofile=os.environ['HOME'] + '/.local/share/Trash/info/'+ os.path.basename(filename)+'.'+str(count)+'.trashinfo'
					f=open(infofile, 'w')
					f.write('[Trash Info]\n')
					f.write('Path='+filename+'\n')
					now=datetime.datetime.now()
					f.write('DeletionDate='+ str(now.strftime("%Y-%m-%dT%H:%M:%S")))
					f.close()
				if count>1:
					os.system('mv ' + chr(34)+ filename + chr(34) + ' ' + chr(34) + self.trash_folder + '/' + os.path.basename(filename)+'.'+str(count) + chr(34))
				else:
					os.system('mv ' + chr(34)+ filename + chr(34) + ' ' + self.trash_folder)
				filename  = ''			
	
	def update(self):
		# find the correct trash directory or return if no trash directory exists
		if os.path.exists(self.TRASH_DIRS[0]) and os.path.isdir(self.TRASH_DIRS[0]):
			self.trash_folder = self.TRASH_DIRS[0]
		elif os.path.exists(self.TRASH_DIRS[1]) and os.path.isdir(self.TRASH_DIRS[1]):
			self.trash_folder = self.TRASH_DIRS[1]
		else:
			self.trash_folder = None
			self.item_count = 0
			return
		
		old_item_count = self.item_count
		self.item_count = len(os.listdir(self.trash_folder))
		
		# if the auto empty feature is enabled then check if the trash needs to be emptied
		if self.auto_empty and self.item_count >= self.auto_empty_size:
			if self.trash_folder==self.TRASH_DIRS[0]:
				os.system('rm -rf ' + os.environ['HOME'] + '/.local/share/Trash/info/*')
			os.system('rm -rf ' + self.trash_folder + '/*')
			os.system('rm -rf ' + self.trash_folder + '/*.*')
			os.system('rm -rf ' + self.trash_folder + '/.*')
			self.item_count = len(os.listdir(self.trash_folder))
		
		# if the number of items in the trash is drawn on the icon then check if it changed
		if self.show_count and self.item_count != old_item_count:
			self.redraw_canvas()
		return True

	def on_mouse_down(self, event):
		if event.type == gtk.gdk._2BUTTON_PRESS: 
			if event.button == 1:
				os.system('xdg-open trash:/// &')
		
	def menuitem_callback(self, widget, id):
		screenlets.Screenlet.menuitem_callback(self, widget, id)
		if id=="Empty":
			if self.trash_folder is None:
				screenlets.show_error(None, _("No trash folder found."))
			elif screenlets.show_question(self,_('Do you want to permanently remove all the items in your Trash folder?')):
				if self.trash_folder==self.TRASH_DIRS[0]:
					os.system('rm -rf ' + os.environ['HOME'] + '/.local/share/Trash/info/*')
				os.system('rm -rf ' + self.trash_folder + '/*')
				os.system('rm -rf ' + self.trash_folder + '/*.*')
				os.system('rm -rf ' + self.trash_folder + '/.*')
				self.update()
		elif id=="Open":
			os.system('xdg-open trash:/// &')

	def on_draw(self, ctx):
		if self.theme:
			ctx.set_operator(cairo.OPERATOR_OVER)
			ctx.scale(self.scale, self.scale)
			
			# find the right icon name to use
			if self.item_count == 0:
				ico = 'user-trash-empty'
				if self.style and not self.check_for_icon(ico):
					ico = 'emptytrash'
			else:
				ico = 'user-trash-full'
				if self.style and not self.check_for_icon(ico):
					ico = 'trashcan_full'
			
			# draw the icon
			if self.style == True:
				self.draw_icon(ctx, 0, 0, ico, 128, 128)
			else:
				self.theme.render(ctx, ico)
			
			# draw the item count
			if self.show_count:
				ctx.set_source_rgba(1,1,1,0.65)
				self.draw_rounded_rectangle(ctx,20,128,5,self.width-40,23)
				ctx.set_source_rgba(0,0,0,1)
				#item counter
				self.draw_text(ctx,str(self.item_count) + _(' items'), 0, 132,
					"FreeSans", 10, self.width, pango.ALIGN_CENTER)
			
	def on_draw_shape(self,ctx):
		if self.theme:
			self.on_draw(ctx)

if __name__ == "__main__":
	import screenlets.session
	screenlets.session.create_session(TrashScreenlet)
