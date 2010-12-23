# -*- coding: utf-8 -*-
#===================================================
# 
# Represents an actor in game (player, npc, etc)
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 22, 2010
#===================================================

import math
import pygame

class Actor(pygame.sprite.Sprite):
    ''' This class represents the base class for all the character objects; npc
    players, etc'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = None
        self.rect = None
        self.radius = 0
        
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
        
