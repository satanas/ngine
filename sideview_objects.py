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
    def __init__(self, res, pos):
        objects.Actor.__init__(self)
        objects.FallingObject.__init__(self)
        self.res = res
        
        ckey = (0, 255, 0)
        orig = self.res.image.get('tux')
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
        
        self.xspeed = 2.7
        self.yspeed = 2
        self.anim_delay = 4
        
        self.set_image(self.right_image, pos)
        self.set_array(self.right_array)
        
    def on_move(self, xdir, ydir):
        if xdir < 0:
            self.set_array(self.left_array)
        elif xdir > 0:
            self.set_array(self.right_array)
        
    def on_collide_top(self, object):
        print 'collide top'
        self.jumping = False
        self.jump_speed = 0
    
    def on_collide_bottom(self, object):
        print 'collide bottom'
        
    def update(self):
        self.check_gravity()
        if self.xdir == 0 and self.ydir == 0:
            if self.last_xdir < 0:
                self.image = self.left_image
            elif self.last_xdir > 0:
                self.image = self.right_image
        self.xdir = 0
        self.ydir = 0

# A class that represent a little square box on screen
class Platform(objects.Actor, objects.UnwalkableObject):
    def __init__(self, res, id, pos, top, bottom, left, right):
        objects.Actor.__init__(self)
        objects.UnwalkableObject.__init__(self, top, bottom, left, right)
        self.res = res
        
        image = pygame.Surface((24, 24))
        image.fill((255,255,0))
        orig = self.res.image.get('ground')
        if id == '01':
            image = tools.get_image_at(orig, 0, 0, 24, 24)
        if id == '02':
            image = tools.get_image_at(orig, 24, 0, 24, 24)
        elif id == '03':
            image = tools.get_image_at(orig, 48, 0, 24, 24)
        elif id == '04':
            image = tools.get_image_at(orig, 72, 0, 24, 24)
        elif id == '06':
            image = tools.get_image_at(orig, 0, 24, 24, 24)
        elif id == '09':
            image = tools.get_image_at(orig, 72, 24, 24, 24)
        elif id == '16':
            image = tools.get_image_at(orig, 0, 72, 24, 24)
        elif id == '19':
            image = tools.get_image_at(orig, 72, 72, 24, 24)
        self.set_image(image, pos)
        self.set_limits()
