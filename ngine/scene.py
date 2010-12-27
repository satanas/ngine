# -*- coding: utf-8 -*-
#================================================
#
# Represents a generic and basic game scene
#
# Copyright (C) 2010  Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 24, 2010
#===================================================

import pygame

from ngine import map
from ngine import camera
from ngine import resources

class Scene:
    def __init__(self, director, _input, gamedata):
        self.director = director
        self.gamedata = gamedata
        self._input = _input
        self.res = resources.Resources()
        self.camera =  camera.Camera(director.screen, gamedata.screen_res)
        self.cbg = CompositedBackground(gamedata.screen_res)
        self.screen = director.screen
        self.maploader = map.MapLoader()
        
    def _fade_in(self):
        pass
    
    def _fade_out(self):
        pass
        
    def set_backgrounds(self, bg1=None, bg2=None, bg3=None):
        if bg2:
            bg2 = self.res.bg.get(bg2)
        if bg3:
            bg3 = self.res.bg.get(bg3)
        self.cbg.set_backgrounds(bg1, bg2, bg3)
        
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
        
class CompositedBackground:
    ''' This class holds three bgs. The first must be of the world size, the
    second must be scrollable and the last one must be of the screen size '''
    def __init__(self, size, h_scrolling=True, v_scrolling=False):
        self.bg = [None, None, None]
        self.x_offset = 0
        self.y_offset = 0
        self.size = size
        self.ssize = (0, 0) # Scrolling size
        self.h_scrolling = h_scrolling
        self.v_scrolling = v_scrolling
        self.image = pygame.Surface(self.size)
        self.rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        self.color = (0, 0, 0)
        self.x_speed = 0
        
    def set_color(self, color):
        self.color = color
    
    def set_backgrounds(self, bg1=None, bg2=None, bg3=None):
        self.bg[0] = bg1
        self.bg[1] = bg2
        self.bg[2] = bg3
        
        if bg2:
            self.ssize = bg2.get_size()
        
    def scroll(self, x_speed=0, y_speed=0):
        if not self.bg[1]:
            return
        self.x_speed = x_speed
        
    def update(self, value=False):
        if value:
            self.x_offset += self.x_speed
            if (self.x_offset < -self.ssize[0]): 
                self.x_offset = 0
            if (self.x_offset > self.ssize[0]): 
                self.x_offset = 0
        self.x_speed = 0
        
    def draw(self):
        self.image.fill(self.color)
        
        if self.bg[0]: 
            self.image.blit(self.bg[0], (0,0), self.rect)
        if self.bg[1]: 
            self.image.blit(self.bg[1], (self.x_offset, 0))
            if self.x_offset < 0:
                x = self.x_offset + self.ssize[0]
            else:
                x = self.x_offset - self.ssize[0]
            self.image.blit(self.bg[1], (x, 0))
        if self.bg[2]: 
            self.image.blit(self.bg[2], (0,0))
        
        
