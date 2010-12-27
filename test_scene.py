# -*- coding: utf-8 -*-

#================================================
#
# Dummy Scene for the Ngine Example (please execute test.py)
#
# Copyright (C) 2010  Wil Alvarez <wil.alejandro@gmail.com>
#
#===================================================

import pygame
import random

from ngine import scene
from ngine import collisions
from ngine import particles

from test_keys import *
from test_objects import *

class DummyScene(scene.Scene):
    def __init__(self, director, _input, gamedata):
        scene.Scene.__init__(self, director, _input, gamedata)
        
    def _load_map(self, filename):
        self.maploader.load(filename)
        
        for row in self.maploader.layers['blocks']:
            for block in row:
                if block.t_id == '01':
                    tb, bb, lb, rb = self.maploader.get_collide_bounds(block.x, block.y)
                    Block((block.real_x, block.real_y), tb, bb, lb, rb)
        
        for event in self.maploader.events:
            if event.e_id == 'box':
                self.box = Box((event.x, event.y))
            elif event.e_id == 'deadbox':
                DeadBox((event.x, event.y))
            elif event.e_id == 'block':
                Block((event.x, event.y))
        
    def _on_load(self):
        self.layer1 = pygame.sprite.Group()
        self.layer2 = pygame.sprite.Group()
        self.gblocks = pygame.sprite.Group()
        self.all = pygame.sprite.Group()
        
        Box.containers = self.all, self.layer1
        DeadBox.containers = self.all, self.layer2
        particles.Particle.containers = self.all, self.layer2
        Block.containers = self.all, self.layer2, self.gblocks
        
        self._load_map('01.map')
        
        self.res.font.load_default('__default__', 16, (255,255,255))
        self.res.bg.load(['bg1.png', 'bg2.png'])
        #self.res.tile.load('mud-tile-example.png', self.maploader.get_tile_size())
        
        self.effect = 0
        '''
        for i in range(100):
            x = random.randint(30, 1950)
            y = random.randint(30, 1950)
            Block((x,y))
        self.target2 = DeadBox((200,200))
        self.target3 = DeadBox((400,390))
        '''
        self.camera.world_size = (2000, 2000)
        self.camera.set_target(self.box)
        #self.set_backgrounds(bg3='bg1', bg2='bg2')
        self.set_backgrounds(bg1=self.maploader.layers['background'])
        
    def handle_events(self):
        self._input.handle_input()
        
        if self._input.lookup(LEFT): 
            self.box.move(-1,0)
            self.cbg.scroll(-self.box.xspeed)
        if self._input.lookup(RIGHT): 
            self.box.move(1,0)
            self.cbg.scroll(self.box.xspeed)
        if self._input.lookup(UP): 
            self.box.move(0,-1)
        if self._input.lookup(DOWN): 
            self.box.move(0,1)
        #if self._input.lookup(ACTION1): 
        #    self.camera.pan_to_pos(self.target2.rect.center)
        #if self._input.lookup(ACTION2): 
        #    self.camera.move_to_pos(self.target3.rect.topleft, camera.TOPLEFT)
        #if self._input.lookup(ACTION3): 
        #    self.camera.move_to_rel(2,0)
        if self._input.lookup(BUTTON1):
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
        if self._input.lookup(BUTTON3): 
            self.effect += 1
            if self.effect > 4:
                self.effect = 0
        if self._input.lookup(EXIT): 
            return True
        
        return False
    
    def check_collisions(self):
        for obj in self.gblocks:
            if collisions.check(self.box, obj):
                obj.collide(self.box)
                
    def update(self):
        self.all.update()
        scroll = self.camera.update()
        self.cbg.update(scroll)
        
    def draw(self):
        self.cbg.draw()
        self.camera.draw_background(self.cbg.image)
        self.camera.draw_groups([self.layer2, self.layer1])
        
        if self.effect == 3:
            ang = random.randint(-25, 25)
            particles.Particle(pos=pygame.mouse.get_pos(), angle=ang, 
                               size=1.8, color_type='random', duration=1500, 
                               vx=0.5, vy=1, ax=0, ay=0)
        elif self.effect == 4:
            particles.ParticlesBoost(pygame.mouse.get_pos(), 180, 2, 
                                     particles=50)
        self.__text_on_screen()
    
    def __text_on_screen(self):
        fps = str(int(self.director.clock.get_fps ()))
        obj_count = str(len(self.all))
        info1 = self.res.font.render('__default__', 'FPS: ' + fps)
        info2 = self.res.font.render('__default__', 'Objects: ' + obj_count)
        self.screen.blit(info1, (10, 10))
        self.screen.blit(info2, (10, 20))
        
        if self.effect == 0: 
            text = self.res.font.render('__default__', 'Effect: Explosion')
        elif self.effect == 1: 
            text = self.res.font.render('__default__', 'Effect: Fireworks')
        elif self.effect == 2: 
            text = self.res.font.render('__default__', 'Effect: Shock')
        elif self.effect == 3: 
            text = self.res.font.render('__default__', 'Effect: Trace')
        elif self.effect == 4: 
            text = self.res.font.render('__default__', 'Effect: Boost')
        inst = self.res.font.render('__default__', 'Click on the screen to see the effect. Right click to change it')
        self.screen.blit(inst, (150,440))
        self.screen.blit(text, (250,460))
