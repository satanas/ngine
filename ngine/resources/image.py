# -*- coding: utf-8 -*-
#===================================================
# 
# Submodule of Resources that handles images
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 11, 2010
#===================================================

import pygame

from ngine.resources import tools

class ImageHandler:
    def __init__(self):
        self.__files = {}
        
    def load(self, images):
        for filename in images:
            key = filename.split('.')[0]
            filepath = tools.get_datafile_path('images', filename)
            try:
                image = pygame.image.load(filepath)
                if image.get_alpha():
                    image = image.convert_alpha()
                else:
                    image = image.convert()
            except Exception, message:
                raise SystemExit, message
            self.__files[key] = image
            
    def get(self, key):
        return self.__files[key]
