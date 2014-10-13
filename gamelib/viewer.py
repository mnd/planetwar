#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014  Nikolay Merinov

# Author: Nikolay Merinov <nikolay.merinov@member.fsf.org>

# This file is part of PlanetWar.

# PlanetWar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PlanetWar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

__doc__ = """viewer.py -- display game GUI"""

from gamelib import maprepr, stepper, rocket
import pygame, sys, time

class View ():
    """View class would be used for displaying objects to screen"""
    def __init__ (self, myMap, size):
        self.size = size
        self.map = myMap
        self.screenSize = self.width, self.height = size*myMap.width, size*myMap.height
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)
        # Fill background
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((210, 210, 210))

        self.baseSquare1 = pygame.Surface((size,size)).convert()
        self.baseSquare1.fill((0,0,255))

        self.baseSquare2 = pygame.Surface((size,size)).convert()
        self.baseSquare2.fill((255,0,0))

        self.rocketSquare = pygame.Surface((3,3)).convert()
        self.rocketSquare.fill((0,0,0))

        self.groundSquare = pygame.Surface((size,size)).convert()
        self.screen.blit(self.background, (0, 0))

    def step (self, rockets):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.base.quit()
                sys.exit()                #probably return exit code, instead of exit
                return 1
        # Drow map
        self.background.fill((210, 210, 210))
        for x in range(self.map.width):
            for y in range(self.map.height):
                if isinstance(self.map.content[x][y], maprepr.SpaceObject):
                    pass                      #don't drow space in foreground
                elif isinstance(self.map.content[x][y], maprepr.BaseObject):
                    if (self.map.bases[0] is self.map.content[x][y]):
                        self.background.blit(self.baseSquare1, (x*self.size,y*self.size))
                    else:
                        self.background.blit(self.baseSquare2, (x*self.size, y*self.size))
                elif isinstance(self.map.content[x][y], maprepr.GroundObject):
                    color = 255 - min(255, int(self.map.content[x][y].weight*2.55))
                    self.groundSquare.fill((color,color,color))
                    self.background.blit(self.groundSquare, (x*self.size,y*self.size))
                else:
                    raise Exception ('unknown object on the map')
        # Drow rockets
        for r in rockets:
            [x,y] = r.get_place ()
            self.background.blit(self.rocketSquare, (int(x*self.size),int(y*self.size)))
        # Display image to screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

def run (myMap, size):
    proc = stepper.Stepper (myMap)        #rockets processor
    view = View(myMap, size)              #viewer

    proc.launch_rocket (rocket.SimpleRocket ((32.5, 22.5), (2.46, 0.0), 40))
    proc.launch_rocket (rocket.SimpleRocket ((22.5, 32.5), (0.0, 1.7), 70))

    while 1:
        # 1. Select place from where you would start rocket
        # 2. Display rocket fly
        view.step (proc.rockets)
        while proc.is_inprogress ():
            view.step (proc.rockets)
            time.sleep (0.2)
            proc.step ()
        # 3. Change user and repeat

def runTest (myMap, size):
    proc = stepper.Stepper (myMap)
    proc.launch_rocket (rocket.SimpleRocket ((32.5, 22.5), (2.2, 0.0), 40))
    proc.launch_rocket (rocket.SimpleRocket ((22.5, 32.5), (0.0, 1.7), 70))

    view = View(myMap, size)
    while 1:
        view.step (proc.rockets)
        proc.step ()
        time.sleep (0.3)
