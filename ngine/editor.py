# -*- coding: utf-8 -*-
#===================================================
# 
# A map editor for Ngine
#
# Copyright (C) 2011  Wil Alvarez <wil.alejandro@gmail.com>
#
#===================================================

import gtk
import cairo

class MapTest(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.active = False
        self.error = False
        self.connect('expose-event', self.expose)
        self.set_size_request(1600, 1600)
        self.timer = None
        self.count = 1
        
    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        cr.set_line_width(0.3)
        rect = self.get_allocation()
        
        w_tile = 32
        h_tile = 32
        
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.rectangle(0, 0, 1600, 1600)
        cr.fill()
        
        cr.set_source_rgb(1.0, 1.0, 1.0)
        for i in range (1600/32):
            cr.move_to(32 * i, 0)
            cr.line_to(32 * i, 1600)
            
            cr.move_to(0, 32 * i)
            cr.line_to(1600, 32 * i)
            
            cr.stroke()

class MapEditor(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        
        self.set_title('Ngine Map Editor')
        self.set_size_request(1024, 600)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect('delete-event', self.__close)
        
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.test = MapTest()
        scroll.add_with_viewport(self.test)
        
        self.toolbox = gtk.VBox(False)
        self.toolbox.set_size_request(224, 600)
        
        toolbar = gtk.HBox(False)
        
        mainbox = gtk.HBox(False)
        mainbox.pack_start(scroll, True, True)
        mainbox.pack_start(self.toolbox, False, False)
        
        self.statusbar = gtk.Statusbar()
        self.statusbar.push(0, 'Welcome...')
        
        vbox = gtk.VBox(False)
        vbox.pack_start(toolbar, False, False, 0)
        vbox.pack_start(mainbox, True, True, 0)
        vbox.pack_start(self.statusbar, False, False)
        
        self.add(vbox)
        
        self.show_all()
        
    def __close(self, widget, event):
        self.destroy()
        gtk.main_quit()
        
if __name__ == '__main__':
    m = MapEditor()
    gtk.main()
