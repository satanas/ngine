# -*- coding: utf-8 -*-
#===================================================
# 
# Submodule of Resources with useful and common tools
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 11, 2010
#===================================================

import os
import pygame

def get_datafile_path(folder, filename):
     return os.path.realpath(os.path.join(os.path.dirname(__file__),
        '..', '..', 'data', folder, filename))
     #return os.path.realpath(os.path.join(os.path.dirname(__file__),
     #   'data', folder, filename))
     
def get_image_at(orig, x_pos, y_pos, width, height, colorkey=None):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    if colorkey:
        image.set_colorkey(colorkey, pygame.locals.RLEACCEL)
    image.blit(orig, (0, 0, width, height), (x_pos, y_pos, width, height))
    return image.convert_alpha()
    
def flip_images(imgarray):
    tmp = []
    for image in imgarray:
        tmp.append(pygame.transform.flip(image, 1, 0))
    return tmp
