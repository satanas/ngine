# -*- coding: utf-8 -*-
#===================================================
# 
# Submodule of Resources that handles sound effects
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 11, 2010
#===================================================

import pygame

from ngine.resources import tools

class SoundHandler:
    def __init__(self):
        pygame.mixer.init()
        self.__files = {}
        
    def load(self, sounds):
        for filename in sounds:
            if not pygame.mixer:
                self.__files[key] = NoneSound()
            else:
                key = filename.split('.')[0]
                filepath = tools.get_datafile_path('sounds', filename)
                try:
                    sound = pygame.mixer.Sound(filepath)
                except Exception, message:
                    sound = NoneSound()
                self.__files[key] = sound
            
    def play(self, key):
        self.__files[key].play()
        
class NoneSound:
    def play(self): 
        pass
