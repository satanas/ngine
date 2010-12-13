# -*- coding: utf-8 -*-
#===================================================
# 
# camera.py - A module that let you create a 2D side-scrolling camera with some
# optimizations
#
# Copyright (C) 2008  Wil Alvarez <wil_alejandro@yahoo.com>
#
# This PACKAGE is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software 
# Foundation; either version 3 of the License, or (at your option) any later
# version.
# This PACKAGE is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License 
# for more details.
#
# You should have received a copy of the GNU General Public License along with 
# this PACKAGE (see COPYING); if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#===================================================

import pygame

PROXIMITY = 16 # Maximum value to consider if a sprite is near the target
BG_COLOR = (0,0,0)

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

from ngine.resources import background

class Camera:
    def __init__(self, screen, world_size, bg_color=None):
        self.rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        self.screen = screen
        self.target = None
        self.world_size = world_size
        self.panning = False
        self.pan_pos = (0,0)
        self.pan_align = None
        self.pan_speed = SLOW_PAN_STEP
        self.locked = False
        self.last_target_pos = (0,0)
        global BG_COLOR
        if (bg_color is not None): BG_COLOR = bg_color
        
        self.bg1 = None
        self.bg2 = None
        self.bg3 = None
        self.bgh = background.BackgroundHandler()
        
    def __watch_edges(self, rect):
        # Watching for the world edges
        if (rect.top < 0): 
            rect.top = 0
        elif (rect.top > self.world_size[1]-rect.h): 
            rect.top = self.world_size[1]-rect.h
            
        if (rect.left < 0): 
            rect.left = 0
        elif (rect.left > self.world_size[0]-rect.w): 
            rect.left = self.world_size[0]-rect.w
        
        return rect
        
    def __update_bgs(self, updatebg2):
        self.clear()
        
        if (self.bg1 is not None): 
            self.screen.blit(self.bg1, (0,0))
        if (self.bg2 is not None and updatebg2): 
            self.bg2.scroll()
        elif (self.bg2 is not None and not updatebg2): 
            self.bg2.update()
        if (self.bg3 is not None): 
            self.screen.blit(self.bg3, (0,0), self.rect)
        
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
        
    def set_backgrounds(self, bg1=None, bg2=None, bg3=None):
        if bg1: 
            #self.bg1 = loadpng(bg1)
            key = bg1.split('.')[0]
            print 'key1', key
            self.bgh.load([bg1])
            self.bg1 = self.bgh.get(key)
        if bg2:
            key = bg2.split('.')[0]
            print 'key2', key
            self.bgh.load([bg2])
            self.bg2 = ScrollingImage(self.screen, self.bgh.get(key), -5, (0,0))
        if (bg3 is not None): 
            #self.bg3 = loadpng(bg3)
            key = bg3.split('.')[0]
            print 'key3', key
            self.bgh.load([bg3])
            self.bg3 = self.bgh.get(key)
        
    def set_target(self, sprite, pan=False):
        """ Used to set the target that camera must follow"""
        self.target = sprite
        self.unlock(pan)

    def clear_target(self):
        """ Used to clear the target sprite """
        self.target = None
        
    def is_on_screen(self, sprite):
        """This is used mainly to check collisions just when sprite is on 
        screen"""
        return self.rect.colliderect(sprite.rect)
        
    def is_near_target(self, sprite):
        """ Verify is a sprite is near the target (according to proximity 
        value) """
        if self.target==None: return False
        
        proxrect = pygame.Rect(0,0, self.target.rect.width+PROXIMITY, 
            self.target.rect.height+PROXIMITY)
        proxrect.center = self.target.rect.center
        
        return proxrect.colliderect(sprite.rect)
        
    def is_near_sprite(self, sprite1, sprite2):
        """ Verify is sprite1 is near sprite2 (according to proximity 
        value) """
        proxrect = pygame.Rect(0,0, sprite1.rect.width+PROXIMITY, 
            sprite1.rect.height+PROXIMITY)
        proxrect.center = sprite1.rect.center
        
        return proxrect.colliderect(sprite2.rect)
        
    def update(self):
        updatebg2 = False
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
        elif (self.target is not None) and \
            (self.last_target_pos != self.target.rect.center):
            self.last_target_pos = self.target.rect.center
            self.rect.center = self.target.rect.center
            updatebg2 = True
        
        self.rect = self.__watch_edges(self.rect)
        self.__update_bgs(updatebg2)
        
    def clear(self):
        self.screen.fill(BG_COLOR)

    def draw_groups(self, groups_list):
        for group in groups_list:
            for s in group.sprites():
                if self.is_on_screen(s):
                    self.screen.blit(s.image, (s.rect.left-self.rect.left, 
                        s.rect.top-self.rect.top, s.rect.width, s.rect.height))

class ScrollingImage:
    def __init__(self, screen, picture, speed, pos):
        self.screen = screen
        self.speed = speed
        self.image = picture
        rect = self.image.get_rect()
        self.size = (rect.width, rect.height)
        self.pos = pos
        self.offset = 0
        
    def scroll(self):
        self.screen.blit(self.image, (self.offset, self.pos[1]))
        self.screen.blit(self.image, (self.offset+self.size[0], self.pos[1]))
        self.offset += self.speed
        if (self.offset < -self.size[0]): self.offset=0

    def update(self):
        self.screen.blit(self.image, (self.offset, self.pos[1]))
        self.screen.blit(self.image, (self.offset+self.size[0], self.pos[1]))

def loadpng(name):
	""" Load image and return image object"""
	#fullname = os.path.join('data', 'images', name)
	fullname = name
	try:
		image = pygame.image.load(fullname)
		if image.get_alpha() is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	except pygame.error, message:
		print 'Cannot load image:', fullname
		raise SystemExit, message
	return image
