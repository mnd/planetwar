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
        self.screenSize = (self.width, self.height) = (size*myMap.width,
                                                       size*myMap.height)
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

        self.selectSquare = pygame.Surface((size,size)).convert()
        self.selectSquare.fill((0,255,0))

    def selectPowerVector (self, start_square, start_place):
        [sx, sy] = start_place
        sx = int(sx)
        sy = int(sy)
        while 1:
            [x,y] = pygame.mouse.get_pos ()
            px = (int (x / self.size) + 0.5 - sx) / 10
            py = (int (y / self.size) + 0.5 - sy) / 10
            for event in pygame.event.get ():
                if event.type == pygame.QUIT:
                    pygame.base.quit ()
                    sys.exit ()        #probably rise exception, instead of exit
                if event.type == pygame.MOUSEBUTTONUP:
                    return (px, py)
            self.step ([], start_square, (start_place, (px, py)))

    def selectStartPlace (self, base):
        while 1:
            [x,y] = pygame.mouse.get_pos ()
            x = int (x / self.size)
            y = int (y / self.size)
            for event in pygame.event.get ():
                if event.type == pygame.QUIT:
                    pygame.base.quit ()
                    sys.exit ()        #probably rise exception, instead of exit
                if event.type == pygame.MOUSEBUTTONUP:
                    if ((base.x - 1 <= x and x <= base.x + base.r
                         and base.y - 1 <= y and y <= base.y + base.r)
                        and (x == base.x - 1 or x == base.x + base.r
                             or y == base.y - 1 or y == base.y + base.r)):
                        return (x, y)
            if ((base.x - 1 <= x and x <= base.x + base.r
                 and base.y - 1 <= y and y <= base.y + base.r)
                and (x == base.x - 1 or x == base.x + base.r
                     or y == base.y - 1 or y == base.y + base.r)):
                self.step ([], (x,y))
            else:
                self.step ()

    def step (self, rockets = [], select = None, vector = None):
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                pygame.base.quit ()
                sys.exit ()            #probably rise exception, instead of exit

        # Drow map
        self.background.fill((210, 210, 210))
        for x in range(self.map.width):
            for y in range(self.map.height):
                if isinstance(self.map.content[x][y], maprepr.SpaceObject):
                    pass                      #don't drow space in foreground
                elif isinstance(self.map.content[x][y], maprepr.BaseObject):
                    if (self.map.bases[0] is self.map.content[x][y]):
                        self.background.blit(self.baseSquare1, (x*self.size,
                                                                y*self.size))
                    else:
                        self.background.blit(self.baseSquare2, (x*self.size,
                                                                y*self.size))
                elif isinstance(self.map.content[x][y], maprepr.GroundObject):
                    color = 255 - min(255, int(self.map.content[x][y].weight*2.55))
                    self.groundSquare.fill((color,color,color))
                    self.background.blit(self.groundSquare, (x*self.size,
                                                             y*self.size))
                else:
                    raise Exception ('unknown object on the map')
        # Drow rockets
        for r in rockets:
            [x,y] = r.get_place ()
            self.background.blit(self.rocketSquare, (int(x*self.size),
                                                     int(y*self.size)))
        # Drow select sqares
        if select != None:
            [x,y] = select
            self.background.blit(self.selectSquare, (x*self.size, y*self.size))

        # Drow power vector
        if vector != None:
            [start, power] = vector
            [x, y] = start
            [px, py] = power
            x *= self.size
            y *= self.size
            px *= self.size
            py *= self.size
            pygame.draw.line(self.background, (255,255,0),
                              (int (x),int (y)), (int (x+px),int (y+py)), 2)

        # Display image to screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
