# -*- coding: utf-8 -*-
#===================================================
# 
# Handle colissions
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 22, 2010
#===================================================

def check(actor, obj):
    ox = obj.rect.centerx
    oy = obj.rect.centery
    
    ax = actor.rect.centerx
    ay = actor.rect.centery
    
    x = ox - ax if ox > ax else ax - ox
    y = oy - ay if oy > ay else ay - oy
    
    d2 = pow(x, 2) + pow(y, 2)
    r2 = pow(actor.radius + obj.radius, 2)
    #print obj, d2, r2
    if d2 <= r2:
        return obj.rect.colliderect(actor.rect)
    return False
