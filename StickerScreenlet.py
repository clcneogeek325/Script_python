#!/usr/bin/env python

import screenlets
from screenlets.options import IntOption
import cairo
import gobject

# use gettext for translation
import gettext

_ = screenlets.utils.get_translator(__file__)

def tdoc(obj):
	obj.__doc__ = _(obj.__doc__)
	return obj

@tdoc
class StickerScreenlet(screenlets.Screenlet):
	"""A simple linux eye candy. Distro stickers for your desktop."""
	
	# default meta-info for Screenlets
	__name__ = 'StickerScreenlet'
	__version__ = '0.1.2+'
	__author__ = 'Whise'
	__desc__ = __doc__

	xx = 0

	def __init__(self, **keyword_args):
		screenlets.Screenlet.__init__(self, width=200, height=200,uses_theme=True, **keyword_args) 
		self.theme_name = "Linux"
		# add add default menu items
		self.add_default_menuitems()
		# add settings
		self.add_option(IntOption('Screenlet', 'xx', 
			self.xx, _('Rotation angle'), _('Rotation angle'), 
			min=0, max=360))		

	def __setattr__(self, name, value):
		screenlets.Screenlet.__setattr__(self, name, value)
		if name == 'xx':
			self.redraw_canvas()

	def on_draw(self, ctx):
		ctx.scale(self.scale, self.scale)
		ctx.set_operator(cairo.OPERATOR_OVER)		
		if self.theme:
			ctx.translate(50,50)
			ctx.translate(self.theme.width / 2.0, self.theme.height / 2.0);
			ctx.rotate((self.xx)*3.14/180);
			ctx.translate(-self.theme.width / 2.0, -self.theme.height / 2.0);
			self.theme['sticker.svg'].render_cairo(ctx)
			ctx.save()

	def on_draw_shape(self,ctx):
		ctx.scale(self.scale, self.scale)
		ctx.set_operator(cairo.OPERATOR_OVER)	
		if self.theme:
			self.on_draw (ctx)

# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
	import screenlets.session
	screenlets.session.create_session(StickerScreenlet)
