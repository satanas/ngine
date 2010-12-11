# -*- coding: utf-8 -*-
#===================================================
# 
# input.py - a simple library to bind standard input into user defined actions 
# to be used in pygame applications
#
# Copyright (C) 2008 - 2010  Wil Alvarez <wil.alejandro@gmail.com>
#
#===================================================
#
# Nov 20, 2008 - Wil Alvarez:
#   + Added support for documentation in pydoc format
#   + Added support UP and DOWN events for keys and joystick buttons
#   + Improved support for mouse move and quit events
#
# Sep 17, 2008 - Wil Alvarez:
#   + Changed format to complaint with python standard (indentation, underscore
#   separation for method name, etc)
#
# May 4, 2008 - Wil Alvarez: 
#   + Implemented mouse down/up events
#   + Added support for QUIT event

import pygame

KEY_UP = pygame.KEYUP
KEY_DOWN = pygame.KEYDOWN

MOUSE_MOTION = pygame.MOUSEMOTION
MOUSE_BUTTON_UP = pygame.MOUSEBUTTONUP
MOUSE_BUTTON_DOWN = pygame.MOUSEBUTTONDOWN

JOY_BUTTON_UP = pygame.JOYBUTTONUP
JOY_BUTTON_DOWN = pygame.JOYBUTTONDOWN

JOY_AXIS_LEFT = -1
JOY_AXIS_RIGHT = 1
JOY_AXIS_UP = -1
JOY_AXIS_DOWN = 1

QUIT = pygame.QUIT

JOY_SENSITIVITY = 0.90
JOY_OFFSET = (0.0038, 0.0039)

class InputParser:
    ''' This module binds standard input into user defined actions. It comes 
    with support for mouse and joystick'''
    def __init__(self, parseall=False, allow_repeat=True, sensitivity=JOY_SENSITIVITY):
        self.actions = {}
        self.bindings = {
            KEY_UP: {},
            KEY_DOWN: {},
            MOUSE_BUTTON_UP: {},
            MOUSE_BUTTON_DOWN: {},
            JOY_BUTTON_UP: {},
            JOY_BUTTON_DOWN: {},
            JOY_AXIS_UP: {},
            JOY_AXIS_DOWN: {},
            JOY_AXIS_LEFT: {},
            JOY_AXIS_RIGHT: {},
            MOUSE_MOTION: {0:None},
            QUIT: {0:None},
        }
        self.repeats = {}
        self.any = False
        self.parseall = parseall        # Do nothing so far
        JOY_SENSITIVITY = sensitivity   # Do nothing so far too
        self.allow_repeat = allow_repeat
        self.register = False
        
        for i in range(pygame.joystick.get_count()):
            joy=pygame.joystick.Joystick(i)
            joy.init()
            #print 'axis', joy.get_numaxes()
            #print 'axispos', joy.get_axis(0)
            
    def __abs_axis_value(self, value):
        ''' Get the joystick axis value and convert to -1, 0, 1. Direction
            values
        '''
        if (-JOY_SENSITIVITY < value < JOY_SENSITIVITY): 
            return 0
        elif (value <= -JOY_SENSITIVITY): 
            return -1
        elif (value >= JOY_SENSITIVITY): 
            return 1
        else:
            print 'else'
            return 0
    
    def __clear(self):
        ''' Clear all unrepeated actions '''
        for action in self.actions:
            if not self.repeats[action]:
                self.actions[action] = False
    
    def __unregister(self):
        ''' Register all actions '''
        del self.actions
        self.actions = {}
        
    def __register(self):
        ''' Register all actions bound '''
        for key in self.bindings:
            for x in self.bindings[key]:
                action = self.bindings[key][x]
                if action is None: continue
                if (not self.allow_repeat) and (action in self.actions):
                    raise ActionExist, action
                self.actions[action] = False
        self.register = True
        
    def set_sensitivity(self, value):
        ''' Sets the joystick sensitivity '''
        JOY_SENSITIVITY = value
        
    def bind_key(self, event, key, action, repeat=False):
        ''' Bind an action based on a keyboard event and a pressed key '''
        
        '''@event: The event to be intercepted (input.KEY_UP or input.KEY_DOWN)
            @key: The key that should be pressed to fire up the action
            @action: The action to be fired up
            @repeat: Indicate if action should be repeated while key is pressed
        '''
        if (event != KEY_UP) and (event != KEY_DOWN):
            raise InvalidEvent
        self.bindings[event][key] = action
        self.repeats[action] = repeat
        
    def bind_mouse_motion(self, action):
        ''' Bind an action based on mouse movements '''
        '''
            @action: The action to be fired up
        '''
        self.bindings[MOUSE_MOTION][0] = action
        self.repeats[action] = False
        
    def bind_mouse_button(self, event, button, action, repeat=False):
        ''' Bind an action based on a mouse button event '''
        '''
            @event: The event to be intercepted (input.MOUSE_BUTTON_UP or 
                input.MOUSE_BUTTON_DOWN)
            @button: The mouse button that should be pressed to fire up the 
                action (left: 1, middle: 2, right: 3)
            @action: The action to be fired up
            @repeat: Indicate if action should be repeated while button is 
                pressed
        '''
        if (event != MOUSE_BUTTON_UP) and (event != MOUSE_BUTTON_DOWN):
            raise InvalidEvent
        self.bindings[event][button] = action
        self.repeats[action] = repeat
        
    def bind_joy_button(self, event, button, action,repeat=False):
        ''' Bind an action based on a joystick button event '''
        '''
            @event: The event to be intercepted (input.JOY_BUTTON_UP or 
                input.JOY_BUTTON_DOWN)
            @button: The mouse button that should be pressed to fire up the 
                action (from 1 to 9)
            @action: The action to be fired up
            @repeat: Indicate if action should be repeated while button is 
                pressed
        '''
        if (event != JOY_BUTTON_UP) and (event != JOY_BUTTON_DOWN):
            raise InvalidEvent
        self.bindings[event][button] = action
        self.repeats[action] = repeat
        
    def bind_joy_axis(self, direction, axis, action, repeat=True):
        ''' Bind an action based on a joystick movement event '''
        '''
            @direction: The direction of axis movement (input.JOY_AXIS_LEFT, 
                input.JOY_AXIS_RIGHT, input.JOY_AXIS_UP, input.JOY_AXIS_DOWN)
            @axis: The joystick axis that should be pressed to fire up the 
                action (from 1 to 9)
            @action: The action to be fired up
            @repeat: Indicate if action should be repeated while axis is 
                pressed
        '''
        if (direction != JOY_AXIS_LEFT) and (direction != JOY_AXIS_RIGHT)\
        and (direction != JOY_AXIS_UP) and (direction != JOY_AXIS_DOWN):
            raise InvalidEvent
        self.bindings[direction][axis] = action
        self.repeats[action] = repeat
        
    def bind_quit(self, action):
        ''' Bind an action when pygame window is closed '''
        '''
            @action: The action to be fired up
        '''
        self.bindings[QUIT][0] = action
        self.repeats[action] = False
    
    def lookup(self, action):
        ''' Look if an action has been fired up '''
        '''
            @action: The action to look for
            @return: True if the action was fired up, False otherwise
        '''
        if action in self.actions:
            return self.actions[action]
        
    def lookup_any(self):
        ''' Look up for any key/button pressed '''
        '''
            @return: True if any button was pressed, False otherwise
        '''
        return self.any
        
    def handle_input(self):
        ''' Handles the standard input and set up actions for each event '''
        if (self.register is False): self.__register()
        self.__clear()
        
        for event in pygame.event.get():
            if event.type == KEY_DOWN:
                self.any = True
                # Set up the KEY_DOWN action
                if event.key in self.bindings[KEY_DOWN]:
                    action = self.bindings[KEY_DOWN][event.key]
                    self.actions[action] = True
            
            if event.type == KEY_UP:
                self.any = False
                # Set up the KEY_UP action
                if event.key in self.bindings[KEY_UP]:
                    action = self.bindings[KEY_UP][event.key]
                    self.actions[action] = True
                # Set down the KEY_DOWN action
                if event.key in self.bindings[KEY_DOWN]:
                    action = self.bindings[KEY_DOWN][event.key]
                    self.actions[action] = False
                    
            if (event.type == MOUSE_BUTTON_DOWN):
                self.any = True
                # Set up the MOUSE_BUTTON_DOWN action
                if event.button in self.bindings[MOUSE_BUTTON_DOWN]:
                    action = self.bindings[MOUSE_BUTTON_DOWN][event.button]
                    self.actions[action] = True
            
            if (event.type == MOUSE_BUTTON_UP):
                self.any = True
                # Set up the MOUSE_BUTTON_UP action
                if event.button in self.bindings[MOUSE_BUTTON_UP]:
                    action = self.bindings[MOUSE_BUTTON_UP][event.button]
                    self.actions[action] = True
                # Set down the MOUSE_BUTTON_DOWN action
                if event.button in self.bindings[MOUSE_BUTTON_DOWN]:
                    action = self.bindings[MOUSE_BUTTON_DOWN][event.button]
                    self.actions[action] = False
            
            if (event.type == MOUSE_MOTION):
                mm_action = self.bindings[MOUSE_MOTION][0]
                if mm_action is not None:
                    self.actions[mm_action] = True
            
            if event.type == QUIT:
                quit_action = self.bindings[QUIT][0]
                if quit_action is not None:
                    self.actions[quit_action] = True
            
            if (event.type == JOY_BUTTON_DOWN):
                self.any = True
                # Set up the JOY_BUTTON_DOWN action
                if event.button in self.bindings[JOY_BUTTON_DOWN]:
                    action = self.bindings[JOY_BUTTON_DOWN][event.button]
                    self.actions[action] = True
            
            if (event.type == JOY_BUTTON_UP):
                self.any = True
                # Set up the JOY_BUTTON_UP action
                if event.button in self.bindings[JOY_BUTTON_UP]:
                    action = self.bindings[JOY_BUTTON_UP][event.button]
                    self.actions[action] = True
                # Set down the JOY_BUTTON_DOWN action
                if event.button in self.bindings[JOY_BUTTON_DOWN]:
                    action = self.bindings[JOY_BUTTON_DOWN][event.button]
                    self.actions[action] = False
                
            if (event.type == pygame.JOYAXISMOTION):
                if (event.axis == 2): continue
                direction = self.__abs_axis_value(event.value)
                #print 'axis:',event.axis, 'axisvalue:',axisvalue, 
                #print 'event value:',event.value, self.actions
                if (event.axis not in self.bindings[-1]): continue
                if (event.axis not in self.bindings[1]): continue
                    
                if (direction == 0):
                    action_left = self.bindings[-1][event.axis]
                    action_right = self.bindings[1][event.axis]
                    self.actions[action_left] = False
                    self.actions[action_right] = False
                elif event.axis in self.bindings[direction]:
                    action = self.bindings[direction][event.axis]
                    self.actions[action] = True
                
        pygame.event.pump()

class InvalidEvent(Exception):
    def __init__(self):
        pass
        
    def __str__(self):
        return 'Invalid event for this bind or not defined in module'

class ActionExist(Exception):
    def __init__(self, action):
        self.action = action
        
    def __str__(self):
        return 'Action 0x%X already was defined' % self.action
