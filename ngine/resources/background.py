# -*- coding: utf-8 -*-
#===================================================
# 
# Submodule of Resources that handles background images
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 11, 2010
#===================================================

import pygame

from ngine.resources import tools

class BackgroundHandler:
    def __init__(self):
        self.__files = {}
        
    def load(self, images):
        for filename in images:
            key = filename.split('.')[0]
            filepath = tools.get_datafile_path('backgrounds', filename)
            try:
                bg = pygame.image.load(filepath)
                bg.set_colorkey((0, 0, 0), pygame.locals.RLEACCEL)
                bg = bg.convert_alpha()
            except Exception, message:
                raise SystemExit, message
            self.__files[key] = bg
            
    def get(self, key):
        return self.__files[key]
