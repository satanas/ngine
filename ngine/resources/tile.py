# -*- coding: utf-8 -*-
#===================================================
# 
# Submodule of Resources that handles tiled maps
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 26, 2010
#===================================================

import pygame

from ngine.resources import tools

class TileHandler:
    def __init__(self):
        self.__tiles = {}
        
    def load(self, filename, tile_size, tileset_size):
        filepath = tools.get_datafile_path('images', filename)
        try:
            self.tileset = pygame.image.load(filepath)
            if self.tileset.get_alpha():
                self.tileset = self.tileset.convert_alpha()
            else:
                self.tileset = self.tileset.convert()
        except Exception, message:
            raise SystemExit, message
        
        tile_width = tileset_size[0]
        tile_height = tileset_size[1]
        
        for i in range(tile_height):
            for j in range(tile_width):
                index = (j + i) + ((tile_width -1) * i) + 1
                hindex = "%02d" % index
                print hindex, j * tile_size[0], i * tile_size[1]
                tile = tools.get_image_at(self.tileset, j * tile_size[0], 
                    i * tile_size[1], tile_size[0], tile_size[1])
                self.__tiles[hindex] = tile
        
    def get(self, index):
        return self.__tiles[index]
