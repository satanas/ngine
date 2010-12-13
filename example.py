#!/usr/bin/env python
# -*- coding: utf-8 -*-

#================================================
#
# This script shows how to use Camera class in a game that just move a
# box around the map.
#
# Copyright (C) 2010  Wil Alvarez <wil.alejandro@gmail.com>
#
#===================================================

import pygame

from ngine import input
from ngine import camera
from ngine import resources

# KEY BINDINGS (Defined by user)
LEFT = 0x10
RIGHT = 0x11
UP = 0x12
DOWN = 0x13
ACTION1 = 0x14
ACTION2 = 0x15
ACTION3 = 0x16
EXIT = 0xFF

#MOUSE BINDINGS
MOTION = 0x20
BUTTON1 = 0x21
BUTTON2 = 0x22
BUTTON3 = 0x23

# A class that represent a little square box on screen
class Box(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((32, 32))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft=(120, 120)
        
    def move(self, x_speed, y_speed):
        self.rect.move_ip(x_speed, y_speed)
        
    def moveAbs(self, x, y):
        self.rect.center = (x, y)
        
    def changeColor(self, color):
        self.image.fill(color)

# A class that represent a little square box on screen
class DeadBox(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((32, 32))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.topleft=pos


# The main class that hold the funny part
class Example:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Camera Example')
        self.screen=pygame.display.set_mode((320, 320))
        self.clock = pygame.time.Clock()
        
        # We create a new instance of InputParser
        self.input=input.InputParser()
        self.input.bind_key(input.KEY_DOWN, pygame.K_LEFT, LEFT, True)
        self.input.bind_key(input.KEY_DOWN, pygame.K_RIGHT, RIGHT, True)
        self.input.bind_key(input.KEY_DOWN, pygame.K_UP, UP, True)
        self.input.bind_key(input.KEY_DOWN, pygame.K_DOWN, DOWN, True)
        self.input.bind_key(input.KEY_DOWN, pygame.K_SPACE, ACTION1)
        self.input.bind_key(input.KEY_DOWN, pygame.K_LCTRL, ACTION2)
        self.input.bind_key(input.KEY_DOWN, pygame.K_LSHIFT, ACTION3)
        self.input.bind_key(input.KEY_DOWN, pygame.K_ESCAPE, EXIT)
        '''
        self.input.bind_mouse_button(BUTTON1, input.MOUSE_BUTTON1)
        self.input.bind_mouse_button(MOTION, input.MOUSE_MOTION)
        
        self.input.bind_joy_button(ACTION1, input.JOY_BUTTON1)
        self.input.bind_joy_button(ACTION2, input.JOY_BUTTON2)
        self.input.bind_joy_button(ACTION3, input.JOY_BUTTON3)
        
        self.input.bind_joy_axis(LEFT, input.JOY_AXIS_0_LEFT)
        self.input.bind_joy_axis(RIGHT, input.JOY_AXIS_0_RIGHT)
        self.input.bind_joy_axis(UP, input.JOY_AXIS_1_UP)
        self.input.bind_joy_axis(DOWN, input.JOY_AXIS_1_DOWN)
        '''
        layer1 = pygame.sprite.Group()
        layer2 = pygame.sprite.Group()
        all = pygame.sprite.Group()
        
        Box.containers=all, layer1
        DeadBox.containers=all, layer2
        
        self.box=Box()
        DeadBox((0,0))
        DeadBox((100,100))
        DeadBox((70,70))
        self.target2=DeadBox((200,200))
        self.target3=DeadBox((400,390))
        
        self.camera = camera.Camera(self.screen, (600, 500))
        self.camera.set_target(self.box)
        self.camera.set_backgrounds(bg2='bg1.png', bg3='bg3.png')
        
        while True:
            self.clock.tick(60)
            
            # Then we process the keys detected by handle keyboard
            self.__gameControl()
            
            # Update everything
            #layer1.update()
            #layer2.update()
            all.update()
            self.camera.update()
            self.camera.draw_groups([layer2, layer1])
            
            pygame.display.flip()
            
    def __gameControl(self):
        # We call the handle keyboard method
        self.input.handle_input()
        
        if self.input.lookup(LEFT): 
            self.box.move(-2,0)
        if self.input.lookup(RIGHT): 
            self.box.move(2,0)
        if self.input.lookup(UP): 
            self.box.move(0,-2)
        if self.input.lookup(DOWN): 
            self.box.move(0,2)
        if self.input.lookup(ACTION1): 
            self.camera.pan_to_pos(self.target2.rect.center)
        if self.input.lookup(ACTION2): 
            self.camera.move_to_pos(self.target3.rect.topleft, camera.TOPLEFT)
        if self.input.lookup(ACTION3): 
            self.camera.move_to_rel(2,0)
        if self.input.lookup(BUTTON1): 
            print 'Hello'
        if self.input.lookup(EXIT): 
            exit(0)
        
if __name__=="__main__":
    ex=Example()
