# -*- coding: utf-8 -*-
#===================================================
# 
# Handle all resources
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
        self.music = music.MusicHandler()
        self.sound = sound.SoundHandler()
        self.image = image.ImageHandler()
        self.font = font.FontHandler()
        self.bg = background.BackgroundHandler()
