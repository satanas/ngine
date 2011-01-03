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

class SpriteObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = None
        self.rect = None
        self._rect = None
        self.radius = 0
        self.xspeed = 1
        self.yspeed = 1
        self.xdir = 0
        self.ydir = 0
        self.last_xdir = 0
        self.last_ydir = 0
        self.old_pos = (0, 0)
        
        self.anim_frame = 0
        self.anim_delay = 2
        self.anim_array = []
        #self.jump_speed = 0
        #self.jumping = False
        
    def set_image(self, image, position=None):
        self.image = image
        self.rect = self.image.get_rect(topleft = position)
        self._rect = self.image.get_rect(topleft = position)
        w = self._rect.width / 2
        h = self._rect.height / 2
        self.radius = math.sqrt(pow(w, 2) + pow(h, 2))
        
    def set_relative_rect(self, width, height, top=None, left=None):
        self._rect.width = width
        self._rect.height = height
        if top:
            self._rect.top = top
        if left:
            self._rect.left = left
        
        w = self._rect.width / 2
        h = self._rect.height / 2
        self.radius = math.sqrt(pow(w, 2) + pow(h, 2))
    
    def move(self, xdir, ydir):
        self.on_move(xdir, ydir)
        self.xdir = xdir
        self.ydir = ydir
        self.last_xdir = xdir
        self.last_ydir = ydir
        self.old_pos = self.rect.topleft
        self.rect.move_ip(self.xspeed * xdir, self.yspeed * ydir)
        self.next_image()
        
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
        
    def on_move(self, xdir, ydir):
        raise NotImplemented
    
class FallingObject:
    ''' This checks for the gravity effect '''
    def __init__(self, gravity=0.7, max_gravity_speed=13):
        # Jump vars
        self.jump_speed = 0
        self.jumping = False
        self.gravity = gravity
        self.max_gravity_speed = max_gravity_speed
        
    # FIXME: Definir mejor estos valores de gravedad y velocidad de salto
    def check_gravity(self):
        # Gravity and Jumping
        if self.jump_speed < self.max_gravity_speed:
            self.jump_speed += self.gravity
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

class UnwalkableObject:
    ''' This class represents the base class for all the platform objects'''
    def __init__(self, top, bottom, left, right):
        self._collide_top = top
        self._collide_bottom = bottom
        self._collide_left = left
        self._collide_right = right
        
    def __is_xaligned(self, obj):
        if obj.rect.right > self._rect.left and obj.rect.left < self._rect.right:
            return True
        return False
        
    def __is_yaligned(self, obj):
        if obj.rect.bottom > self._rect.top and obj.rect.top < self._rect.bottom:
            return True
        return False
        
    def __in_top_threshold(self, obj):
        if obj.rect.bottom > self._rect.top and obj.rect.bottom < self.t_limit:
            return True
        return False
        
    def __in_bottom_threshold(self, obj):
        if obj.rect.top < self._rect.bottom and obj.rect.top > self.b_limit:
            return True
        return False
    
    def __in_left_threshold(self, obj):
        if obj.rect.right > self._rect.left and obj.rect.right < self.l_limit:
            return True
        return False
        self._rect.right >= object.rect.left > self._rect.left
        
    def __in_right_threshold(self, obj):
        if obj.rect.left < self._rect.right and obj.rect.left > self.r_limit:
            return True
        return False
        
    def __in_unknown_area(self, obj):
        x_inside = self.r_limit > self._rect.x > self.l_limit
        y_inside = self.b_limit > self._rect.y > self.t_limit
        
        if x_inside and y_inside:
            return True
        return False
    
    def __check_collide_top(self, object):
        if not self.__is_xaligned(object):
            return
        if self.__in_top_threshold(object):
            object.rect.bottom = self._rect.top
            object.on_collide_top(self)
            #object.landing()
        
    def __check_collide_bottom(self, object):
        if not self.__is_xaligned(object):
            return
        if self.__in_bottom_threshold(object):
            object.rect.top = self._rect.bottom
            object.on_collide_bottom(self)
            # stop jump
            
    def __check_collide_left(self, object):
        if not self.__is_yaligned(object):
            return
        if self.__in_left_threshold(object):
            object.rect.right = self._rect.left
            object.on_collide_left(self)
        
    def __check_collide_right(self, object):
        if not self.__is_yaligned(object):
            return
        if self.__in_right_threshold(object):
            object.rect.left = self._rect.right
            object.on_collide_right(self)
        
    def collide(self, object):
        if self.__in_unknown_area(object):
            object.topleft = self.old_pos
            return 
        if self._collide_top:
            self.__check_collide_top(object)
        if self._collide_bottom:
            self.__check_collide_bottom(object)
        if self._collide_left:
            self.__check_collide_left(object)
        if self._collide_right:
            self.__check_collide_right(object)
        object.xdir = 0
        object.ydir = 0
        
    def set_limits(self):
        self.t_limit = self._rect.top + 4
        self.b_limit = self._rect.bottom - 4
        self.l_limit = self._rect.left + 4
        self.r_limit = self._rect.right - 4
        
class Actor(SpriteObject, CollidableObject):
    ''' This class represents the base class for all the character objects; npc
    players, etc'''
    def __init__(self):
        SpriteObject.__init__(self)
        CollidableObject.__init__(self)
        
        
