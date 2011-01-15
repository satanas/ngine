# -*- coding: utf-8 -*-

#================================================
#
# Dummy Objects for the Top-View Example (please execute topview_example.py)
#
# Copyright (C) 2010  Wil Alvarez <wil.alejandro@gmail.com>
#
#===================================================

import pygame

from ngine import objects
from ngine.resources import tools

# A class that represent a little square box on screen
class Tux(objects.Actor):
    def __init__(self, res, pos, group):
        objects.Actor.__init__(self, group)
        self.res = res
        
        ckey = (0,255, 0)
        orig = self.res.image.get('tux')
        self.front_array = [
            tools.get_image_at(orig, 0, 64, 32, 32, ckey),
            tools.get_image_at(orig, 32, 64, 32, 32, ckey),
            tools.get_image_at(orig, 64, 64, 32, 32, ckey),
        ]
        self.back_array = [
            tools.get_image_at(orig, 0, 96, 32, 32, ckey),
            tools.get_image_at(orig, 32, 96, 32, 32, ckey),
            tools.get_image_at(orig, 64, 96, 32, 32, ckey),
        ]
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
        self.front_image = tools.get_image_at(orig, 0, 64, 32, 32, ckey)
        self.back_image = tools.get_image_at(orig, 0, 96, 32, 32, ckey)
        self.right_image = tools.get_image_at(orig, 0, 0, 32, 32, ckey)
        self.left_image = tools.get_image_at(orig, 128, 32, 32, 32, ckey)
        
        self.xspeed = 2.5
        self.yspeed = 2.5
        self.anim_delay = 8
        
        self.set_image(self.front_image, pos)
        self.set_relative_rect()
        self.set_array(self.front_array)
        
    def on_move(self, xdir, ydir):
        if xdir < 0:
            self.set_array(self.left_array)
        elif xdir > 0:
            self.set_array(self.right_array)
        elif ydir < 0:
            self.set_array(self.back_array)
        elif ydir > 0:
            self.set_array(self.front_array)
        
    def update(self):
        if self.xdir == 0 and self.ydir == 0:
            if self.last_xdir < 0:
                self.image = self.left_image
            elif self.last_xdir > 0:
                self.image = self.right_image
            elif self.last_ydir < 0:
                self.image = self.back_image
            elif self.last_ydir > 0:
                self.image = self.front_image
        self.xdir = 0
        self.ydir = 0
        
# A class that represent a little square box on screen
class DeadBox(objects.SpriteObject):
    def __init__(self, pos):
        objects.SpriteObject.__init__(self)
        
        image = pygame.Surface((32, 32))
        image.fill((0,0,255))
        self.set_image(image, pos)

# A class that represent a little square box on screen
class ItemBox(objects.SpriteObject):
    def __init__(self, pos):
        objects.SpriteObject.__init__(self)
        
        image = pygame.Surface((32, 32))
        image.fill((90,20,100))
        self.set_image(image, pos)

# A class that represent a little square box on screen
class Block(objects.SpriteObject, objects.UnwalkableObject):
    def __init__(self, pos, top, bottom, left, right):
        objects.SpriteObject.__init__(self)
        objects.UnwalkableObject.__init__(self, top, bottom, left, right)
        
        image = pygame.Surface((32, 32))
        image.fill((255,255,0))
        self.set_image(image, pos)
        self.set_relative_rect()
        
class Tree(objects.SpriteObject, objects.CollidableObject, objects.UnwalkableObject):
    def __init__(self, res, pos, top, bottom, left, right):
        objects.SpriteObject.__init__(self)
        objects.CollidableObject.__init__(self)
        objects.UnwalkableObject.__init__(self, top, bottom, left, right)
        self.res = res
        
        orig = self.res.image.get('map')
        image = tools.get_image_at(orig, 0, 256, 32, 32)
        self.set_image(image, pos)
        self.set_relative_rect()

class WaterWell(objects.SpriteObject, objects.CollidableObject, objects.UnwalkableObject):
    def __init__(self, res, pos, top, bottom, left, right):
        objects.SpriteObject.__init__(self)
        objects.CollidableObject.__init__(self)
        objects.UnwalkableObject.__init__(self, top, bottom, left, right)
        self.res = res
        
        orig = self.res.image.get('map')
        image = tools.get_image_at(orig, 0, 32, 32, 32)
        self.set_image(image, pos)
        self.set_relative_rect()

class Gravestone(objects.SpriteObject, objects.CollidableObject, objects.UnwalkableObject):
    def __init__(self, res, pos, top, bottom, left, right):
        objects.SpriteObject.__init__(self)
        objects.CollidableObject.__init__(self)
        objects.UnwalkableObject.__init__(self, top, bottom, left, right)
        self.res = res
        
        orig = self.res.image.get('map')
        image = tools.get_image_at(orig, 32, 256, 32, 32)
        self.set_image(image, pos)
        self.set_relative_rect()

class CrossGravestone(objects.SpriteObject, objects.CollidableObject, objects.UnwalkableObject):
    def __init__(self, res, pos, top, bottom, left, right):
        objects.SpriteObject.__init__(self)
        objects.CollidableObject.__init__(self)
        objects.UnwalkableObject.__init__(self, top, bottom, left, right)
        self.res = res
        
        orig = self.res.image.get('map')
        image = tools.get_image_at(orig, 64, 256, 32, 32)
        self.set_image(image, pos)
        self.set_relative_rect()
        
class Fence(objects.SpriteObject, objects.CollidableObject, objects.UnwalkableObject):
    def __init__(self, t_id, res, pos, top, bottom, left, right):
        objects.SpriteObject.__init__(self)
        objects.CollidableObject.__init__(self)
        objects.UnwalkableObject.__init__(self, top, bottom, left, right)
        self.res = res
        
        orig = self.res.image.get('map')
        
        if t_id == '17':
            image = tools.get_image_at(orig, 0, 64, 32, 32)
        elif t_id == '19':
            image = tools.get_image_at(orig, 64, 64, 32, 32)
        elif t_id == '18':
            image = tools.get_image_at(orig, 32, 64, 32, 32)
        elif t_id == '33':
            image = tools.get_image_at(orig, 0, 128, 32, 32)
        elif t_id == '34':
            image = tools.get_image_at(orig, 32, 128, 32, 32)
        elif t_id == '35':
            image = tools.get_image_at(orig, 64, 128, 32, 32)
        elif t_id == '25':
            image = tools.get_image_at(orig, 0, 96, 32, 32)
        
        self.set_image(image, pos)
        if t_id == '34':
            self.set_relative_rect(32, 20, top=self.rect.top + 6)
        elif t_id == '25':
            self.set_relative_rect(14, 32, left=self.rect.left + 2)
        else:
            self.set_relative_rect()
            
class Coin(objects.SpriteObject, objects.CollidableObject):
    def __init__(self, res, pos):
        objects.SpriteObject.__init__(self)
        objects.CollidableObject.__init__(self)
        
        self.anim_delay = 5
        
        ckey = (0, 255, 0)
        orig = res.image.get('coin32')
        array = [
            tools.get_image_at(orig, 0, 0, 32, 32, ckey),
            tools.get_image_at(orig, 32, 0, 32, 32, ckey),
            tools.get_image_at(orig, 64, 0, 32, 32, ckey),
            tools.get_image_at(orig, 96, 0, 32, 32, ckey),
        ]
        
        self.set_image(array[0], pos)
        self.set_relative_rect()
        self.set_array(array)
    
    def update(self):
        self.next_image()
