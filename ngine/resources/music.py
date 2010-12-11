# -*- coding: utf-8 -*-
#===================================================
# 
# Submodule of Resources that handles music effects
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 11, 2010
#===================================================

import pygame

from ngine.resources import tools

class MusicHandler:
    def __init__(self):
        pygame.mixer.init()
        self.__files = {}
        self.current = None
        
    def load(self, musics):
        for filename in musics:
            key = filename.split('.')[0]
            filepath = tools.get_datafile_path('music', filename)
            self.__files[key] = filepath
            
    def play(self, key):
        if not pygame.mixer:
            return NoneMusic()
        try:
            pygame.mixer.music.load(self.__files[key])
            pygame.mixer.music.play(-1)
        except Exception, message:
            raise SystemExit, message
    
    def stop(self):
        pygame.mixer.music.stop()
        
    def fadeout(self, delay=2500):
        pygame.mixer.music.fadeout(delay)
        
    def change(self, new_key, fadeout=True, delay=2500):
        if fadeout:
            self.fadeout(delay)
        else:
            self.stop()
        self.play(new_key)
        
class NoneMusic:
    def play(self): 
        pass
