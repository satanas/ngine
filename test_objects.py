# -*- coding: utf-8 -*-

#================================================
#
# Dummy Objects for the Ngine Example (please execute test.py)
#
# Copyright (C) 2010  Wil Alvarez <wil.alejandro@gmail.com>
#
#===================================================

import pygame

from ngine import objects

# A class that represent a little square box on screen
class Box(objects.Actor):
    def __init__(self):
        objects.Actor.__init__(self)
        
        image = pygame.Surface((32, 32))
        image.fill((255,0,0))
        self.set_image(image, (120, 120))
        self.xspeed = 2
        self.yspeed = 2
        
    def moveAbs(self, x, y):
        self.rect.center = (x, y)
        
    def changeColor(self, color):
        self.image.fill(color)

# A class that represent a little square box on screen
class DeadBox(objects.SpriteObject):
    def __init__(self, pos):
        objects.SpriteObject.__init__(self)
        
        image = pygame.Surface((32, 32))
        image.fill((0,0,255))
        self.set_image(image, (120, 120))
        
# A class that represent a little square box on screen
class Block(objects.Actor, objects.UnwalkableObject):
    def __init__(self, pos):
        objects.Actor.__init__(self)
        objects.UnwalkableObject.__init__(self, True, True, True, True)
        
        image = pygame.Surface((32, 32))
        image.fill((255,255,0))
        self.set_image(image, pos)
        self.set_limits()
