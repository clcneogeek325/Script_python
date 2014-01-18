#!/usr/bin/env python

import cairo
import gtk
import pango
import gobject
import os
import threading
import commands
import random

Flickr = Plugins.importAPI('Flickr')

#log = screenlets.logger.get_default_logger()

X_SIZE = 400
Y_SIZE = 400

# use gettext for translation
import gettext

_ = screenlets.utils.get_translator(__file__)

def tdoc(obj):
	obj.__doc__ = _(obj.__doc__)
	return obj

class Updater(threading.Thread):

	failstate = False
	laststate = False

	dealingWithData = False

	__lock = threading.Lock()
	image2 = ""

	screenlet = None
	
	engine1 = None

	folders = None
	recursive = False

	shown_rss_urls = []
	shown_folder_paths = []

	flickr = None
	flickr_gen = None
	flickr_imgs = None
	flickr_current = ''

	flickrurl = None
	mediaRSS_URL = None
	
	url = None

	tmp = commands.getoutput("echo $HOME") + "/.cache/screenlets/Slideshow"
	os.system("mkdir -p " + tmp)

	use_types = ['.jpg', '.gif', '.png','.bmp', '.svg', '.jpeg', '.tif', '.tiff']

	def __init__(self, screenlet):
		threading.Thread.__init__(self)
		self.screenlet = screenlet

	def set_engine(self, engine):
		self.engine1 = engine

	def fetch_flickr(self):

		print "Trying Flickr..."


		try:
			if not self.flickr:
				self.flickr = Flickr.Flickr()

			use_new_fetching = hasattr(self.flickr, 'fetch_images')

			if self.flickr_current != self.flickrurl:
				self.flickr_imgs = []
				self.flickr_current = self.flickrurl
				self.flickr_gen = None

			print 'Loading %s.' % self.flickrurl
			# Keep the number of cached images above 20 if possible.
			# This ensures that the Slideshow doesn't get too repetitive.
			while not self.flickr_imgs or len(self.flickr_imgs) < 20:
				if use_new_fetching:
					print 'Using new fetching mechanism.'
					# Try to use the previous generator.
					if self.flickr_gen:
						try:
							imgs = self.flickr_gen.next()
						except StopIteration:
							self.flickr_gen = None
	
					# Try a new generator (in case the page updated).
					if not self.flickr_gen:
						self.flickr_gen = self.flickr.fetch_images(self.flickrurl)
						try:
							imgs = self.flickr_gen.next()
						except StopIteration:
							# Give up on fetching images.
							break
	
					# Catch duplicated image sets.
					if imgs == self.flickr_imgs:
						self.flickr_gen = None
						break
	
					# Add the fetched images to our cache.
					self.flickr_imgs += imgs
				else:
					print 'Using old Flickr plugin API.'
					# Use the old Flickr plugin API.
					imgs = self.flickr.get_image_list(self.flickrurl)
					urls = [self.flickr.url_list[img] for img in imgs]
					self.flickr_imgs += zip(imgs, urls)
					if len(self.flickr_imgs) == 0:
						break

			if len(self.flickr_imgs) == 0:
				return False

			image, url = random.choice(self.flickr_imgs)

			self.flickr_imgs.remove((image, url))

			self.url = url

			print url

			self.image2 = self.tmp + "/slide"
			self.flickr.save_image(image, self.image2)

		except:
			traceback.print_exc()

			return False

		return True

	def fetch_mediaRSS(self):

		print "Trying RSS..."

		print self.mediaRSS_URL

		try:
			source = urlopen(self.mediaRSS_URL)
			sourcetxt = source.read()

			print "Opened and read."

			items = []
			while sourcetxt.find("<item>")>0:
				sourcetxt = sourcetxt[sourcetxt.find("<item>")+1:]
				item = sourcetxt[:sourcetxt.find("</item>")]
				items.append(item)

			print len(items), "items found."

			# show only the ones not shown if possible
			# ...
			# remove image of previous url first if it's not the only one
			if len(items) > 1:
				for item in items:
					imageurl = item[item.rfind("<link>")+6:]
					imageurl = imageurl[:imageurl.find("</link>")]
					if imageurl == self.url:
						items.remove(item)

			# fallback from these, not two in a row
			fallback = random.choice(items)

			# remove all the shown urls
			for shown_url in self.shown_rss_urls:
				for item in items:
					imageurl = item[item.rfind("<link>")+6:]
					imageurl = imageurl[:imageurl.find("</link>")]
					if imageurl == shown_url:
						items.remove(item)

			# at least one should be left, if so, next time free choice
			if len(items) == 1:
				print "Emptying blacklist."
				self.shown_rss_urls = []

			# this should rarely happen
			if len(items) == 0:
				print "Fallback!"
				item = fallback
				self.shown_rss_urls = []
			else:
				print "Still variety of", len(items)
				# just choose random image of the remaining ones
				item = random.choice(items)

			imageurl = item[item.rfind("<link>")+6:]
			imageurl = imageurl[:imageurl.find("</link>")]

			realimage = item[item.rfind("<media:content"):]
			realimage = realimage[realimage.find("url=")+4:]
			realimage = realimage[:realimage.find("/>")]

			if realimage.find(" ") >= 0:
				realimage = realimage[:realimage.find(" ")]

			realimage = realimage.replace('"', '').replace("'", "")

			print realimage

			imageget = urlopen(realimage)
			imagefile = imageget.read()

			print "Acquired all right."

			fileObj = open( self.tmp + "/slide","w") #// open for for write
			fileObj.write(imagefile)

			fileObj.close()

			print "Updated slide file."

			self.shown_rss_urls.append(imageurl)
			self.url = imageurl

		except:
			traceback.print_exc()
			return False

		self.image2 =  self.tmp + "/slide"	

		return True

	def fetch_folder(self):

		print "Trying Folder..."

		imgs = []
		if self.recursive:
			for root, dirs, files in os.walk(self.folders): 
				if len(imgs) > self.screenlet.recursion_limit:
					break
				for file in files:
					if len(imgs) > self.screenlet.recursion_limit:
						break
					try:
						if os.path.splitext(file)[1].lower() in self.use_types:
							print root, file
							imgs.append(os.path.join(root,file))
					except:
						traceback.print_exc()
						pass
		else:
			if os.path.exists(self.folders) and os.path.isdir(self.folders): 
				for f in os.listdir(self.folders):				
					try:  #splitext[1] may fail
						if os.path.splitext(f)[1].lower() in self.use_types: 
							# if so, add it to our list.
									 imgs.append(self.folders + os.sep + f)
					except:
						traceback.print_exc()
						pass
		try:


			if len(imgs) == 0:

				return False

			# show only the ones not shown if possible
			# ...
			# remove image of previous url first if it's not the only one
			if len(imgs) > 1:
				try:
					imgs.remove(self.image2)
				except ValueError:
					pass

			# fallback from these, not two in a row
			fallback = random.choice(imgs)

			# remove all the shown folder paths
			for shown_path in self.shown_folder_paths:
				try:
					imgs.remove(shown_path)
				except ValueError:
					pass

			# at least one should be left, if so, next time free choice
			if len(imgs) == 1:
				print "Emptying blacklist."
				self.shown_folder_paths = []

			# this should rarely happen
			if len(imgs) == 0:
				print "Fallback!"
				image = fallback
				self.shown_folder_paths = []
			else:
				print "Still variety of", len(imgs)
				# just choose random image of the remaining ones
				image = random.choice(imgs)

			self.shown_folder_paths.append(image)
			self.image2 = image

		except:
			traceback.print_exc()
			pass

		print self.image2

		return True


	def run ( self ):

		self.flickrurl = self.screenlet.flickrurl
		self.mediaRSS_URL = self.screenlet.mediaRSS_URL
		self.recursive = self.screenlet.recursive
		self.folders = self.screenlet.folders
		
		if not self.dealingWithData:
			self.dealingWithData = True
			threading.Thread(target=self.__deal_with_data).start()
			
	def __deal_with_data(self):
		try:
			self.__lock.acquire()

			if self.engine1 == _('Flickr'):
				if not self.fetch_flickr():
					self.failstate = True
					if self.laststate is not self.failstate:
						self.screenlet.notifier.notify(_("Flickr failed, fallback!"))
						self.laststate = self.failstate
				else:
					self.laststate = not self.failstate
					self.failstate = False

			if self.engine1 == _('Media RSS'):
				if not self.fetch_mediaRSS():
					self.failstate = True
					if self.laststate is not self.failstate:
						self.screenlet.notifier.notify(_("Media RSS failed, fallback!"))
						self.laststate = self.failstate
				else:
					self.laststate = not self.failstate
					self.failstate = False

			if self.engine1 == _('Folder') or self.failstate:
				if self.fetch_folder():
					self.failstate = False

		finally:
			self.__lock.release()
			
		self.dealingWithData = False
		gobject.idle_add(self.screenlet.on_reloaded, not self.failstate)


@tdoc
class SlideshowScreenlet (screenlets.Screenlet):
	"""A dynamic picture frame that displays either pictures from Flickr or any Media RSS picture feed (e.g. Picasa, deviantART, ...) or a folder in your filesystem. You can switch the picture in the frame anytime by dragging and dropping an image."""
	
	# --------------------------------------------------------------------------
	# meta-info, options
	# --------------------------------------------------------------------------
	
	__name__		= 'SlideshowScreenlet'
	__version__		= '1.3.10+'
	__author__		= 'Guido Tabbernuk <boamaod@gmail.com>'
	__requires__		= ['python-imaging']
	__desc__		= __doc__
	
	# attributes
	notifier = None
	
	__image = ""
	__timeout = None

	__updater = None

	__start_menu = None
	__stop_menu = None
	__visit_menu = None
	__next_menu = None
	__wall_menu = None
	__folder_menu = None


	# editable options
	update_interval = 60

	image_scale		= 1.0

	image_offset_x	= 0
	image_offset_y	= 0

	image_border = 4
	border_color = (0,0,0,0.5)

	image_shadow = 4
	shadow_color = (0,0,0,0.7)

	bounding_x = X_SIZE
	bounding_y = Y_SIZE
	show_bounding = False

	anchor = _('Upper left')

	border_r = 0.0
	border_g = 0.0
	border_b = 0.0
	border_a = 0.8

	menu_x = 0
	menu_y = 0

	url = ''
	initialized = False
	updated = False
	slide = True
	echo_args = commands.getoutput('grep "^XDG_PICTURES_DIR" ~/.config/user-dirs.dirs | sed -r -e "s/([^=]*=)(.*)/\\2/"')
	if len(echo_args) <= 0:
		folders = commands.getoutput("echo $HOME")
	else:
		folders = commands.getoutput("echo " + echo_args)
#	print "TEMP DIR:", tmp
	engine = _('Media RSS')
	engine1 = _('Media RSS')
	engine_sel = [_('Folder'), _('Flickr'), _('Media RSS')]
	frame_anchor = [_('Upper left'), _('Upper right'), _('Lower left'), _('Lower right'), _('Center')]
	paint_menu = False
	showbuttons = True
	recursive = False
	recursion_limit = 400

	flickrurl = 'http://www.flickr.com/explore/interesting/7days/'
	mediaRSS_URL = 'http://backend.deviantart.com/rss.xml?q=boost%3Apopular+in%3Aphotography+max_age%3A24h&type=deviation&offset=0'

	# --------------------------------------------------------------------------
	# constructor and internals
	# --------------------------------------------------------------------------

	fetching = False

	def __init__ (self, **keyword_args):
		# call super (and enable drag/drop)
		screenlets.Screenlet.__init__(self, width=X_SIZE, height=Y_SIZE,
			uses_theme=True, drag_drop=True, **keyword_args)
		# set theme
		self.theme_name = "default"

		self.width = X_SIZE
		self.height = Y_SIZE
		# initially apply default image (for newly created instances)
		#self.__image = screenlets.PATH + '/Picframe/dali.png'
		# add default menuitems (all the standard ones)
#		self.add_default_menuitems(DefaultMenuItem.XML)

		self.notifier = screenlets.utils.Notifier(self)
		self.__updater = Updater(self)

		# add option group to properties-dialog
		self.add_options_group(_('Image loading'), _('Slideshow image sources & control'))
		# add option group to properties-dialog
		self.add_options_group(_('Appearance'), _('Slideshow appearance'))
		# add editable options
		#self.add_option(FileOption(_('Image loading'), '__image', 
		#	self.__image, _('Filename'),

		self.add_option(StringOption(_('Image loading'), 'engine', self.engine,_('Select Engine'), '',choices = self.engine_sel),realtime=False)

		self.add_option(IntOption(_('Image loading'), 'update_interval', 
			self.update_interval, _('Update interval'), 
			_('The interval for updating info (in seconds: 3660 = 1 day, 25620 = 1 week)'), min=1, max=25620))
		self.add_option(BoolOption(_('Image loading'), 'slide',bool(self.slide), _('Run the show'),_('Is the slideshow running?')))


		self.add_option(StringOption(_('Image loading'), 'flickrurl', self.flickrurl,_('Flickr URL'), _('Flickr URL')))
		self.add_option(StringOption(_('Image loading'), 'mediaRSS_URL', self.mediaRSS_URL,_('Media RSS URL'), _('RSS that publishes images in Media RSS format, Picasa album, deviantART category etc')))
		self.add_option(StringOption(_('Image loading'), 'folders', self.folders,_('Image folder'), _('The folder where the pictures are to be found'),))
		self.add_option(BoolOption(_('Image loading'), 'recursive',bool(self.recursive), _('Folder recursion'),_('Show images from subfolders. Use with care, because there could be millions of images in the home folder and it may freeze the application to go through all of them.')))
		self.add_option(IntOption(_('Image loading'), 'recursion_limit', self.recursion_limit, _('Recursion limit'),_('Max images to include in slideshow material when recurring through the folders.'), min=0, max=99999999))
		

		self.add_option(BoolOption(_('Appearance'), 'showbuttons',bool(self.showbuttons), _('Show controls'),_('Show contol buttons on focus')))

		self.add_option(StringOption(_('Appearance'), 
		  'anchor', 
		  self.anchor,
		  _('Select anchor corner'), 
		  _('Select anchor corner'),
		  choices = self.frame_anchor))

		self.add_option(IntOption(_('Appearance'), 'bounding-x', 
			self.bounding_x, _('Bounding X'), 
			_('X size of bounding box'), min=50, max=10000))

		self.add_option(IntOption(_('Appearance'), 'bounding-y', 
			self.bounding_y, _('Bounding Y'), 
			_('Y size of bounding box'), min=50, max=8000))

		self.add_option(IntOption(_('Appearance'), 'border', 
			self.image_border, _('Frame width'), 
			_('Width of the frame'), min=0, max=100))

		self.add_option(ColorOption(_('Appearance'),'border_color', 
			self.border_color, _('Frame Color'), ''))

		self.add_option(IntOption(_('Appearance'), 'shadow', 
			self.image_shadow, _('Shadow width'), 
			_('Width ofthe shadow'), min=0, max=100))

		self.add_option(ColorOption(_('Appearance'),'shadow_color', 
			self.shadow_color, _('Shadow Color'), ''))

		self.add_option(BoolOption(_('Appearance'), 'showbounding',
		  bool(self.showbuttons), _('Show Boundingbox'),_('Show the bounding box')))

#		self.add_option(FloatOption(_('Appearance'), 'image_scale', self.image_scale, 
#			_('Image Scale'), _('Scale of image within this Picframe ...'), 
#			min=0.01, max=10.0, digits=2, increment=0.01,hidden=True))

#		self.add_option(IntOption(_('Appearance'), 'image_offset_x', 
#			self.image_offset_x, _('Image Offset X'), _('X-offset of upper left ')+\
#			'corner of the image within this Picframe ...', 
#			min=0, max=self.width,hidden=True))

#		self.add_option(IntOption(_('Appearance'), 'image_offset_y', 
#			self.image_offset_y, _('Image Offset Y'), _('Y-offset of upper left ')+\
#			'corner of the image within this Picframe ...', 
#			min=0, max=self.height,hidden=True))
#		self.add_option(IntOption(_('SlideShow'), 'bounding-x', 
#			self.bounding_x, _('Bounding X'), 
#			_('X size of bounding box'), min=50, max=1600))

#		self.add_option(IntOption(_('SlideShow'), 'bounding-y', 
#			self.bounding_y, _('Bounding Y'), 
#			_('Y size of bounding box'), min=50, max=1200))

		self.add_option(BoolOption(_('SlideShow'), 'showbounding',
		  bool(self.showbuttons), _('Show Boundingbox'),_('Show the bounding box')))

#		self.add_option(FloatOption(_('SlideShow'), 'image_scale', self.image_scale, 
#			_('Image Scale'), _('Scale of image within this Picframe ...'), 
#			min=0.01, max=10.0, digits=2, increment=0.01,hidden=True))

#		self.add_option(IntOption(_('SlideShow'), 'image_offset_x', 
#			self.image_offset_x, _('Image Offset X'), _('X-offset of upper left ')+\
#			'corner of the image within this Picframe ...', 
#			min=0, max=self.width,hidden=True))

#		self.add_option(IntOption(_('SlideShow'), 'image_offset_y', 
#			self.image_offset_y, _('Image Offset Y'), _('Y-offset of upper left ')+\
#			'corner of the image within this Picframe ...', 
#			min=0, max=self.height,hidden=True))


		self.update_interval = self.update_interval
		self.engine = self.engine
		self.folders = self.folders

	def __setattr__ (self, name, value):
		screenlets.Screenlet.__setattr__(self, name, value)

		if name == 'anchor':
		  self.redraw_canvas()

		if name == 'border_color':
			self.redraw_canvas()

		if name == 'border':
			self.image_border = value
			self.redraw_canvas()

		if name == 'shadow_color':
			self.redraw_canvas()

		if name == 'shadow':
			self.image_shadow = value
			self.redraw_canvas()

		if name == 'showbounding':
			self.show_bounding = value
			self.redraw_canvas()

		if name == 'bounding-x':
			self.bounding_x = value
			self.width = self.bounding_x
			self.redraw_canvas()

		if name == 'bounding-y':
			self.bounding_y = value
			self.height = self.bounding_y
			self.redraw_canvas()

		if name == 'showbuttons':
			self.redraw_canvas()

		if name == 'engine':
			if value == _('Folder') :
				self.engine1 = _('Folder')
				self.update()
			if value == '' :
				self.engine1 = _('Folder')
				self.update()
			if value == _('Flickr'):
				self.engine1 = value
				self.update()
			if value == _('Media RSS'):
				self.engine1 = value
				self.update()
		if name == 'folders' and self.engine == _('Folder'):
				self.engine1 = _('Folder')
				self.update()
		if name == "__image":
			screenlets.Screenlet.__setattr__(self, name, value)
			# update view
			self.redraw_canvas()
			#self.update_shape()
		
		if name == "update_interval":
			if value > 0:
				self.__dict__['update_interval'] = value
				if self.__timeout:
					gobject.source_remove(self.__timeout)
				self.__timeout = gobject.timeout_add(int(value * 1000), self.update)
			else:
				self.__dict__['update_interval'] = 1
				pass

	def on_init(self):

		self.width = self.width
		self.height = self.height

		self.update()
		
		print "Screenlet has been initialized."
		# add default menuitems

		self.__next_menu = self.add_menuitem("next", _("Next slide"))
		self.__visit_menu = self.add_menuitem("visit", _("Open image"))
		self.__wall_menu = self.add_menuitem("wall", _("Set as wallpaper"))
		self.__start_menu = self.add_menuitem("start", _("Start slideshow"))
		self.__stop_menu = self.add_menuitem("stop", _("Stop slideshow"))
		self.add_menuitem("folder", _("Select folder"))
		
		self.add_default_menuitems()
		self.initialized = True

		self.on_menu_state_change()
		self.redraw_canvas()

	def on_menu_state_change(self):
		

#		print "Not fetching? ", not self.fetching

		self.__next_menu.set_sensitive(not self.fetching)
		self.__stop_menu.set_sensitive(self.slide)
		self.__start_menu.set_sensitive(not self.slide)
		self.__visit_menu.set_sensitive(self.__image is not None and len(self.__image) > 0)
		self.__wall_menu.set_sensitive(self.__image is not None and len(self.__image) > 0)


	def on_reloaded (self, result):
		"""Called by updater"""
		if result == True:
		
			self.url = self.__updater.url
			self.__image = self.__updater.image2
			
			self.window.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))	
		
			self.fetching = False
			self.on_menu_state_change()

			self.redraw_canvas()

	def fetch_image(self):

		self.__updater.set_engine(self.engine1)

		if self.initialized and not self.fetching:
		
			self.fetching = True
			self.on_menu_state_change()

			self.__updater.run()

	# --------------------------------------------------------------------------
	# Screenlet handlers
	# --------------------------------------------------------------------------
	def update(self):
		#log.error('Failed to load image "%s": %s (only PNG images supported yet)' % (filename, ex))

		if self.slide:
			self.fetch_image()
		return True

	def on_drag_enter (self, drag_context, x, y, timestamp):
		self.redraw_canvas()

	def on_drag_leave (self, drag_context, timestamp):
		self.redraw_canvas()

	def on_drop (self, x, y, sel_data, timestamp):
		print "Data dropped ..."
		filename = ''
		filename = utils.get_filename_on_drop(sel_data)[0]
		print "Data filename: ", filename
		if filename != '':
			#self.set_image(filename)
			self.__image = filename.replace(chr(34),'')

	def draw_boundingbox(self, ctx):
		bounding_color = (1.0, 0.0, 0.0, 0.5)
		ctx.set_source_rgba(*bounding_color)

		self.draw_rectangle(
		  ctx,0,0,
		  self.bounding_x*self.scale, 
		  self.bounding_y*self.scale)

	def on_draw (self, ctx):

		ctx.set_operator(cairo.OPERATOR_OVER)

		if self.show_bounding:
		  self.draw_boundingbox(ctx)

		image_w, image_h = [self.width, self.height]

		if self.__image is not None and len(self.__image)>0 and self.initialized: 
			image_w, image_h = self.get_image_size(self.__image)

		scaled_image_border = self.scale * self.image_border
		scaled_image_shadow = self.scale * self.image_shadow
		scaled_total_rim = (scaled_image_border + scaled_image_shadow *2 ) * 2.0

		scaled_bounding_x =  self.bounding_x * self.scale
		scaled_bounding_y =  self.bounding_y * self.scale

		image_aspect = (image_w + scaled_total_rim ) / (image_h + scaled_total_rim)
		image_scale = 1.0
		b_box_aspect = (1.0 * self.bounding_x) / (1.0 * self.bounding_y)

		if image_aspect > b_box_aspect:
		  image_scale =  ( scaled_bounding_x - scaled_total_rim /2.0 ) / (1.0 * image_w )
		else:
		  image_scale = ( scaled_bounding_y - scaled_total_rim /2.0) / (1.0 * image_h)

		#background_color = (self.border_r, self.border_g, self.border_b, self.border_a)
		#ctx.set_source_rgba(*background_color) 

		scaled_image_x = image_scale * image_w
		scaled_image_y = image_scale * image_h

		tl_image_corner_x = scaled_total_rim / 4.0 
		tl_image_corner_y = scaled_total_rim / 4.0

		if self.anchor == _('Upper right'):
		  tl_image_corner_x = scaled_bounding_x - (scaled_total_rim / 4.0  + scaled_image_x)

		if self.anchor == _('Lower left'):
		  tl_image_corner_y = scaled_bounding_y - (scaled_total_rim / 4.0 + scaled_image_y)

		if self.anchor == _('Lower right'):
		  tl_image_corner_x = scaled_bounding_x - ( scaled_total_rim / 4.0 + scaled_image_x)
		  tl_image_corner_y = scaled_bounding_y - ( scaled_total_rim / 4.0 + scaled_image_y)

		if self.anchor == _('Center'):
		    if image_aspect < b_box_aspect:
		        tl_image_corner_x = (scaled_bounding_x - (scaled_total_rim / 4.0 + scaled_image_x - scaled_image_shadow)) / 2.0
		        tl_image_corner_y = (scaled_bounding_y - (scaled_total_rim / 4.0 + scaled_image_y))
		    else:
		        tl_image_corner_x = (scaled_bounding_x - (scaled_total_rim / 4.0 + scaled_image_x)) 
		        tl_image_corner_y = (scaled_bounding_y - (scaled_total_rim / 4.0 + scaled_image_y - scaled_image_shadow)) / 2.0

		#ctx.set_source_rgba(*self.border_color)

		self.draw_rectangle_advanced(
			ctx, 
			tl_image_corner_x - scaled_image_shadow , 
			tl_image_corner_y - scaled_image_shadow , 
			scaled_image_x, 
			scaled_image_y, 
			rounded_angles=(1, 1, 1, 1), 
			fill=False, 
			border_size = scaled_image_border , 
			border_color = self.border_color, 
			shadow_size = scaled_image_shadow , 
			shadow_color = self.shadow_color)

		#self.draw_rounded_rectangle(
		 # ctx,
		 # tl_image_corner_x,
		 # tl_image_corner_y,
		 # 1.0 * scaled_image_border / (self.scale), 
		 # scaled_image_x + 2.0 * scaled_image_border , 
		 # scaled_image_y + 2.0 * scaled_image_border)


		if self.__image is not None and len(self.__image)>0 and self.initialized: 
			self.draw_scaled_image( ctx, 
			  tl_image_corner_x,# + scaled_total_rim / 2.0, 
			  tl_image_corner_y,# + scaled_total_rim / 2.0, 
			  self.__image, 
			  scaled_image_x, 
			  scaled_image_y)

		self.menu_x = tl_image_corner_x + scaled_image_x - 80 - scaled_image_border * 2.0
		self.menu_y = tl_image_corner_y + scaled_image_y - 23 - scaled_image_border * 2.0
		ctx.translate(self.menu_x,self.menu_y)

		if self.paint_menu == True and  self.showbuttons == True: self.theme.render(ctx, 'menu')

		if self.initialized and not self.updated:
			self.updated = True
			self.update()


	def on_focus(self, event):
		self.paint_menu = True
		self.redraw_canvas()

	def on_unfocus(self, event):
		self.paint_menu = False
		self.redraw_canvas()

	def on_mouse_down(self,event):
			x, y = self.window.get_pointer()
			if y >= self.menu_y and y <=self.menu_y+22:
				if x >= self.menu_x and x <= self.menu_x+26 :
					if self.fetching:
						self.window.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
					if self.slide:
						self.slide = False
						self.notifier.notify(_("Slideshow stopped!"))
						self.update()
				elif x >= self.menu_x+27 and x <= self.menu_x+49 :
					if self.fetching:
						self.window.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
					if not self.slide:
						self.slide = True
						self.notifier.notify(_("Slideshow started!"))
						self.update()
				elif x >= self.menu_x+50 and x <= self.menu_x+76 :
					if not self.fetching:
						self.fetch_image()
					self.window.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

	def on_menuitem_select (self, id):
		"""handle MenuItem-events in right-click menu"""

		print "MENUITEM: " + id

		if id == "next":
			# TODO: use DBus-call for this
			#self.switch_hide_show()

			self.fetch_image()

		if id == "visit":
			# TODO: use DBus-call for this
			#self.switch_hide_show()
			if self.engine1 == _('Flickr'):
				os.system('firefox ' + self.url + " &")
			elif self.engine1 == _('Media RSS'):
				os.system('firefox ' + self.url + " &")
			elif self.engine1 == _('Folder'):
				os.system('gnome-open ' + chr(34) + self.__image + chr(34) + " &")

		if id == "wall":
			# TODO: use DBus-call for this
			#self.switch_hide_show()
			if screenlets.show_question(self,_('Do you want to set the current image as your desktop wallpaper?')):
				wallpaper = self.tmp + "/wallpaper"
				os.system('cp --force "%s" "%s"' % (self.__image, wallpaper))
				os.system("gconftool-2 -t string -s /desktop/gnome/background/picture_filename " + chr(34) + wallpaper + chr(34))
				os.system("gconftool-2 -t bool -s /desktop/gnome/background/draw_background False")
				os.system("gconftool-2 -t bool -s /desktop/gnome/background/draw_background True")

		if id == "start":
			self.slide = True
			self.update()
		
		if id == "stop":
			self.slide = False

		if id[:7] == "folder":
			# TODO: use DBus-call for this
			self.show_install_dialog()
			self.update()

		self.on_menu_state_change()

	def show_install_dialog (self):
		"""Craete/Show the install-dialog."""

		# create filter
		flt = gtk.FileFilter()
		flt.add_pattern('*')

		# create dialog
		dlg = gtk.FileChooserDialog(action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,buttons=(gtk.STOCK_CANCEL, 
			gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dlg.set_current_folder(self.folders)
		dlg.set_title(_('Select a folder'))
		dlg.set_filter(flt)
		# run
		resp		= dlg.run()
		filename	= dlg.get_filename()
		dlg.destroy()
		if resp == gtk.RESPONSE_OK:
			self.folders = filename 

	def on_draw_shape (self, ctx):
		ctx.scale(self.scale, self.scale)
		if self.theme:
			#self.theme['control-bg.svg'].render_cairo(ctx)
			ctx.set_source_rgba(1, 1, 1, 1)
			ctx.rectangle (0, 0, self.width, self.height)
			ctx.fill()

																					
# If the program is run directly or passed as an argument to the python
# interpreter then launch as new application
if __name__ == "__main__":
	# create session object here, the rest is done automagically
	import screenlets.session
	screenlets.session.create_session(SlideshowScreenlet, threading=True)

