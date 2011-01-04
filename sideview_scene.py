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
        
    def __load_map(self, filename):
        self.maploader.load(filename)
        
        for row in self.maploader.layers['unwalkable']:
            for block in row:
                if block.t_id == '00': 
                    continue
                tb, bb, lb, rb = self.maploader.get_collide_bounds(block.x, block.y)
                Platform(self.res, block.t_id, (block.real_x, block.real_y), tb, bb, lb, rb)
        '''
                elif block.t_id == '65':
                    Tree(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '09':
                    WaterWell(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '66':
                    Gravestone(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '67':
                    CrossGravestone(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '17':
                    FenceUpLeftCorner(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '19':
                    FenceUpRightCorner(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '18':
                    FenceTopBorder(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '33':
                    FenceBottomLeftCorner(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '34':
                    FenceBottomBorder(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '35':
                    FenceBottomRightCorner(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '25':
                    FenceLeftBorder(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
        '''
        for row in self.maploader.layers['characters']:
            for char in row:
                if char.t_id == '01':
                    self.player = Tux(self.res, (char.real_x, char.real_y))
        '''
        for row in self.maploader.layers['items']:
            for item in row:
                if item.t_id == '01':
                    ItemBox((item.real_x, item.real_y))
        '''
    def on_load(self):
        self.layer1 = pygame.sprite.Group()
        self.layer2 = pygame.sprite.Group()
        self.gblocks = pygame.sprite.Group()
        self.all = pygame.sprite.Group()
        
        Tux.containers = self.all, self.layer1
        Platform.containers = self.all, self.layer2, self.gblocks
        
        self.res.font.load_default('__default__', 16, (255,255,255))
        self.res.bg.load(['bg1.png', 'bg2.png', 'scroll.png'])
        self.res.image.load(['tux.png', 'ground.png'])
        
        self.__load_map('01.map')
        
        self.effect = 0
        self.on_loaded_map()
        self.append_to_draw(self.layer2)
        self.append_to_draw(self.layer1)
        self.set_camera_target(self.player)
        self.set_backgrounds(bg1=self.maploader.layers['background'], bg2='scroll')
        
    def handle_events(self):
        self._input.handle_input()
        
        if self._input.lookup(LEFT): 
            self.player.move(-1, 0)
            self.scroll_bg(-self.player.xspeed)
        if self._input.lookup(RIGHT): 
            self.player.move(1, 0)
            self.scroll_bg(self.player.xspeed)
        if self._input.lookup(UP): 
            self.player.move(0, -1)
        if self._input.lookup(DOWN): 
            self.player.move(0, 1)
        #if self._input.lookup(ACTION1): 
        #    self.camera.pan_to_pos(self.target2.rect.center)
        #if self._input.lookup(ACTION2): 
        #    self.camera.move_to_pos(self.target3.rect.topleft, camera.TOPLEFT)
        #if self._input.lookup(ACTION3): 
        #    self.camera.move_to_rel(2,0)
        if self._input.lookup(EXIT): 
            return True
        
        return False
    
    def check_collisions(self):
        for obj in self.gblocks:
            if collisions.check(self.player, obj):
                print 'checked'
                obj.collide(self.player)
                
    def on_update(self):
        self.all.update()
        
    def on_draw(self):
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
