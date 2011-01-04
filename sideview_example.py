#!/usr/bin/env python
# -*- coding: utf-8 -*-

#================================================
#
# This script shows how to use Ngine to create a simple side-view game
#
# Copyright (C) 2010-2011  Wil Alvarez <wil.alejandro@gmail.com>
#
#===================================================

import pygame

from ngine import director
from ngine import gamedata
from ngine import inputparser as input_p

from dummy_keys import *
from sideview_scene import DummyScene

def main():
    gdata = gamedata.GameData('Side-View Example - Ngine', (640, 480), 1)
    
    # Map all input keys to Input Parser
    _input = input_p.InputParser()
    _input.bind_key(input_p.KEY_DOWN, pygame.K_LEFT, LEFT, True)
    _input.bind_key(input_p.KEY_DOWN, pygame.K_RIGHT, RIGHT, True)
    _input.bind_key(input_p.KEY_DOWN, pygame.K_UP, UP, True)
    _input.bind_key(input_p.KEY_DOWN, pygame.K_DOWN, DOWN, True)
    _input.bind_key(input_p.KEY_DOWN, pygame.K_SPACE, ACTION1)
    _input.bind_key(input_p.KEY_DOWN, pygame.K_LCTRL, ACTION2)
    _input.bind_key(input_p.KEY_DOWN, pygame.K_LSHIFT, ACTION3)
    _input.bind_key(input_p.KEY_DOWN, pygame.K_ESCAPE, EXIT)
        
    _dir = director.Director(gdata)
    scene = DummyScene(_dir, _input, gdata)
    _dir.change_scene(scene)
    _dir.loop()
 
if __name__ == '__main__':
    pygame.init()
    main()
