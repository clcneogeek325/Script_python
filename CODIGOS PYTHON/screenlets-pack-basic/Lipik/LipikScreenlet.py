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

#  LipikScreenlet (c) Guido Tabbernuk 2010 <boamaod@gmail.com>
#  NotesScreenlet (c) RYX (aka Rico Pfaus) 2007 <ryx@ryxperience.com>
#
# INFO:
# - a simple sticky note application
# 
# TODO:
# - try to get informed about end of begin_move_drag-operation
# - separate shadow into its own theme and add distance when picked up
# - maybe use another "paper" for the dragged-state
# - randomly rotate notes after they were "picked up"
# - tomboy/gnote export

import screenlets
import datetime
from screenlets.options import IntOption, BoolOption, StringOption
from screenlets.options import FontOption, ColorOption

import gtk
import Image
import os
from gtk import gdk
import cairo
import pango
import sys
import random

import uuid

import dbus, gobject, dbus.glib

# use gettext for translation
import gettext

_ = screenlets.utils.get_translator(__file__)

def tdoc(obj):
	obj.__doc__ = _(obj.__doc__)
	return obj

@tdoc
class LipikScreenlet (screenlets.Screenlet):
	"""A simple and usable sticky notes Screenlet with theming and fully functional in-note editing, depends on 'python-numpy' package"""
	
	# default meta-info for Screenlets
	__name__	= 'LipikScreenlet'
	__version__	= '0.0.14+'
	__author__	= 'boamaod@gmail.com'
	__requires__	= ['python-numpy']
	__desc__	= __doc__
	
	# internal vars
	__editing		= True		# we are editing, show cursor
	__cursor_index	= 0			# current cursor position
	__pin_var_rot	= 0.0			# pin-rotation variation
	__pin_var_x		= 0.0		# pin x-position variation
	__pin_var_y		= 0.0		# pin y-position variation

	# GTK editor vars
	__editor = None
	__textbuffer = None
	__fixed = None

	__export_menu = None
	__tomboy_path = None
	__tomboy = None

	__bus = None
	__obj = None

	__notifier = None

	# TEST: experimental yet
	#__textlen	= 0				# length of entire text (excluding special chars!)
	#__lines		= [[0, '']]		# list with lists [line_length, line_text]
	#__curline	= 0				# current line (index in __lines)
	# /TEST
	
	# editable options
	x = 200
	y = 200
	cp_x = 100
	cp_y = 100
	pin_x		= 100
	pin_y		= 6
	text_x_top		= 20
	text_y_top		= 20
	text_x_bottom		= 20
	text_y_bottom		= 20
	font_name	= 'Sans 12'
	rgba_color	= (0.0, 0.0, 0.0, 1.0)
	text_prefix	= ''
	text_suffix	= ''
	note_text	= ""	# hidden option because val has its own editing-dialog
	random_pin_pos	= True

	export_dest = "Tomboy"
	export_dests = ['Tomboy', 'Gnote']
	export_tag = "Lipik"
	open_after_export = True

	# constructor
	def __init__ (self, text="", **keyword_args):
		# call super (and init themes and drag/drop)
		screenlets.Screenlet.__init__(self, width=200, height=200, 
			uses_theme=True, drag_drop=True, uses_pango=True, **keyword_args) 
		# init attributes (not directly, that would cause redraw)
		self.__dict__['note_text'] = text
		self.__cursor_index = len(text)
		# set theme (redraws canvas)
		self.theme_name = "default"
		# add menu-items
#		self.add_menuitem("edit_text", "Edit...")
#		self.add_menuitem("", "-")
#		self.add_menuitem("copy", "Copy")
#		self.add_menuitem("paste", "Paste")
#		self.add_menuitem("", "-")
#		self.add_menuitem("clear", "Clear")
		# add default menuitems
		# add settings groups
		self.add_options_group(_('Text'), 
			_('Text-/Font-related settings for the sticknotes.'))
		self.add_options_group(_('Layout'), 
			_('The Layout-related settings for the sticknotes..'))
		self.add_options_group(_('Export'), 
			_('The Export options for the sticknotes.'))
		# add editable options
		self.add_option(IntOption(_('Layout'), 'pin_x', 
			self.pin_x, _('X-Position of Pin'), 
			_('The X-Position of the tack/pin for the sticknote ...'), 
			min=0, max=200))
		self.add_option(IntOption(_('Layout'), 'pin_y', 
			self.pin_y, _('Y-Position of Pin'), 
			_('The Y-Position of the tack/pin for the sticknote ...'), 
			min=0, max=200))
		self.add_option(BoolOption(_('Layout'), 'random_pin_pos', 
			self.random_pin_pos, _('Randomize Pin'), 
			_('If active, the pin/tack will be slightly moved randomly '+\
			'whenever the note is picked up ...')))
		self.add_option(FontOption(_('Text'), 'font_name', 
			self.font_name, _('Default Font'), 
			_('The default font of the text (when no Markup is used) ...')))
		self.add_option(ColorOption(_('Text'), 'rgba_color', 
			self.rgba_color, _('Default Color'), 
			_('The default color of the text (when no Markup is used) ...')))
		self.add_option(IntOption(_('Layout'), 'text_x_top', 
			self.text_x_top, _('X-top position'), 
			_('The X-Position of the text-rectangle\'s upper left corner ...'), 
			min=0, max=200))
		self.add_option(IntOption(_('Layout'), 'text_y_top', 
			self.text_y_top, _('Y-top position'), 
			_('The Y-Position of the text-rectangle\'s upper left corner ...'), 
			min=0, max=200))
		self.add_option(IntOption(_('Layout'), 'text_x_bottom', 
			self.text_x_bottom, _('X-bottom position'), 
			_('The X-Position of the text-rectangle\'s down right corner ...'), 
			min=0, max=200))
		self.add_option(IntOption(_('Layout'), 'text_y_bottom', 
			self.text_y_bottom, _('Y-bottom position'), 
			_('The Y-Position of the text-rectangle\'s down right corner ...'), 
			min=0, max=200))
		self.add_option(IntOption(_('Layout'), 'cp_x', 
			self.cp_x, _('Colorpicker X-position'), 
			_('The X-Position of color picker to paint the text background...'), 
			min=0, max=200))
		self.add_option(IntOption(_('Layout'), 'cp_y', 
			self.cp_y, _('Colorpicker Y-position'), 
			_('The Y-Position of the color picker to paint the text background...'), 
			min=0, max=200))
#		self.add_option(StringOption('Text', 'text_prefix', 
#			self.text_prefix, 'Text-Prefix', 
#			'The text/Pango-Markup to be placed before the text ...'))
#		self.add_option(StringOption('Text', 'text_suffix', 
#			self.text_suffix, 'Text-Suffix', 
#			'The text/Pango-Markup to be placed after the text ...'))
		# add hidden "note_text"-option (to save but not show in editor)
		self.add_option(StringOption(_('Text'), 'note_text', 
			self.note_text, _('Note-Text'), 
			_('The text on this sticky note ...'), hidden=True))
		self.add_option(StringOption(_('Export'), 'export_dest', 
			self.export_dest, _('Export destination'),
			_('What is the destination of the export from the Screenlet'),
			choices = self.export_dests))
		self.add_option(BoolOption(_('Export'), 'open_after_export', 
			self.open_after_export, _('Open after export'), 
			_('If checked, the note will be opened in the destination application immediately after export.')))
		self.add_option(StringOption(_('Export'), 'export_tag', 
			self.export_tag, _('Exported note tag'), 
			_('The tag string that will be connected to note exported')))

		self.__notifier = screenlets.utils.Notifier(self)

	def on_load_theme (self):
		print "ON_LOAD_THEME"

		name = 'note-bg'

		fn = ""

		if os.path.isfile (self.theme.path + '/' + name + '.svg'):
			fn = self.theme.path + '/' + name + '.svg'
		elif os.path.isfile (self.theme.path + '/' + name + '.png'):
			fn = self.theme.path + '/' + name + '.png'

		pixbuf = gtk.gdk.pixbuf_new_from_file(fn)

		# SEE KUSKILE MUJALE VEEL, ET ÕIGE SUURUS TULEKS ALATI????
		self.height=pixbuf.get_height()
		self.width=pixbuf.get_width()



	def on_init (self):
		print "Screenlet has been initialized."
		# add default menuitems

		self.__export_menu = self.add_menuitem("export", _("Export now"))
		
		self.init_export()

		# add default menu items
		self.add_default_menuitems()

		self.on_load_theme()

		x_size = int((self.width-self.text_x_top-self.text_x_bottom)*self.scale)
		y_size = int((self.height-self.text_y_top-self.text_y_bottom)*self.scale)

		x_pos = int(self.text_x_top*self.scale)
		y_pos = int(self.text_y_top*self.scale)

		# create textview
		self.__editor = gtk.TextView()
		self.__editor.set_size_request(x_size, y_size)
		self.__editor.set_wrap_mode(gtk.WRAP_WORD_CHAR)
		self.__textbuffer = gtk.TextBuffer()
		self.__textbuffer.set_text(self.note_text)
		self.__textbuffer.connect("changed", self.buf_on_change)

		self.__editor.set_buffer(self.__textbuffer)

		self.__editor.modify_font(pango.FontDescription(self.font_name))
		textcol = gdk.Color(int(self.rgba_color[0]*65535), int(self.rgba_color[1]*65535), int(self.rgba_color[2]*65535))
		self.__editor.modify_text(gtk.STATE_NORMAL, textcol)

		self.__editor.modify_base(gtk.STATE_NORMAL, self.render_color('note-bg'))

		self.__fixed = gtk.Fixed()
		self.window.add(self.__fixed)
		self.__fixed.put(self.__editor, x_pos, y_pos)

		self.window.show_all()        


	def buf_on_change(self, buf):
		self.note_text = buf.get_text(*buf.get_bounds())
#		self.__dict__['note_text'] = self.note_txt

	def on_update_shape(self):

		if self.__editor is None:
			return

		x_size = int((self.width-self.text_x_top-self.text_x_bottom)*self.scale)
		y_size = int((self.height-self.text_y_top-self.text_y_bottom)*self.scale)

		x_pos = int(self.text_x_top*self.scale)
		y_pos = int(self.text_y_top*self.scale)

		self.__editor.modify_font(pango.FontDescription(self.font_name))
		textcol = gdk.Color(int(self.rgba_color[0]*65535), int(self.rgba_color[1]*65535), int(self.rgba_color[2]*65535))
		self.__editor.modify_text(gtk.STATE_NORMAL, textcol)

		self.__editor.modify_base(gtk.STATE_NORMAL, self.render_color('note-bg'))

		self.__editor.set_size_request(x_size, y_size)
		self.__fixed.move(self.__editor,  x_pos, y_pos)


	def __setattr__ (self, name, value):
		# call Screenlet.__setattr__ in baseclass (ESSENTIAL!!!!)
		screenlets.Screenlet.__setattr__(self, name, value)
		# check attribute name

		if name == 'note_text':
			pass
		if name in ('export_dest', 'open_after_export'):
			self.init_export()
		elif name in ('font_name', 'width', 'height', 'pin_x', 'pin_y', 'cp_x', 'cp_y', 'text_x_top', 
			'text_y_top', 'text_x_bottom', 
			'text_y_bottom', 'random_pin_pos', 
			'rgba_color'):
			if self.window:
				self.redraw_canvas()
				self.update_shape()


	def init_export(self):

		if self.__export_menu is None:
			return

		# detect tomboy/gnote only by filesystem, don't start tomboy/gnote automatically by using dbus

		if self.export_dest == 'Tomboy':

			if os.environ.has_key("tomboy_path"):
				self.__tomboy_path = os.environ["__tomboy_path"]
			else:
				self.__tomboy_path = "~/.local/share/tomboy"
			self.__tomboy_path = os.path.expanduser(self.__tomboy_path)

			# if tomboy is used in the system, add export to Tomboy menuitem
			if (os.path.exists(self.__tomboy_path) and os.path.isdir(self.__tomboy_path)):
				self.__export_menu.set_sensitive(True)	
			else:
				self.__export_menu.set_sensitive(False)

		elif self.export_dest == 'Gnote':

			if os.environ.has_key("gnote_path"):
				self.__tomboy_path = os.environ["__gnote_path"]
			else:
				self.__tomboy_path = "~/.local/share/gnote"
			self.__tomboy_path = os.path.expanduser(self.__tomboy_path)

			# if tomboy is used in the system, add export to Tomboy menuitem
			if (os.path.exists(self.__tomboy_path) and os.path.isdir(self.__tomboy_path)):
				self.__export_menu.set_sensitive(True)	
			else:
				self.__export_menu.set_sensitive(False)

		else: # should never happen

			self.__export_menu.set_sensitive(False)


	# drawing
	
	def draw_pin (self, ctx):
		"""Draw the pin at its position to the given context."""
		ctx.translate(self.pin_x, self.pin_y)
		# add some variation?
		if self.random_pin_pos:
			ctx.rotate(self.__pin_var_rot)
			ctx.translate(self.__pin_var_x, self.__pin_var_y)
		# render pin
		ctx.set_operator (cairo.OPERATOR_OVER)
		if self.theme.loaded:
			#self.theme["note-pin.svg"].render_cairo(ctx)
			self.theme.render(ctx, 'note-pin')
	
	# screenlet event handlers
	
	def on_drop (self, x, y, sel_data, timestamp):
		print "SOMETHING DROPPED!! TODO: ask for confirmation if text not empty"
		txt = sel_data.get_text()
		if txt != "":
			self.note_text += txt
	
	def on_focus (self, event):
		if self.__editing == False:
			self.__editing = True
#			self.redraw_canvas()	# TODO: only redraw cursor area
	
	def on_unfocus (self, event):
		if self.__editing == True and self.is_dragged == False:
			self.__editing = False
#			self.redraw_canvas()

	
	def on_menuitem_select (self, id):
		if id=="export":

			print "EXPORTING..."

			header = '<?xml version="1.0" encoding="utf-8"?>\n<note version="0.3" xmlns:link="http://beatniksoftware.com/tomboy/link" xmlns:size="http://beatniksoftware.com/tomboy/size" xmlns="http://beatniksoftware.com/tomboy">\n'
			cr = '<create-date>' + datetime.datetime.now().isoformat() + '</create-date>\n'
			ch = '<last-change-date>'+ datetime.datetime.now().isoformat() + '</last-change-date>\n'
			mdch = '<last-metadata-change-date>' + datetime.datetime.now().isoformat() + '</last-metadata-change-date>\n'
			cp = '<cursor-position>0</cursor-position>\n'
			tags = '<tags><tag>' + self.export_tag + '</tag></tags>\n'
			openst = '<open-on-startup>False</open-on-startup>'

			print str(datetime.datetime.now())


#			print "\"" + contents + "\""

			if (self.export_dest == 'Tomboy' or self.export_dest == 'Gnote') and self.open_after_export:

				# Get the D-Bus session bus
				self.__bus = dbus.SessionBus()
				print self.__bus

				# Access the Tomboy D-Bus object
				self.__obj = self.__bus.get_object("org.gnome." + self.export_dest, "/org/gnome/" + self.export_dest + "/RemoteControl")
				print self.__obj

				# Access the Tomboy remote control interface
				self.__tomboy = dbus.Interface(self.__obj, "org.gnome." + self.export_dest + ".RemoteControl")
				print self.__tomboy

				if self.__tomboy is not None:
					self.__export_menu.set_sensitive(True)
				else:
					self.__export_menu.set_sensitive(False)
					self.__notifier.notify(self.export_dest + " D-Bus interface is not available!")
					return

				# note://tomboy/589ee349-d19a-4d77-83a1-b0d15e336889

				footer = '</note>'

#				new_note = self.__tomboy.CreateNote()

				# why is 42 max width for a title???
				title = self.note_text[:self.note_text.find('\n')][:42]

				new_note = self.__tomboy.CreateNamedNote(title)

				if new_note == "":
					new_note = self.__tomboy.CreateNote()

				print new_note

#				contents = '<text xml:space="preserve"><note-content version="0.1">' + self.note_text + '</note-content></text>'

				contents = '<note-title>' + title + '</note-title><title>' + title + '</title><text xml:space="preserve"><note-content version="0.1">' + self.note_text + '</note-content></text>'
#				contents = '<title></title><text xml:space="preserve"><note-content version="0.1">' + self.note_text + '</note-content></text>'

				note_xml = header + contents + footer

#				print note_xml

				self.__tomboy.SetNoteCompleteXml(new_note, note_xml)
				self.__tomboy.AddTagToNote(new_note, self.export_tag)

				print "Starting to display note"

				self.__tomboy.DisplayNote(new_note)

			elif self.export_dest == 'Tomboy' or self.export_dest == 'Gnote':

				footer = ch + mdch + cr + cp + tags + openst + '</note>'

				contents = '<title />\n<text xml:space="preserve"><note-content version="0.1">' + self.note_text + '</note-content></text>\n'

				note_xml = header + contents + footer

				name = str(uuid.uuid4())
				filename = name + ".note"
				filepath = self.__tomboy_path+"/" + filename

				print "exporting to: " + filepath

				f = open(filepath,'w')
				print >>f, note_xml

				self.__notifier.notify("Silently exported to " + self.export_dest + ".")

	
	def on_mouse_down (self, event):
		#x = event.x / self.scale
		#y = event.y / self.scale

		if event.button == 1:
			self.__pin_var_rot = (random.random()-0.5)/2
			self.__pin_var_x = random.random()
			self.__pin_var_y = random.random()
			self.redraw_canvas()
		return False
	
	# the drawing-handler, draws this Screenlet's background/visuals
	def on_draw (self, ctx):
		# set scale
		ctx.scale(self.scale, self.scale)
		# translate while dragging
		if self.is_dragged:
			ctx.translate(-5, -5)
		#else:
			#else, add a small randomized rotation
			#ctx.rotate((random.random()-0.5)/25)
			# TODO: resize window to fit after rotation

		# render bg
		ctx.set_operator (cairo.OPERATOR_OVER)
		if self.theme.loaded:
			#self.theme["note-bg.svg"].render_cairo(ctx)

			name = 'note-bg'
			self.theme.render(ctx, name)

#		self.__editor.modify_base(gtk.STATE_NORMAL, self.render_color(ctx, 'note-bg'))


		# draw pin if not dragging
		if self.is_dragged == False:
			self.draw_pin(ctx)

	def render_color (self, name):
		"""Get some color from theme background."""

		if not self.theme:
			return gdk.Color(0xffff, 0xffff, 0xffff, 0xffff)

		fn = ""

		### Render Graphics even if rsvg is not available###
		if os.path.isfile (self.theme.path + '/' + name + '.svg'):
			fn = self.theme.path + '/' + name + '.svg'
		elif os.path.isfile (self.theme.path + '/' + name + '.png'):
			fn = self.theme.path + '/' + name + '.png'

		pixbuf = gtk.gdk.pixbuf_new_from_file(fn)
		pb = pixbuf.subpixbuf(self.cp_x,self.cp_y,1,1)

#		print subpixbuf.get_pixels()
#		print subpixbuf.get_pixels_array().tolist()[0][0]


		arr=pb.get_pixels_array()
#		arr=pb.get_pixels()

#		width,height = pb.get_width(),pb.get_height()
#		img = Image.fromstring("RGB",(width,height),pb.get_pixels() )
#		print img.getcolors()
#		print img.getpixel((0,0))
		
#		colors = img.getcolors()
#		print arr
#		print arr.tolist()

		a = arr.tolist()[0][0]

#		print gdk.Color(a[0]*0x100, a[1]*0x100, a[2]*0x100, a[3]*0x100)
		return gdk.Color(a[0]*0x100, a[1]*0x100, a[2]*0x100, a[3]*0x100)
#		return gdk.Color(0xffff, 0xffff, 0xffff, 0xffff)
#		return subpixbuf.get_pixels_array().tolist()[0][0]
		
	
	# this handler draws the Screenlets window-shape to make
	# the window-background click-through in transparent areas
	def on_draw_shape (self,ctx):
		#set scale
		ctx.scale(self.scale, self.scale)
		# just render bg
		if self.theme:
			#self.theme["note-bg.svg"].render_cairo(ctx)
			self.theme.render(ctx, 'note-bg')
	
	# other event handling
	
	# NOTE: self.is_dragged doesn't work properly .. this needs fixing

	

# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
	# create new session
	import screenlets.session
	screenlets.session.create_session(LipikScreenlet)

