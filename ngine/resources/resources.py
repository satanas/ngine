# -*- coding: utf-8 -*-
#===================================================
# 
# A module that let you create a 2D side-scrolling camera with some
# optimizations
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 11, 2010
#===================================================

import pygame

from ngine.resources import music
from ngine.resources import sound
from ngine.resources import image
from ngine.resources import font
from ngine.resources import background

class Resources:
    def __init__(self):
        pygame.mixer.init()
        pygame.font.init()
        pygame.display.init()
        
        self.music = MusicHandler()
        self.sound = SoundHandler()
        self.image = ImageHandler()
        self.font = FontHandler()
        self.bg = BackgroundHandler()
