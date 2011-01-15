# -*- coding: utf-8 -*-
#===================================================
# 
# A map editor for Ngine
#
# Copyright (C) 2011  Wil Alvarez <wil.alejandro@gmail.com>
#
#===================================================

import os
import gtk
import cairo

class Map(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON1_MOTION_MASK)
        
        self.connect('expose-event', self.expose)
        self.width = 1
        self.height = 1
        self.tilewidth = 1
        self.tileheight = 1
        self.real_width = 1
        self.real_height = 1
        
        self.layers = {
            'background': None,
            'decorations': None,
            'unwalkable': None,
            'items': None,
            'characters': None,
        }
        
        self.enable = {
            'background': True,
            'decorations': True,
            'unwalkable': True,
            'items': True,
            'characters': True,
            'all': True
        }
    
    def __get_int_val(self, fd):
        return int(fd.readline().strip().split(' = ')[1])
        
    def __get_float_val(self, fd):
        return float(fd.readline().strip().split(' = ')[1])
        
    def __get_str_val(self, fd):
        return fd.readline().strip().split(' = ')[1]
        
    def __build_color(self, str_val):
        r = int(str_val.split(',')[0])
        g = int(str_val.split(',')[1])
        b = int(str_val.split(',')[2])
        return (r, g, b)
                    
    def __process_section(self, fd, header):
        tilename = self.__get_str_val(fd)
        tsw = self.__get_int_val(fd)
        tsh = self.__get_int_val(fd)
        
        tilepath = os.path.realpath(os.path.join(os.path.dirname(__file__),
        '..', 'data', 'images', tilename))
        
        tilepixbuf = gtk.gdk.pixbuf_new_from_file(tilepath)
        self.layers[header] = []
        
        htile = TileHandler()
        htile.load(tilename, (self.tilewidth, self.tileheight) , (tsw, tsh))
        
        for i in range(self.height):
            row = fd.readline().strip().split(' ')
            self.layers[header].append([])
            
            for j in range(len(row)):
                if row[j] == '00': 
                    self.layers[header][i].append(None)
                else:
                    self.layers[header][i].append(htile.get(row[j]))
        
    def load(self, filename):
        filepath = os.path.realpath(os.path.join(os.path.dirname(__file__),
        '..', 'data', 'maps', filename))
        fd = open(filepath, 'r')
        
        # Load map settings
        header = fd.readline().strip()
        
        if header != '[ngine-map]':
            raise SyntaxWarning
        self.width = self.__get_int_val(fd)
        self.height = self.__get_int_val(fd)
        self.tilewidth = self.__get_int_val(fd)
        self.tileheight = self.__get_int_val(fd)
        self.bgcolor = self.__build_color(self.__get_str_val(fd))
        self.scrolling = self.__get_float_val(fd)
        fd.readline().strip()
        
        header = fd.readline()
        while header != '':
            header = header.strip()
            if header == '[background]':
                self.__process_section(fd, header[1:-1])
            elif header == '[decorations]':
                self.__process_section(fd, header[1:-1])
            elif header == '[unwalkable]':
                self.__process_section(fd, header[1:-1])
            elif header == '[items]':
                self.__process_section(fd, header[1:-1])
            elif header == '[characters]':
                self.__process_section(fd, header[1:-1])
            
            fd.readline()
            header = fd.readline()
            
        self.real_width = self.width * self.tilewidth
        self.real_height = self.height * self.tileheight
        self.set_size_request(self.real_width, self.real_height)
        
    def set_layer(self, layer, value):
        self.enable[layer]= value
        self.queue_draw()
        
    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        rect = self.get_allocation()
        
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.rectangle(0, 0, self.real_width, self.real_height)
        cr.fill()
        
        if self.layers['background'] and self.enable['background']:
            for i in range(self.height):
                for j in range(self.width):
                    pix = self.layers['background'][i][j]
                    if pix:
                        cr.set_source_pixbuf(pix, self.tilewidth * j, self.tileheight * i)
                        cr.paint()
                        del pix
        
        if self.layers['decorations'] and self.enable['decorations']:
            for i in range(self.height):
                for j in range(self.width):
                    pix = self.layers['decorations'][i][j]
                    if pix:
                        cr.set_source_pixbuf(pix, self.tilewidth * j, self.tileheight * i)
                        cr.paint()
                        del pix

        if self.layers['unwalkable'] and self.enable['unwalkable']:
            for i in range(self.height):
                for j in range(self.width):
                    pix = self.layers['unwalkable'][i][j]
                    if pix:
                        cr.set_source_pixbuf(pix, self.tilewidth * j, self.tileheight * i)
                        cr.paint()
                        del pix
        
        if self.layers['items'] and self.enable['items']:
            for i in range(self.height):
                for j in range(self.width):
                    pix = self.layers['items'][i][j]
                    if pix:
                        cr.set_source_pixbuf(pix, self.tilewidth * j, self.tileheight * i)
                        cr.paint()
                        del pix
                        
        if self.layers['characters'] and self.enable['characters']:
            for i in range(self.height):
                for j in range(self.width):
                    pix = self.layers['characters'][i][j]
                    if pix:
                        cr.set_source_pixbuf(pix, self.tilewidth * j, self.tileheight * i)
                        cr.paint()
                        del pix
                        
        cr.set_line_width(0.3)
        cr.set_source_rgb(1.0, 1.0, 1.0)
        for i in range (self.real_width/self.tilewidth):
            cr.move_to(self.tilewidth * i, 0)
            cr.line_to(self.tilewidth * i, self.real_height)
            cr.stroke()
        
        for i in range (self.real_height/self.tileheight):
            cr.move_to(0, self.tileheight * i)
            cr.line_to(self.real_width, self.tileheight * i)
            cr.stroke()

class MapEditor(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        
        self.set_title('Ngine Map Editor')
        self.set_size_request(1024, 600)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect('delete-event', self.__close)
        
        # Build the toolbar
        toolbar = gtk.HBox(False)
        
        # Build the map
        scrolled_map = gtk.ScrolledWindow()
        scrolled_map.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self._map = Map()
        self._map.load('01.map')
        scrolled_map.add_with_viewport(self._map)
        self._map.connect("button-press-event", self.__print)
        
        # Build the toolbox
        bg_layer = LayerBox('Background')
        bg_layer.toggle.connect('toggled', self.__toggle_layer, 'background')
        dc_layers = LayerBox('Decorations', bg_layer.radio)
        dc_layers.toggle.connect('toggled', self.__toggle_layer, 'decorations')
        uw_layers = LayerBox('Unwalkable', bg_layer.radio)
        uw_layers.toggle.connect('toggled', self.__toggle_layer, 'unwalkable')
        it_layers = LayerBox('Items', bg_layer.radio)
        it_layers.toggle.connect('toggled', self.__toggle_layer, 'items')
        ch_layers = LayerBox('Characters', bg_layer.radio)
        ch_layers.toggle.connect('toggled', self.__toggle_layer, 'characters')
        
        layers_box = gtk.VBox(False)
        layers_box.pack_start(bg_layer, False, False, 0)
        layers_box.pack_start(dc_layers, False, False, 0)
        layers_box.pack_start(uw_layers, False, False, 0)
        layers_box.pack_start(it_layers, False, False, 0)
        layers_box.pack_start(ch_layers, False, False, 0)
        layers = gtk.Frame('Layers')
        layers.add(layers_box)
        
        toolbox = gtk.VBox(False)
        toolbox.set_size_request(224, 600)
        toolbox.pack_start(layers, False, False, 0)
        
        mainbox = gtk.HBox(False)
        mainbox.pack_start(scrolled_map, True, True)
        mainbox.pack_start(toolbox, False, False)
        
        # Build the statusbar
        self.statusbar = gtk.Statusbar()
        self.statusbar.push(0, 'Welcome...')
        
        
        vbox = gtk.VBox(False)
        vbox.pack_start(toolbar, False, False, 0)
        vbox.pack_start(mainbox, True, True, 0)
        vbox.pack_start(self.statusbar, False, False)
        
        self.add(vbox)
        
        self.show_all()
        
    def __print(self, widget, event):
        print 'scrolled', event.x, event.y, event.button
        
    def __toggle_layer(self, widget, layer):
        self._map.set_layer(layer, widget.get_active())
        
    def __close(self, widget, event):
        self.destroy()
        gtk.main_quit()
        
class LayerBox(gtk.HBox):
    def __init__(self, caption, group=None):
        gtk.HBox.__init__(self, False)
        self.toggle = gtk.ToggleButton('X')
        self.toggle.set_active(True)
        self.radio = gtk.RadioButton(group, caption)
        
        self.pack_start(self.toggle, False, False, 0)
        self.pack_start(self.radio, True, True, 0)
    
class TileHandler:
    def __init__(self):
        self.__tiles = {}
        
    def load(self, filename, tile_size, tileset_size):
        tilepath = os.path.realpath(os.path.join(os.path.dirname(__file__),
        '..', 'data', 'images', filename))
        
        tilepixbuf = gtk.gdk.pixbuf_new_from_file(tilepath)
        tile_width = tileset_size[0]
        tile_height = tileset_size[1]
        
        for i in range(tile_height):
            for j in range(tile_width):
                index = (j + i) + ((tile_width -1) * i) + 1
                hindex = "%02d" % index
                tile = tilepixbuf.subpixbuf(j * tile_size[0], i * tile_size[1], tile_size[0], tile_size[1])
                self.__tiles[hindex] = tile
                del tile
        
    def get(self, index):
        return self.__tiles[index]
        
if __name__ == '__main__':
    m = MapEditor()
    gtk.main()
