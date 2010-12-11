# -*- coding: utf-8 -*-
#===================================================
# 
# Submodule of Resources with useful and common tools
#
# Copyright (C) 2010 Wil Alvarez <wil.alejandro@gmail.com>
#
# Created at: Dic 11, 2010
#===================================================

import os

def get_datafile_path(folder, filename):
     #return os.path.realpath(os.path.join(os.path.dirname(__file__),
     #   '..', '..', 'data', folder, filename))
     return os.path.realpath(os.path.join(os.path.dirname(__file__),
        'data', folder, filename))
