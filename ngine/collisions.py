# -*- coding: utf-8 -*-
#===================================================
# 
# Handle collisions
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 22, 2010
#===================================================

import math
import pygame

def check(actor, obj):
    ox = obj.rect.centerx
    oy = obj.rect.centery
    
    ax = actor.rect.centerx
    ay = actor.rect.centery
    
    x = ox - ax if ox > ax else ax - ox
    y = oy - ay if oy > ay else ay - oy
    
    d2 = pow(x, 2) + pow(y, 2)
    r2 = pow(actor.radius + obj.radius, 2)
    
    if d2 <= r2:
        return obj.rect.colliderect(actor.rect)
    '''
    #else:
    x1 = actor.old_centerx
    y1 = actor.old_centery
    
    try:
        #print (x1,y1), (ax, ay)
        alpha = math.atan(abs(ay - y1)/abs(ax - x1))
        h = math.sqrt(pow(abs(ay - y1), 2) + pow(abs(ax - x1), 2))
        
        #print alpha, h
        #rect = pygame.Rect(1, h, 
    except ZeroDivisionError:
        rect = pygame.Rect(0, 0, actor.rect.width, abs(ay - y1))
        rect.top = actor.rect.top
        rect.centerx = actor.rect.centerx
        
        #print 'collision', rect, obj.rect, rect.colliderect(obj.rect)
    '''
    
    return False
