# -*- coding: utf-8 -*-
#================================================
#
# Holds the basic game data
#
# Copyright (C) 2010  Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 24, 2010
#===================================================

class GameData:
    ''' You should overwrite this class and add all params needed '''
    def __init__(self, title, screen_res, fps=60):
        self.screen_title = title
        self.screen_res = screen_res
        self.fps = fps
