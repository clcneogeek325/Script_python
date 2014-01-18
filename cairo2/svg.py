#!/usr/bin/env python
import cairo
 
svg = cairo.SVGSurface("ejemplo.svg", 500,500)
ctx = cairo.Context(svg)
svg.finish()
 
print "La imagen se ha creado correctamente"



