# -*- coding: utf-8 -*-
#================================================
#
# Represents a generic and basic game scene
#
# Copyright (C) 2010  Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 24, 2010
#===================================================

from ngine import camera
from ngine import resources

class Scene:
    def __init__(self, director, _input, gamedata):
        self.director = director
        self.gamedata = gamedata
        self._input = _input
        self.res = resources.Resources()
        self.camera =  camera.Camera(director.screen, gamedata.screen_res)
        self.screen = director.screen
        
    def _fade_in(self):
        pass
    
    def _fade_out(self):
        pass
        
    def load(self):
        self._on_load()
        self._fade_in()
    
    def unload(self):
        self._fade_out()
        self._on_unload()
        
    def _on_load(self):
        raise NotImplemented
    
    def _on_unload(self):
        raise NotImplemented
    
    def handle_events(self):
        ''' Input events should be checked here. Return True if you want to
        exit game. False otherwise '''
        raise NotImplemented
        
    def check_collisions(self):
        raise NotImplemented
    
    def update(self):
        ''' Camera should be updated here '''
        raise NotImplemented
    
    def draw(self):
        ''' Camera should draw groups here '''
        raise NotImplemented
        
    
            
        
