# -*- coding: utf-8 -*-
#===================================================
# 
# Holds the very basic game objects
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 22, 2010
#===================================================

import math
import pygame

from ngine import collisions

class SpriteObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = None
        self.rect = None
        self.old_pos = (0, 0)
        
        self.anim_frame = 0
        self.anim_delay = 2
        self.anim_array = []
        
    def set_image(self, image, position=None):
        self.image = image
        self.rect = self.image.get_rect(topleft = position)
        
    def set_array(self, images):
        self.anim_array = images
    
    def next_image(self, cyclic=True):
        limit = len(self.anim_array)
        index = self.anim_frame / self.anim_delay
        
        self.anim_frame += 1
        if index >= limit: 
            index = limit - 1
        
        self.image = self.anim_array[index]
        
        last_frame = False
        if (self.anim_frame >= (limit * self.anim_delay)):
            last_frame = True
            if cyclic:
                self.anim_frame = 0
                
        return last_frame
    
class FallingObject:
    ''' This checks for the gravity effect '''
    def __init__(self, gravity=0.7, max_gravity_speed=6):
        self.old_centerx = 0
        self.old_centery = 0
        self.jump_speed = 0
        self.jumping = False
        self.gravity = gravity
        self.max_gravity_speed = max_gravity_speed
        
        # FIXME: Definir mejor estos valores de gravedad y velocidad de salto
    
                    
class CollidableObject:
    ''' This class has all methods needed for any collidable object and trigger 
    events when collisions happens'''
    def __init__(self):
        self._rect = None
        self.radius = 0
        
    def set_relative_rect(self, width=None, height=None, top=None, left=None):
        if not self._rect:
            self._rect = self.image.get_rect(center=self.rect.center)
        
        if not width:
            self._rect.width = self.rect.width
        else:
            self._rect.width = width
        
        if not width:
            self._rect.height = self.rect.height
        else:
            self._rect.height = height
        
        if top:
            self._rect.top = top
        if left:
            self._rect.left = left
        
        w = self._rect.width / 2
        h = self._rect.height / 2
        self.radius = math.sqrt(pow(w, 2) + pow(h, 2))
    
    def update_relative_rect(self):
        self._rect.center = self.rect.center
        
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

class UnwalkableObject:
    ''' This class represents the base class for all the platform objects'''
    def __init__(self, top, bottom, left, right):
        self._collide_top = top
        self._collide_bottom = bottom
        self._collide_left = left
        self._collide_right = right
    
    def check_collide_top(self, obj):
        if self._collide_top:
            obj._set_position(bottom = self._rect.top)
            obj.on_collide_top(self)
    
    def check_collide_bottom(self, obj):
        if self._collide_bottom:
            obj._set_position(top = self._rect.bottom)
            obj.on_collide_bottom(self)
    
    def check_collide_left(self, obj):
        if self._collide_left:
            obj._set_position(right = self._rect.left)
            obj.on_collide_left(self)
    
    def check_collide_right(self, obj):
        if self._collide_right:
            obj._set_position(left = self._rect.right)
            obj.on_collide_right(self)

class Actor(SpriteObject, CollidableObject):
    ''' This class represents the base class for all the character objects; npc
    players, etc'''
    def __init__(self, unwalkable_group):
        SpriteObject.__init__(self)
        CollidableObject.__init__(self)
        
        self.jump_speed = 0
        self.jumping = False
        self.gravity = 0.7
        self.max_gravity_speed = 6
        
        self.xspeed = 1
        self.yspeed = 1
        self.xdir = 0
        self.ydir = 0
        self.last_xdir = 0
        self.last_ydir = 0
        self.unwalkable_group = unwalkable_group
        
    def _gravity_move(self):
        self.rect.move_ip(0, self.jump_speed)
        self.update_relative_rect()
        
    def _real_move(self, xdir, ydir):
        self.rect.move_ip(self.xspeed * xdir, self.yspeed * ydir)
        self.update_relative_rect()
        
    def _set_position(self, top=None, bottom=None, left=None, right=None):
        if top:
            self.rect.top = top
        if bottom:
            self.rect.bottom = bottom
        if left:
            self.rect.left = left
        if right:
            self.rect.right = right
        self.update_relative_rect()
    
    def move(self, xdir, ydir):
        self.on_move(xdir, ydir)
        self.xdir = xdir
        self.ydir = ydir
        self.last_xdir = xdir
        self.last_ydir = ydir
        
        if xdir < 0:
            self._real_move(xdir, 0)
            for obj in self.unwalkable_group:
                if collisions.check(self, obj):
                    obj.check_collide_right(self)
        elif xdir > 0:
            self._real_move(xdir, 0)
            for obj in self.unwalkable_group:
                if collisions.check(self, obj):
                    obj.check_collide_left(self)
        elif ydir < 0:
            self._real_move(0, ydir)
            for obj in self.unwalkable_group:
                if collisions.check(self, obj):
                    obj.check_collide_bottom(self)
        elif ydir > 0:
            self._real_move(0, ydir)
            for obj in self.unwalkable_group:
                if collisions.check(self, obj):
                    obj.check_collide_top(self)
        
        self.next_image()
        
    def check_gravity(self):
        if self.jump_speed < self.max_gravity_speed:
            self.jump_speed += self.gravity
        if self.jump_speed >= 4.5:
            self.jumping = True
            self.on_falling()
        
        self._gravity_move()
        for obj in self.unwalkable_group:
            if collisions.check(self, obj):
                obj.check_collide_top(self)
    
    def jump(self):
        pass
        
    def on_move(self, xdir, ydir):
        raise NotImplemented
    
    def on_falling(self):
        pass
        
