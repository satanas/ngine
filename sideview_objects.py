# -*- coding: utf-8 -*-

#================================================
#
# Dummy Objects for the Side-View Example (please execute sideview_example.py)
#
# Copyright (C) 2011  Wil Alvarez <wil.alejandro@gmail.com>
#
#===================================================

import pygame

from ngine import objects
from ngine.resources import tools

# A class that represent a little square box on screen
class Tux(objects.Actor, objects.FallingObject):
    def __init__(self, res, pos, group):
        objects.Actor.__init__(self, group)
        objects.FallingObject.__init__(self)
        #self.res = res
        
        ckey = (0, 255, 0)
        orig = res.image.get('tux')
        self.right_array = [
            tools.get_image_at(orig, 32, 0, 32, 32, ckey),
            tools.get_image_at(orig, 64, 0, 32, 32, ckey),
            tools.get_image_at(orig, 96, 0, 32, 32, ckey),
        ]
        self.left_array = [
            tools.get_image_at(orig, 32, 32, 32, 32, ckey),
            tools.get_image_at(orig, 64, 32, 32, 32, ckey),
            tools.get_image_at(orig, 96, 32, 32, 32, ckey),
        ]
        self.right_image = tools.get_image_at(orig, 0, 0, 32, 32, ckey)
        self.left_image = tools.get_image_at(orig, 128, 32, 32, 32, ckey)
        self.jump_right_image = tools.get_image_at(orig, 128, 0, 32, 32, ckey)
        self.jump_left_image = tools.get_image_at(orig, 0, 32, 32, 32, ckey)
        
        self.xspeed = 3
        self.yspeed = 2
        self.anim_delay = 4
        
        self.set_image(self.right_image, pos)
        self.set_relative_rect()
        self.set_array(self.right_array)
        self.last_xdir = 1
        
    def on_move(self, xdir, ydir):
        if xdir < 0:
            self.set_array(self.left_array)
        elif xdir > 0:
            self.set_array(self.right_array)
        
    def on_collide_top(self, object):
        self.jumping = False
        self.jump_speed = 0
        
    def jump(self):
        if not self.jumping:
            self.jump_speed = -11
            self.jumping = True
            
    def update(self):
        self.check_gravity()
        if self.xdir == 0 and self.ydir == 0:
            if self.last_xdir < 0:
                self.image = self.left_image
            elif self.last_xdir > 0:
                self.image = self.right_image
        if self.jumping:
            if self.last_xdir < 0:
                self.image = self.jump_left_image
            elif self.last_xdir > 0:
                self.image = self.jump_right_image
        self.xdir = 0
        self.ydir = 0

# A class that represent a little square box on screen
class Platform(objects.SpriteObject, objects.CollidableObject, objects.UnwalkableObject):
    def __init__(self, res, id, pos, top, bottom, left, right):
        objects.SpriteObject.__init__(self)
        objects.CollidableObject.__init__(self)
        objects.UnwalkableObject.__init__(self, top, bottom, left, right)
        self.res = res
        
        image = pygame.Surface((24, 24))
        image.fill((255,255,0))
        orig = self.res.image.get('ice-ground')
        if id == '01':
            image = tools.get_image_at(orig, 0, 0, 24, 24)
        elif id == '02':
            image = tools.get_image_at(orig, 24, 0, 24, 24)
        elif id == '03':
            image = tools.get_image_at(orig, 48, 0, 24, 24)
        elif id == '04':
            image = tools.get_image_at(orig, 0, 24, 24, 24)
        elif id == '05':
            image = tools.get_image_at(orig, 24, 24, 24, 24)
        elif id == '06':
            image = tools.get_image_at(orig, 48, 24, 24, 24)
        elif id == '07':
            image = tools.get_image_at(orig, 0, 48, 24, 24)
        elif id == '08':
            image = tools.get_image_at(orig, 24, 48, 24, 24)
        elif id == '09':
            image = tools.get_image_at(orig, 48, 48, 24, 24)
        self.set_image(image, pos)
        self.set_relative_rect()

class Coin(objects.SpriteObject, objects.CollidableObject):
    def __init__(self, res, pos):
        objects.SpriteObject.__init__(self)
        objects.CollidableObject.__init__(self)
        
        self.anim_delay = 5
        
        ckey = (0, 255, 0)
        orig = res.image.get('coin24')
        array = [
            tools.get_image_at(orig, 0, 0, 24, 24, ckey),
            tools.get_image_at(orig, 24, 0, 24, 24, ckey),
            tools.get_image_at(orig, 48, 0, 24, 24, ckey),
            tools.get_image_at(orig, 72, 0, 24, 24, ckey),
        ]
        
        self.set_image(array[0], pos)
        self.set_relative_rect()
        self.set_array(array)
    
    def update(self):
        self.next_image()
