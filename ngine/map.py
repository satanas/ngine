# -*- coding: utf-8 -*-

#================================================
#
# Tiled Map handler
#
# Copyright (C) 2010  Wil Alvarez <wil.alejandro@gmail.com>
#
#===================================================

import pygame

from ngine.resources import tile
from ngine.resources import tools

class MapLoader:
    def __init__(self):
        self.events = []
        self.layers = {
            'background': None,
            'scrolling': None,
            'decorations': None,
            'unwalkable': None,
            'items': None,
            'characters': None,
        }
        self.width = 0
        self.height = 0
        self.tilewidth = 0
        self.tileheight = 0
    
    def __get_int_val(self, fd):
        return int(fd.readline().strip().split(' = ')[1])
        
    def __get_str_val(self, fd):
        return fd.readline().strip().split(' = ')[1]
        
    def __build_color(self, str_val):
        r = int(str_val.split(',')[0])
        g = int(str_val.split(',')[1])
        b = int(str_val.split(',')[2])
        return (r, g, b)
    
    def __process_background(self, fd):
        tilename = self.__get_str_val(fd)
        tsw = self.__get_int_val(fd)
        tsh = self.__get_int_val(fd)
        
        htile = tile.TileHandler()
        htile.load(tilename, self.get_tile_size(), (tsw, tsh))
        
        self.layers['background'] = pygame.Surface(self.get_size())
        self.layers['background'].fill(self.bgcolor)
        
        for i in range(self.height):
            row = fd.readline().strip().split(' ')
            for j in range(len(row)):
                if row[j] == '00': 
                    continue
                x_pos = j * self.tilewidth
                y_pos = i * self.tileheight
                self.layers['background'].blit(htile.get(row[j]), 
                    (x_pos, y_pos, self.tilewidth, self.tileheight), 
                    (0, 0, self.tilewidth, self.tileheight))
        
    def __process_decorations(self, fd):
        tilename = self.__get_str_val(fd)
        tsw = self.__get_int_val(fd)
        tsh = self.__get_int_val(fd)
        
        htile = tile.TileHandler()
        htile.load(tilename, self.get_tile_size(), (tsw, tsh))
        
        for i in range(self.height):
            row = fd.readline().strip().split(' ')
            for j in range(len(row)):
                if row[j] == '00': 
                    continue
                x_pos = j * self.tilewidth
                y_pos = i * self.tileheight
                self.layers['background'].blit(htile.get(row[j]), 
                    (x_pos, y_pos, self.tilewidth, self.tileheight), 
                    (0, 0, self.tilewidth, self.tileheight))
        
    def __process_scrolling(self, fd):
        self.layers['scrolling'] = Layer()
        filename = fd.readline().split(' = ')[1]
        self.image = tools.get_datafile_path('images', filename)
        
    def __process_unwalkable(self, fd):
        self.layers['unwalkable'] = []
        for i in range(self.height):
            line = fd.readline().strip().split(' ')
            row = []
            for j in range(len(line)):
                block = Tile(line[j], j, i, self.tilewidth, self.tileheight)
                row.append(block)
            self.layers['unwalkable'].append(row)
    
    def __process_characters(self, fd):
        self.layers['characters'] = []
        for i in range(self.height):
            line = fd.readline().strip().split(' ')
            row = []
            for j in range(len(line)):
                char = Tile(line[j], j, i, self.tilewidth, self.tileheight)
                row.append(char)
            self.layers['characters'].append(row)
    
    def __process_events(self, fd):
        event = fd.readline()
        while event != '':
            event = event.strip()
            self.events.append(Event(event.split()[0], 
                int(event.split()[1]) * self.tilewidth,
                int(event.split()[2]) * self.tileheight))
            event = fd.readline()
        
    def load(self, filename):
        filepath = tools.get_datafile_path('maps', filename)
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
        fd.readline().strip()
        
        header = fd.readline()
        while header != '':
            header = header.strip()
            if header == '[background]':
                self.__process_background(fd)
            elif header == '[decorations]':
                self.__process_decorations(fd)
            elif header == '[scrolling]':
                self.__process_scrolling(fd)
            elif header == '[unwalkable]':
                self.__process_unwalkable(fd)
            elif header == '[items]':
                pass
            elif header == '[characters]':
                self.__process_characters(fd)
            elif header == '[events]':
                self.__process_events(fd)
            fd.readline()
            header = fd.readline()
        
    def get_collide_bounds(self, x, y):
        try:
            top = True if self.layers['unwalkable'][y - 1][x].t_id == '00' else False
        except:
            top = False
        
        try:
            bottom = True if self.layers['unwalkable'][y + 1][x].t_id == '00' else False
        except:
            bottom = False
            
        try:
            left = True if self.layers['unwalkable'][y][x - 1].t_id == '00' else False
        except:
            left = False
            
        try:
            right = True if self.layers['unwalkable'][y][x + 1].t_id == '00' else False
        except:
            right = False
        
        return top, bottom, left, right
        
    def get_tile_size(self):
        return self.tilewidth, self.tileheight
    
    def get_size(self):
        return self.width * self.tilewidth, self.height * self.tileheight
    
class Layer:
    def __init__(self):
        self.data = []
        self.image = None
        self.tileset = None
        self.tilesetwidth = 0
        self.tilesetheight = 0

class Tile:
    def __init__(self, t_id, x, y, tilewidth, tileheight):
        self.t_id = t_id
        self.x = x
        self.y = y
        self.real_x = x * tilewidth
        self.real_y = y * tileheight
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False
        
    def set_collide_bounds(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        
class Event:
    ''' This class load events in full size coords '''
    def __init__(self, e_id, ex, ey):
        self.e_id = e_id
        self.x = ex
        self.y = ey
            
