# -*- coding: utf-8 -*-
#===================================================
# 
# Holds a variety of game objects
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 22, 2010
#===================================================

import math
import pygame

class FallingObject:
    ''' This checks for the gravity effect '''
    def __init__(self):
        # Jump vars
        self.jump_speed = 0
        self.jumping = False
    
    # FIXME: Definir mejor estos valores de gravedad y velocidad de salto
    def check_gravity(self):
        # Gravity and Jumping
        if self.jump_speed < MAX_GRAVITY_SPEED:
            self.jump_speed += GRAVITY
        if self.jump_speed >= 4.5:
            self.jumping = True
        self.rect.move_ip(0, self.jump_speed)
        
class CollidableObject:
    ''' This class has all methods needed for any collidable object and trigger 
    events when collisions happens'''
    def __init__(self):
        pass
        
    def on_collide_top(self, object):
        ''' Override in child class'''
        pass
        
    def on_collide_bottom(self, object):
        ''' Override in child class'''
        pass
        
    def on_collide_left(self, object):
        ''' Override in child class'''
        pass
        
    def on_collide_right(self, object):
        ''' Override in child class'''
        pass

class PlatformObject(pygame.sprite.Sprite):
    ''' This class represents the base class for all the platform objects'''
    def __init__(self, top, bottom, left, right):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.killable = False
        self.moveable = False
        self.hide = False
        self.xdir = self.ydir = 0
        
        self.on_top = []
        self.on_bottom = []
        self.on_left = []
        self.on_right = []
        
        self._collide_top = top
        self._collide_bottom = bottom
        self._collide_left = left
        self._collide_right = right
        
    def __check_collide_top(self, object):
        if (object.rect.left < self.rect.right - 4) and \
        (object.rect.right > self.rect.left + 4) and \
        (object.jump_speed > 0):
            if (object.rect.bottom >= self.rect.top) and \
            (object.rect.bottom < (self.rect.bottom - 8)):
                object.rect.bottom = self.rect.top
                object.on_collide_top(self)
                self.activate_from_top()
                if (not object in self.on_top):
                    self.on_top.append(object)
        
    def __check_collide_bottom(self, object):
        if (object.rect.left < self.rect.right - 4) and \
        (object.rect.right > self.rect.left + 4) and \
        (object.jump_speed < 0):
            if (object.rect.top <= self.rect.bottom) and \
            (object.rect.bottom > self.rect.bottom):
                object.rect.top = self.rect.bottom
                object.on_collide_bottom(self)
                self.activate_from_bottom()
                if (object not in self.on_bottom):
                    self.on_bottom.append(object)
    
    def __check_collide_left(self, object):
        if (object.rect.bottom > self.rect.top) and \
        (object.rect.top < self.rect.bottom):
            if (self.rect.right >= object.rect.left > self.rect.left):
                object.rect.left = self.rect.right
                object.on_collide_left(self)
                self.activate_from_left()
        
    def __check_collide_right(self, object):
        if (object.rect.bottom > self.rect.top) and \
        (object.rect.top < self.rect.bottom):
            if (self.rect.right > object.rect.right >= self.rect.left):
                object.rect.right = self.rect.left
                object.on_collide_right(self)
                self.activate_from_right()
    
    def collide(self, object):
        if object in self.on_top: self.on_top.remove(object)
        if object in self.on_bottom: self.on_bottom.remove(object)
        
        if self._collide_top:
            self.__check_collide_top(object)
        if self._collide_bottom:
            self.__check_collide_bottom(object)
        if self._collide_left:
            self.__check_collide_left(object)
        if self._collide_right:
            self.__check_collide_right(object)
        
    def activate_from_top(self):
        ''' Override in child class'''
        pass
        
    def activate_from_bottom(self):
        ''' Override in child class'''
        pass
        
    def activate_from_left(self):
        ''' Override in child class'''
        pass
        
    def activate_from_right(self):
        ''' Override in child class'''
        pass
        
    def update_move(self, dx, dy):
        self.rect.move_ip(dx, dy)
        for object in self.on_top:
            object.rect.move_ip(dx, dy)
            
        for object in self.on_bottom:
            object.rect.move_ip(dx, dy)
        
class Actor(pygame.sprite.Sprite, CollidableObject):
    ''' This class represents the base class for all the character objects; npc
    players, etc'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        CollidableObject.__init__(self)
        
        self.image = None
        self.rect = None
        self.radius = 0
        self.jump_speed = 0
        self.jumping = False
        
    def set_image(self, image, position):
        self.image = image
        self.rect = self.image.get_rect(topleft = position)
        w = self.rect.width / 2
        h = self.rect.height / 2
        self.radius = math.sqrt(pow(w, 2) + pow(h, 2))
        #~ self.radius = math.ceil(math.sqrt(pow(16, 2) + pow(16, 2)))
        #~ self.image = pygame.Surface((32, 32))
        #~ pygame.draw.circle(self.image, (24,123, 97), (16,16), self.radius)
        #~ pygame.draw.line(self.image, (0,0,0), (0,16), (32,16), 1)
        #~ pygame.draw.line(self.image, (0,0,0), (16,0), (16,32), 1)
        #~ self.rect = self.image.get_rect(topleft = position)
