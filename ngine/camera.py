# -*- coding: utf-8 -*-
#===================================================
# 
# camera.py - A module that let you create a 2D side-scrolling camera with some
# optimizations
#
# Copyright (C) 2008 - 2010  Wil Alvarez <wil.alejandro@gmail.com>
#
#===================================================

import math
import pygame

from ngine import collisions
from ngine.resources import background

# Alignment Constants
CENTER = 0x11
TOPLEFT = 0x12

# Scrolling Constants
SCROLL_NONE = 0x13
SCROLL_HORIZONTAL = 0x14
SCROLL_VERTICAL = 0x15
SCROLL_BOTH = 0x16

# Pan speed constants
SLOW_PAN_STEP = 6
MID_PAN_STEP = 12
FAST_PAN_STEP = 24

class Camera:
    def __init__(self, screen, world_size, bg_color=(0,0,0)):
        self.rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        self.old_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        w = self.rect.width / 2
        h = self.rect.height / 2
        self.radius = math.sqrt(pow(w, 2) + pow(h, 2))
        self.screen = screen
        self.target = None
        self.world_size = world_size
        self.panning = False
        self.pan_pos = (0,0)
        self.pan_align = None
        self.pan_speed = SLOW_PAN_STEP
        self.locked = False
        self.last_target_pos = (0,0)
        self.bg_color = bg_color
        
    def __watch_edges(self):
        # Watching for the world edges
        if (self.rect.top < 0): 
            self.rect.top = 0
        elif (self.rect.top > self.world_size[1] - self.rect.h): 
            self.rect.top = self.world_size[1] - self.rect.h
            
        if (self.rect.left < 0): 
            self.rect.left = 0
        elif (self.rect.left > self.world_size[0] - self.rect.w): 
            self.rect.left = self.world_size[0] - self.rect.w
    
    def lock(self):
        self.locked = True
        
    def unlock(self, pan=False):
        if (pan is True) and (self.target is not None):
            self.panning = True
            self.pan_pos = self.target.rect.center
        self.locked = False
        
    def pan_to_pos(self, pos, align=CENTER):
        self.panning = True
        testrect = pygame.Rect(0,0,self.rect.w, self.rect.h)
        
        if (align == CENTER): 
            testrect.center = pos
            testrect = self.__watch_edges(testrect)
            self.pan_pos = testrect.center
        elif (align == TOPLEFT): 
            testrect.topleft = pos
            testrect = self.__watch_edges(testrect)
            self.pan_pos = testrect.topleft
        self.pan_align = align
        
    def move_to_pos(self, pos, align=CENTER):
        testrect = pygame.Rect(0,0,self.rect.w, self.rect.h)
        
        if (align == CENTER): 
            testrect.center = pos
            testrect = self.__watch_edges(testrect)
            self.rect.center = testrect.center
        elif (align == TOPLEFT): 
            testrect.topleft = pos
            testrect = self.__watch_edges(testrect)
            self.rect.topleft = testrect.topleft
            
    def move_to_rel(self, dx, dy, align=CENTER):
        testrect = pygame.Rect(0,0,self.rect.w, self.rect.h)
        
        if (align == CENTER): 
            testrect.center = (self.rect.centerx + dx, self.rect.centery + dy)
            testrect = self.__watch_edges(testrect)
            self.rect.center = testrect.center
        elif (align == TOPLEFT): 
            testrect.topleft = (self.rect.left + dx, self.rect.top + dy)
            testrect = self.__watch_edges(testrect)
            self.rect.topleft = testrect.topleft
    
    def set_target(self, sprite, pan=False):
        """ Used to set the target that camera must follow"""
        self.target = sprite
        self.unlock(pan)
    
    def clear_target(self):
        """ Used to clear the target sprite """
        self.target = None
    
    def is_on_screen(self, sprite):
        """This is used mainly to draw just when sprite is on screen"""
        return collisions.check(self, sprite)
        
    def update(self):
        updatebg2 = False
        self.old_rect.topleft = self.rect.topleft
        
        # If camera is fixed it won't move
        if self.locked:
            pass
        # Soft camera movement (Panning)
        elif self.panning:
            if (self.pan_align == CENTER):
                if (self.rect.centerx < self.pan_pos[0]): 
                    self.rect.centerx += self.pan_speed
                    if (self.rect.centerx > self.pan_pos[0]): 
                        self.rect.centerx = self.pan_pos[0]
                elif (self.rect.centerx > self.pan_pos[0]): 
                    self.rect.centerx -= self.pan_speed
                    if (self.rect.centerx < self.pan_pos[0]): 
                        self.rect.centerx = self.pan_pos[0]
                
                if(self.rect.centery < self.pan_pos[1]): 
                    self.rect.centery += self.pan_speed
                    if (self.rect.centery > self.pan_pos[1]): 
                        self.rect.centery = self.pan_pos[1]
                elif(self.rect.centery > self.pan_pos[1]): 
                    self.rect.centery -= self.pan_speed
                    if (self.rect.centery < self.pan_pos[1]): 
                        self.rect.centery = self.pan_pos[1]
                
                if (self.rect.centerx == self.pan_pos[0]) and \
                    (self.rect.centery == self.pan_pos[1]): 
                    self.panning = False
                
            elif (self.pan_align == TOPLEFT):
                if(self.rect.left < self.pan_pos[0]): 
                    self.rect.left += self.pan_speed
                    if (self.rect.left > self.pan_pos[0]): 
                        self.rect.left = self.pan_pos[0]
                elif(self.rect.left > self.pan_pos[0]): 
                    self.rect.left -= self.pan_speed
                    if (self.rect.left < self.pan_pos[0]): 
                        self.rect.left = self.pan_pos[0]
                
                if(self.rect.top < self.pan_pos[1]): 
                    self.rect.top += self.pan_speed
                    if (self.rect.top > self.pan_pos[1]): 
                        self.rect.top = self.pan_pos[1]
                elif(self.rect.top > self.pan_pos[1]): 
                    self.rect.top -= self.pan_speed
                    if (self.rect.top < self.pan_pos[1]): 
                        self.rect.top = self.pan_pos[1]
                
                if (self.rect.left == self.pan_pos[0]) and \
                    (self.rect.top == self.pan_pos[1]): 
                    self.panning=False
        # Normal movement
        elif self.target and self.last_target_pos != self.target.rect.center:
            self.last_target_pos = self.target.rect.center
            self.rect.center = self.target.rect.center
            updatebg2 = True
            
        self.__watch_edges()
        return self.rect.left != self.old_rect.left and updatebg2
        
    def clear(self):
        self.screen.fill(self.bg_color)
    
    def draw_background(self, image):
        self.screen.blit(image, (0,0))
    
    def draw_groups(self, groups_list):
        for group in groups_list:
            for s in group.sprites():
                if self.is_on_screen(s):
                    x = s.rect.left-self.rect.left
                    y = s.rect.top-self.rect.top
                    self.screen.blit(s.image, (x, y, s.rect.width, s.rect.height))
    
