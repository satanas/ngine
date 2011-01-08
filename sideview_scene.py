# -*- coding: utf-8 -*-

#================================================
#
# Dummy Scene for the Side-View Example (please execute sideview_example.py)
#
# Copyright (C) 2011  Wil Alvarez <wil.alejandro@gmail.com>
#
#===================================================

import pygame
import random

from ngine import scene
from ngine import collisions

from dummy_keys import *
from sideview_objects import *

class DummyScene(scene.Scene):
    def __init__(self, director, _input, gamedata):
        scene.Scene.__init__(self, director, _input, gamedata)
        self.quit = False
        
    def __load_map(self, filename):
        self.maploader.load(filename)
        
        for row in self.maploader.layers['unwalkable']:
            for block in row:
                if block.t_id == '00': 
                    continue
                tb, bb, lb, rb = self.maploader.get_collide_bounds(block.x, block.y)
                Platform(self.res, block.t_id, (block.real_x, block.real_y), tb, bb, lb, rb)
        
        for row in self.maploader.layers['characters']:
            for char in row:
                if char.t_id == '01':
                    self.player = Tux(self.res, (char.real_x, char.real_y), self.gblocks)
        
        for row in self.maploader.layers['items']:
            for item in row:
                if item.t_id == '01':
                    Coin(self.res, (item.real_x, item.real_y))
    
    def on_load(self):
        self.layer1 = pygame.sprite.Group()
        self.layer2 = pygame.sprite.Group()
        self.gblocks = pygame.sprite.Group()
        self.gcoins = pygame.sprite.Group()
        self.all = pygame.sprite.Group()
        
        Tux.containers = self.all, self.layer1
        Platform.containers = self.all, self.layer2, self.gblocks
        Coin.containers = self.all, self.layer2, self.gcoins
        
        self.res.font.load_default('__default__', 16, (255,255,255))
        self.res.bg.load(['bg1.png', 'bg2.png', 'scroll.png', 'north-pole.png'])
        self.res.image.load(['tux.png', 'ice-ground.png', 'coin.png'])
        self.res.sound.load(['coin.ogg'])
        
        self.__load_map('01.map')
        
        self.effect = 0
        self.on_loaded_map()
        self.append_to_draw(self.layer2)
        self.append_to_draw(self.layer1)
        self.set_camera_target(self.player)
        self.set_backgrounds(bg1='north-pole', bg3='scroll')
        
    def handle_events(self):
        self._input.handle_input()
        
        if self._input.lookup(LEFT): 
            self.player.move(-1, 0)
            self.scroll_bg(self.player.xspeed)
        elif self._input.lookup(RIGHT): 
            self.player.move(1, 0)
            self.scroll_bg(-self.player.xspeed)
        if self._input.lookup(ACTION1): 
            self.player.jump()
        if self._input.lookup(EXIT): 
            return True
        if self.quit:
            return True
        
        return False
    
    def check_collisions(self):
        for coin in self.gcoins:
             if collisions.check(self.player, coin):
                 coin.kill()
                 self.res.sound.play('coin')
                
    def on_update(self):
        self.all.update()
        if self.player.rect.top > self.maploader.get_size()[1]:
            self.quit = True
        
    def on_draw(self):
        self.__text_on_screen()
    
    def __text_on_screen(self):
        fps = str(int(self.director.clock.get_fps ()))
        obj_count = str(len(self.all))
        info1 = self.res.font.render('__default__', 'FPS: ' + fps)
        info2 = self.res.font.render('__default__', 'Objects: ' + obj_count)
        self.screen.blit(info1, (10, 10))
        self.screen.blit(info2, (10, 20))
