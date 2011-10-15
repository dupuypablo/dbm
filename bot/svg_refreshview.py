#!/usr/bin/python

# sdaau 2010

# simple svg viewer, 
# with automatic reload of file, and refresh of view, 
# when the file has changed. 

# based on: 

# svg_compare.py
# http://ubuntuforums.org/attachment.php?attachmentid=105589&d=1236408730
# - Brian Parma -
#  Demonstrate SVG scaling with rsvg vs. gtk.gdk.Pixbuf
#  needs 'sudo apt-get install python-rsvg'

# tikz2pdf
# http://www.texample.net/tikz/resources/
# http://kogs-www.informatik.uni-hamburg.de/~meine/tikz/process/#tikz2pdf


import sys
#import cairo
import rsvg
import gtk
import gobject
import os
import time

global svgobj
global svgFileName

class SVGCompareRfvw(gtk.Window):
	def __init__(self, svg): # 'svg' arg == svgobj
		global svgobj
		gtk.Window.__init__(self)
		#~ pix = svg.get_pixbuf()
		self.w = svg.props.width
		self.h = svg.props.height
		self.ratio = self.w/self.h
		self.x, self.y = 0, 0
		self.dx, self.dy = 0, 0
		self.sx, self.sy = 1, 1
		self.ds = 0.1
		self.interp = 1
		self.interp_text = ['Nearest neighbor sampling',
							'Tiles',
							'Bilinear',
							'Hyperbolic']
		
		self.add_events(gtk.gdk.BUTTON_PRESS_MASK | 
					gtk.gdk.POINTER_MOTION_MASK |
					gtk.gdk.POINTER_MOTION_HINT_MASK |
					gtk.gdk.SCROLL_MASK |
					gtk.gdk.LEAVE_NOTIFY_MASK)
		
		self.box = None
		if (self.ratio < 1):
			horizontal = True
			self.box = gtk.HBox()
			self.set_default_size(svg.props.width*2, svg.props.height)
		else:
			horizontal = False
			self.box = gtk.VBox()
			self.set_default_size(svg.props.width, svg.props.height*2)
			
		self.add(self.box)
		
		
		self.connect('delete-event',gtk.main_quit)
	#    win.connect('expose-event',win_expose, svg)
		self.connect('button-press-event',self.butt_event)
		self.connect('scroll-event',self.scroll_event)
		self.connect('key-press-event',self.key_event)
		self.connect('motion-notify-event',self.move_event)
		#~ pix_da.connect('expose-event', self.pix_expose, pix)
		
		#~ self.show_all()
		self.f = None
		self.init2()
		
	## this part of init can be called repeatedly, 
	## to refresh the image from disk
	def init2(self):
		self.svg_da = gtk.DrawingArea()
		#~ pix_da = gtk.DrawingArea()
		if self.f is not None:
			#~ print "removing old!"
			self.box.remove(self.f)
		self.f = gtk.Frame()
		self.f.add(self.svg_da)
		self.box.add(self.f)
		#~ f = gtk.Frame()
		#~ f.add(pix_da)
		#~ box.add(f)
		
		## use the global object for expose-event, 
		##  so we can refresh it at runtime
		self.svg_da.connect('expose-event', self.svg_expose, svgobj)
		self.show_all()
		
		
	def key_event(self, widget, event):
		#print 'key',event.keyval
		if event.keyval in [gtk.keysyms.plus, gtk.keysyms.equal,
							gtk.keysyms.KP_Add]:
			self.sx += self.ds
			self.sy += self.ds
			self.queue_draw()
		elif event.keyval in [gtk.keysyms.minus, gtk.keysyms.KP_Subtract]:
			self.sx -= self.ds
			self.sy -= self.ds
			self.queue_draw()
		elif event.keyval in [gtk.keysyms.i, gtk.keysyms.I]:
			self.interp = (self.interp + 1) % 4
			print 'Switching interpolation method to: %s ' % self.interp_text[self.interp]
			self.queue_draw()
		
	
	def reloadFileAndRefresh(self):
		global svgobj
		global svgFileName
		#~ self.svg_da = gtk.DrawingArea()
		svgobj = rsvg.Handle(svgFileName)
		#~ self.svg_expose(self.svg_da, None, svgobj)
		#~ self.remove(self.box)
		#~ self.__init__(svgobj)
		self.init2()
		
	
	def butt_event(self, widget, event):
		print 'butt',event.button
		if event.button == 1:
			self.x, self.y = event.x, event.y
			## try refresh
			self.reloadFileAndRefresh()
		elif event.button == 4:
			self.sx += self.ds
			self.sy += self.ds
			self.queue_draw()
		elif event.button == 5:
			self.sx -= self.ds
			self.sy -= self.ds
			self.queue_draw()
			
	def scroll_event(self, widget, event):
		if event.direction == gtk.gdk.SCROLL_UP:
			self.sx += self.ds
			self.sy += self.ds
			self.queue_draw()
		elif event.direction == gtk.gdk.SCROLL_DOWN:
			self.sx -= self.ds
			self.sy -= self.ds
			self.queue_draw()
		
	def move_event(self, widget, event):
		#print 'move',int(event.state),int(gtk.gdk.BUTTON1_MASK)
		if event.is_hint:
			x, y, state = event.window.get_pointer()
		else:
			x, y, state = event.x, event.y, event.state
			
		if event.state & gtk.gdk.BUTTON1_MASK:
			self.dx += x - self.x
			self.dy += y - self.y
			self.x, self.y = x, y
			print self.dx, self.dy
			self.queue_draw()
		
	def svg_expose(self, da, event, svg):
		x, y, w, h = da.allocation
		if svg is not None:
			ctx = da.window.cairo_create()
			
			ctx.translate(self.dx,self.dy)  # Translate
			ctx.scale(self.sx,self.sy)      # Scale
			
			svg.render_cairo(ctx)
		
		return True

	#~ def pix_expose(self, da, event, pix):
		
		#~ interp = [gtk.gdk.INTERP_NEAREST,
				  #~ gtk.gdk.INTERP_TILES,
				  #~ gtk.gdk.INTERP_BILINEAR,
				  #~ gtk.gdk.INTERP_HYPER]
				  
		#~ # one way to scale
		#~ mod_pix = pix.scale_simple(self.w*self.sx, self.h*self.sy, interp[self.interp])
				  
		#~ if pix is not None:
#~ #            ctx = da.window.cairo_create()

#~ #            ctx.translate(self.dx,self.dy)  # Translate
#~ #            ctx.scale(self.sx,self.sy)      # another way to scale

#~ #            ctx.set_source_pixbuf(mod_pix, 0, 0)
#~ #            ctx.paint()
			#~ da.window.draw_pixbuf(None,mod_pix,0,0,self.dx,self.dy)
		
		#~ return True

#def test_event(widget, event):
	##print 'event!',int(event.type),int(event.state),event.is_hint,int(gtk.gdk.BUTTON1_MASK)
	#if event.is_hint:
		#x, y, state = event.window.get_pointer()
		#print 'hint',x,y,int(state),event.x,event.y,int(event.state)
	#if not event.is_hint:
		#print 'no hint',event.x,event.y,int(event.state)
	
## similar to a thread, this function runs repeatedly
## but only when the GtkWindow is idle... 
global previous_mtime
global svgc

def idle_refresher():
	# just needed to start out of thread.. 
	global svgc
	
	svgc.reloadFileAndRefresh()
	
	return False # because we will run just once! 

def idle_func(*args):
	global previous_mtime
	global svgFileName
	global svgc
	#~ print "idle_func", args
	mtime = os.path.getmtime(svgFileName)
	if mtime > previous_mtime:
		print "refreshview: file change detected..."
		previous_mtime = mtime
		gobject.timeout_add(500, idle_refresher)
	
	time.sleep(0.025) 	# idle_add seems to hog the processor 
						# .. but with time.sleep here, we enforce a rendering 
						# .. framerate! For 40 fps, we have 1/40 = 0.025 sec
	return True


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print sys.argv[0]+':','usage:',sys.argv[0],'<filename>'
	else:
		global svgobj
		global svgFileName
		global previous_mtime
		global svgc
		try:
			svgFileName = sys.argv[1]
			# must also init previous_mtime here:
			previous_mtime = os.path.getmtime(svgFileName)
			svgobj = rsvg.Handle(svgFileName)
			svgc = SVGCompareRfvw(svgobj)
			gobject.threads_init()
			gtk.gdk.threads_init()
			gobject.idle_add(idle_func)
			gtk.main()
		except KeyboardInterrupt:
			gtk.main_quit()
