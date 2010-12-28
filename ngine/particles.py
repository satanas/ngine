# -*- coding: utf-8 -*-
#===================================================
# 
# Generate a wide type of particles (explosions, blasts, boosts)
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 23, 2010
#===================================================

import math
import pygame
import random

def random_color():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    return r, g, b
        
class Particle(pygame.sprite.Sprite):
    def __init__(self, **args):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.vx = random.choice([0.2, 0.4, 0.6, 0.8, 1.0])*5
        self.vy = random.choice([0.2, 0.4, 0.6, 0.8, 1.0])*5
        self.ax = random.choice([0, 0.025, 0.05, 0.1])
        self.ay = random.choice([0, 0.025, 0.05, 0.1])
        self.angle=0
        self.duration=self.lifetime=255
        self.lifedec=8
        self.init_color=self.current_color=(255,255,255)
        self.end_color=(0,0,0)
        self.color_type='fixed'
        pos=(0,0)
        max_size=3
        
        if "max_vx" in args: 
            self.vx = random.choice([0.2, 0.4, 0.6, 0.8, 1.0])*args["max_vx"]
        if "max_vy" in args: 
            self.vy = random.choice([0.2, 0.4, 0.6, 0.8, 1.0])*args["max_vy"]
        if "vx" in args: 
            self.vx = args["vx"]
        if "vy" in args: 
            self.vy = args["vy"]
        if "ax" in args: 
            self.ax = args["ax"]
        if "ay" in args: 
            self.ay = args["ay"]
        if "angle" in args: 
            self.angle = args["angle"]
        if "pos" in args: 
            pos = args["pos"]
        if "max_size" in args: 
            max_size = args["max_size"]
        if "duration" in args: 
            self.duration=self.lifetime = args["duration"]
        if "lifedec" in args: 
            self.lifedec = args["lifedec"]
        if "init_color" in args: 
            self.init_color = self.current_color = args["init_color"]
        if "end_color" in args: 
            self.end_color = args["end_color"]
        if "color_type" in args: 
            self.color_type = args["color_type"]
        
        if "size" in args:
            size = args["size"]
        else: 
            size=random.randint(1, max_size)
        
        self.interp_time=self.lifetime/30
        if "interp_time" in args: 
            self.interp_time = self.lifetime/args["interp_time"]
        
        self.diffcolor=[]
        for i in range(3): 
            self.diffcolor.append((self.init_color[i]-self.end_color[i])/self.interp_time)
        
        self.image = pygame.Surface((size, size))
        self.image.fill(self.init_color)
        self.rect = self.image.get_rect(center = pos)
        self.x, self.y = self.rect.center
        w = self.rect.width / 2
        h = self.rect.height / 2
        self.radius = math.sqrt(pow(w, 2) + pow(h, 2))
        
    def interp_color(self):
        tmpcolor=[]
        for i in range(3):
            newitem=self.current_color[i]-self.diffcolor[i]
            if newitem < 0: 
                newitem = 0
            if newitem > 255: 
                newitem = 255
            tmpcolor.append(newitem)
        
        self.current_color = tmpcolor
        return tmpcolor[0], tmpcolor[1], tmpcolor[2]
        
    def update(self):
        self.vx += self.ax
        self.vy += self.ay
        self.x += math.sin(math.radians(self.angle))*self.vx
        self.y += math.cos(math.radians(self.angle))*self.vy
        self.rect.center = self.x, self.y
        self.lifetime -= self.lifedec
        if self.color_type=='random': 
            self.image.fill(random_color())
        elif self.color_type=='interp': 
            self.image.fill(self.interp_color())
        
        if self.lifetime <= 0: 
            self.kill()
        
        self.image.set_alpha((self.lifetime*255)/self.duration)
    
class ParticlesExplosion:
    def __init__(self, pos, s, icolor= (240,255,0), ecolor=(255,0,0), 
                 ctype='interp', particles=50):
        
        for i in range(particles):
            Particle(pos=pos, angle=random.randint(-360,360), max_size=s, 
                     color_type=ctype, duration=300, init_color=icolor, 
                     end_color=ecolor)
            
class ParticlesShock:
    def __init__(self, pos, s, dir, icolor= (255,255,255), ecolor=(0,0, 255), 
                 ctype='random', particles=30):
        
        for i in range(particles):
            ang = dir+random.randint(-25, 25)
            
            Particle(pos=pos, angle=ang, max_size=s, color_type=ctype, 
                     duration=300, interp_time=10, init_color=icolor, 
                     end_color=ecolor)
            
class ParticlesFirework:
    def __init__(self, pos, s, particles=30):
        endcolor = random_color()
        for i in range(particles):
            Particle(pos=pos, angle=random.randint(-360,360), size=s, vx=3, 
                     vy=3, ax=0, ay=0, color_type='interp', duration=400, 
                     init_color=(255, 255, 255), end_color=endcolor)
            Particle(pos=pos, angle=random.randint(-360,360), size=s, vx=2, 
                     vy=2, ax=0, ay=0, color_type='interp', duration=400, 
                     init_color=(255, 255, 255), end_color=endcolor)
            Particle(pos=pos, angle=random.randint(-360,360), size=s, max_vx=1, 
                     max_vy=1, color_type='interp', duration=400, 
                     init_color=(255, 255, 255), end_color=endcolor)
            
class ParticlesBoost:
    def __init__(self, pos, ang, s, icolor= (240,255,0), ecolor=(255,0,0), 
                 ctype='interp', particles=20):
        
        ang += random.randint(-25, 25)
        Particle(pos=pygame.mouse.get_pos(), angle=ang, size=s, 
                 color_type='interp', interp_time=20, init_color= (240,255,0), 
                 end_color=(255,0,0), duration=300, max_vx=1, max_vy=2, ax=0)
                 
# TODO: BloodParticles
