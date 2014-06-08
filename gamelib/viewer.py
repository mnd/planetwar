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

def run (myMap, size):
    proc = stepper.Stepper (myMap)
    proc.launch_rocket (rocket.SimpleRocket ((32.5, 22.5), (2.2, 0.0), 40))
    proc.launch_rocket (rocket.SimpleRocket ((22.5, 32.5), (0.0, 1.7), 70))

    screenSize = width, height = size*myMap.width, size*myMap.height
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    # Fill background
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((210, 210, 210))

    baseSquare1 = pygame.Surface((size,size)).convert()
    baseSquare1.fill((0,0,255))

    baseSquare2 = pygame.Surface((size,size)).convert()
    baseSquare2.fill((255,0,0))

    rocketSquare = pygame.Surface((3,3)).convert()
    rocketSquare.fill((0,0,0))

    groundSquare = pygame.Surface((size,size)).convert()

    screen.blit(background, (0, 0))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.base.quit()
                return 1
                sys.exit()


        background.fill((210, 210, 210))
        flag = 0
        for x in range(myMap.width):
            for y in range(myMap.height):
                if isinstance(myMap.content[x][y], maprepr.SpaceObject):
                    pass                      #don't drow space in foreground
                elif isinstance(myMap.content[x][y], maprepr.BaseObject):
                    if (flag == 0 or flag is myMap.content[x][y]):
                        background.blit(baseSquare1, (x*size,y*size))
                        if (flag == 0): flag = myMap.content[x][y]
                    else:
                        background.blit(baseSquare2, (x*size, y*size))
                elif isinstance(myMap.content[x][y], maprepr.GroundObject):
                    color = 255 - min(255, int(myMap.content[x][y].weight*2.55))
                    groundSquare.fill((color,color,color))
                    background.blit(groundSquare, (x*size,y*size))
                else:
                    raise Exception ('unknown object on the map')
        for r in proc.rockets:
            [x,y] = r.get_place ()
            background.blit(rocketSquare, (int(x*size),int(y*size)))
        proc.step ()
        time.sleep (0.3)
        screen.blit(background, (0, 0))
        pygame.display.flip()
