# -*- coding: utf-8 -*-
#================================================
#
# Handles all resources, game scenes and main loop
#
# Copyright (C) 2010  Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 24, 2010
#===================================================

import pygame

class Director:
    def __init__(self, gamedata):
        pygame.init()
        pygame.display.set_caption(gamedata.screen_title)
        self.screen = pygame.display.set_mode(gamedata.screen_res)
        self.clock = pygame.time.Clock()
        self.scene = None
        self.fps = gamedata.fps
        self.quit = False
        
    def loop(self):
        while not self.quit:
            self.clock.tick(self.fps)
            
            self.quit = self.scene.handle_events()
            self.scene.update()
            self.scene.check_collisions()
            self.scene.draw()
            
            pygame.display.flip()
            
    def change_scene(self, scene):
        if self.scene:
            self.scene.unload()
        self.scene = scene
        self.scene.load()
