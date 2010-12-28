# -*- coding: utf-8 -*-
#================================================
#
# Represents a generic and basic game scene
#
# Copyright (C) 2010  Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 24, 2010
#===================================================
import time
import pygame

from ngine import map
from ngine import camera
from ngine import resources
from ngine.resources import tools

class Scene:
    def __init__(self, director, _input, gamedata):
        self.director = director
        self.gamedata = gamedata
        self._input = _input
        self.res = resources.Resources()
        self.camera =  camera.Camera(director.screen, gamedata.screen_res)
        self.screen = director.screen
        self.maploader = map.MapLoader()
        self.groups_to_draw = []
        
        # Background Layers
        self._bg1 = None
        self._bg2 = None
        self._bg3 = None
        # Background Composited
        self.bg = pygame.Surface(gamedata.screen_res, pygame.HWSURFACE)
        self.bg_color = (0,0,0)
        
        # Scrolling stuffs
        self.x_offset = 0
        self.x_scrolling = False
        self.x_speed = 0
        self.x_dir = 0
        self.x_limit = 0
        
    def __update_scrolling(self, update):
        if update:
            self.x_offset += (self.x_speed * self.x_dir)
            if (self.x_offset < -self.x_limit): 
                self.x_offset = 0
            if (self.x_offset > self.x_limit): 
                self.x_offset = 0
        self.x_dir = 0
        
    def __composite_background(self):
        self.bg.fill(self.bg_color)
        
        if self._bg1:
            x_pos, y_pos = self.camera.rect.topleft
            width, height = self.bg.get_size()
            self.bg.blit(self._bg1, (0, 0, width, height), (x_pos, y_pos, width, height))
        
        if self._bg2: 
            self.bg.blit(self._bg2, (self.x_offset, 0))
            if self.x_offset < 0:
                x = self.x_offset + self.x_limit
            else:
                x = self.x_offset - self.x_limit
            self.bg.blit(self._bg2, (x, 0))
        
        if self._bg3: 
            self.bg.blit(self._bg3, (0,0))
                    
    def append_to_draw(self, group):
        self.groups_to_draw.append(group)
        
    def on_loaded_map(self):
        self.camera.world_size = self.maploader.get_size()
        self.bg_color = self.maploader.bgcolor
        if self.maploader.scrolling > 0:
            self.x_scrolling = True
            self.x_speed = self.maploader.scrolling
    
    def set_camera_target(self, target):
        self.camera.set_target(target)
    
    def set_backgrounds(self, bg1=None, bg2=None, bg3=None):
        self._bg1 = bg1
        if bg2:
            self._bg2 = self.res.bg.get(bg2)
            self.x_limit = self._bg2.get_size()[0]
        if bg3:
            self._bg3 = self.res.bg.get(bg3)
        
    def scroll_bg(self, x_dir):
        if not self._bg2:
            return
        self.x_dir = x_dir
        
    def load(self):
        self.on_load()
        self._fade_in()
        
    def unload(self):
        self._fade_out()
        self.on_unload()
        
    def update(self):
        self.on_update()
        scroll = self.camera.update()
        self.__update_scrolling(scroll)
        
    def draw(self):
        self.__composite_background()
        self.camera.draw_background(self.bg)
        self.camera.draw_groups(self.groups_to_draw)
        self.on_draw()
    
    # ------------------------------------------------------------
    # Transition effects
    # ------------------------------------------------------------
    
    def _fade_in(self):
        pass
        
    def _fade_out(self):
        pass
    
    # ------------------------------------------------------------
    # Methods to overwrite
    # ------------------------------------------------------------
    
    def handle_events(self):
        ''' Input events should be checked here. Return True if you want to
        exit game. False otherwise '''
        raise NotImplemented
        
    def check_collisions(self):
        ''' Detect all your collisions and do something about it '''
        raise NotImplemented
    
    def on_load(self):
        ''' Load all resources here '''
        raise NotImplemented
    
    def on_unload(self):
        ''' Unload all resources here '''
        raise NotImplemented
        
    def on_update(self):
        ''' Update all your sprites here '''
        raise NotImplemented
    
    def on_draw(self):
        ''' Overwrite if necessary '''
        pass
        
