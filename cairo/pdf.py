#!/usr/bin/env python
import cairo
 
nombreArch = "ejemplo1.pdf"
surface = cairo.PDFSurface( nombreArch, 400, 400)

ctx = cairo.Context(surface)
ctx.show_page()
surface.finish()
 
print "El pdf se ha crado correctamente"




