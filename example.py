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
import random

from ngine import input
from ngine import camera
from ngine import resources
from ngine import objects
from ngine import collisions
from ngine import particles

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
class DeadBox(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((32, 32))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.topleft=pos
        
# A class that represent a little square box on screen
class Block(objects.Actor, objects.UnwalkableObject):
    def __init__(self, pos):
        objects.Actor.__init__(self)
        objects.UnwalkableObject.__init__(self, True, True, True, True)
        
        image = pygame.Surface((32, 32))
        image.fill((255,255,0))
        self.set_image(image, pos)
        self.set_limits()

# The main class that hold the funny part
class Example:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Ngine Example')
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        
        self.effect = 0
        
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
        
        self.input.bind_mouse_button(input.MOUSE_BUTTON_UP, 1, BUTTON1)
        self.input.bind_mouse_button(input.MOUSE_BUTTON_UP, 3, BUTTON2)
        '''
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
        self.gblocks = pygame.sprite.Group()
        self.all = pygame.sprite.Group()
        
        Box.containers = self.all, layer1
        DeadBox.containers = self.all, layer2
        particles.Particle.containers = self.all, layer2
        Block.containers = self.all, layer2, self.gblocks
        
        self.box=Box()
        DeadBox((0,0))
        DeadBox((100,100))
        DeadBox((70,70))
        Block((200,20))
        for i in range(100):
            x = random.randint(30, 1950)
            y = random.randint(30, 1950)
            Block((x,y))
        self.target2=DeadBox((200,200))
        self.target3=DeadBox((400,390))
        
        self.camera = camera.Camera(self.screen, (2000, 2000))
        #self.camera.set_target(self.box)
        self.camera.set_backgrounds(bg2='bg1.png', bg3='bg3.png')
        
        self.font = pygame.font.Font(None, 16)
        
        while True:
            self.clock.tick(60)
            
            # Then we process the keys detected by handle keyboard
            self.__game_control()
            self.__check_collisions()
            # Update everything
            #layer1.update()
            #layer2.update()
            self.all.update()
            self.camera.update()
            self.camera.draw_groups([layer2, layer1])
            
            if self.effect == 3:
                ang=random.randint(-25, 25)
                particles.Particle(pos=pygame.mouse.get_pos(), angle=ang, 
                                   size=1.8, color_type='random', duration=1500, 
                                   vx=0.5, vy=1, ax=0, ay=0)
            elif self.effect == 4:
                particles.ParticlesBoost(pygame.mouse.get_pos(), 180, 2, 
                                         particles=50)
            self.__text_on_screen()
            pygame.display.flip()
            
    def __game_control(self):
        # We call the handle keyboard method
        self.input.handle_input()
        
        if self.input.lookup(LEFT): 
            self.box.move(-1,0)
        if self.input.lookup(RIGHT): 
            self.box.move(1,0)
        if self.input.lookup(UP): 
            self.box.move(0,-1)
        if self.input.lookup(DOWN): 
            self.box.move(0,1)
        if self.input.lookup(ACTION1): 
            self.camera.pan_to_pos(self.target2.rect.center)
        if self.input.lookup(ACTION2): 
            self.camera.move_to_pos(self.target3.rect.topleft, camera.TOPLEFT)
        if self.input.lookup(ACTION3): 
            self.camera.move_to_rel(2,0)
        if self.input.lookup(BUTTON1):
            if pygame.mouse.get_pos()[0] > 640/2: 
                dir = 270
            else: 
                dir = 90
            if self.effect == 0:
                particles.ParticlesExplosion(pygame.mouse.get_pos(), 2)
            elif self.effect == 1:
                particles.ParticlesFirework(pygame.mouse.get_pos(), 2)
            elif self.effect == 2:
                particles.ParticlesShock(pygame.mouse.get_pos(), 1, dir, (0,255,0))
        if self.input.lookup(BUTTON2): 
            self.effect += 1
            if self.effect > 4:
                self.effect = 0
        if self.input.lookup(EXIT): 
            exit(0)
            
    def __check_collisions(self):
        for obj in self.gblocks:
            if collisions.check(self.box, obj):
                obj.collide(self.box)
        
    def __text_on_screen(self):
        fps = str(int(self.clock.get_fps ()))
        obj_count = str(len(self.all))
        info1 = self.font.render('FPS: ' + fps, 1, (255,255,255))
        info2 = self.font.render('Objects: ' + obj_count, 1, (255,255,255))
        self.screen.blit(info1, (10, 10))
        self.screen.blit(info2, (10, 20))
        
        if self.effect == 0: 
            text = self.font.render('Effect: Explosion', 1, (255,255,255))
        elif self.effect == 1: 
            text = self.font.render('Effect: Fireworks', 1, (255,255,255))
        elif self.effect == 2: 
            text = self.font.render('Effect: Shock', 1, (255,255,255))
        elif self.effect == 3: 
            text = self.font.render('Effect: Trace', 1, (255,255,255))
        elif self.effect == 4: 
            text = self.font.render('Effect: Boost', 1, (255,255,255))
        inst = self.font.render('Click on the screen to see the effect. Right click to change it', 1, (255,255,255))
        self.screen.blit(inst, (150,440))
        self.screen.blit(text, (250,460))
    
if __name__=="__main__":
    ex=Example()
