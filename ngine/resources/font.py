# -*- coding: utf-8 -*-
#===================================================
# 
# Submodule of Resources that handles fonts
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 11, 2010
#===================================================

import pygame

from ngine.resources import tools

class FontHandler:
    def __init__(self):
        pygame.font.init()
        self.__files = {}
    '''
    def load(self, fonts):
        for filename in fonts:
            key = filename.split('.')[0]
            filepath = tools.get_datafile_path('fonts', filename)
            self.__files[key] = filepath
    '''
    def load(self, filename, size, color, bold=False):
        key = filename.split('.')[0]
        filepath = tools.get_datafile_path('fonts', filename)
        self.__files[key] = [pygame.font.Font(filepath, size), color, bold]
            
    def load_default(self, key, size, color, bold=False):
        self.__files[key] = [pygame.font.Font(None, size), color, bold]
    
    def render(self, key, text):
        try:
            font = self.__files[key][0]
            color = self.__files[key][1]
            bold = self.__files[key][2]
            
            if bold: 
                font.set_bold(1)
            
            rtext = font.render(text, 1, color)
        except Exception, message:
            raise SystemExit, message
        
        return rtext
            
            
            
            
            
            
	
	return font.render(text, 1, color)
	
def rendertextsha(text, color, shadow_color, font, bold=False, aa=1):
	'''
	Returns a rendered font
	'''

	if bold: font.set_bold(1)
	
	return font.render(text, 1, color), font.render(text, 1, shadow_color)
