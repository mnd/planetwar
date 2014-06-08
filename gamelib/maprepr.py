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

__doc__ = """maprepr.py -- map itself and object placed on map"""

class Map ():
    """Map class contain map information. Map represented as MapObject's double
    demensional array.

    self.width -- colums count
    self.height -- rows count
    self.content -- double demensional height*width sized array with MapObject
    object in it
    """
    def __init__ (self, width, height):
        """Construct map object"""
        self.width = width
        self.height = height
        self.content = []
        #create correct sized content array
        for i in xrange (width):
            self.content.append(height*[spaceObject])

    def __repr__(self):
        r = ""
        for x in range(self.width):
            for y in range(self.height):
                r += str(self.content[x][y])
            r += "\n"
        return r


    def createGround (self, place, weight):
        """Create ground in place of space"""
        [x, y] = place
        if isinstance(self.content[x][y], SpaceObject):
            self.content[x][y] = GroundObject(weight)
        else:
            raise Exception ('Ground must be created only over space')

    def createBase (self, place, r, health = 100):
        """Create Base square base with upper left cornel in (x,y) point and edge
        length equal to r
        """
        [x, y] = place
        if x < 0 or y < 0 or x+r > self.height or y+r > self.width:
            raise Exception ('Choose correct place for base')
        b = BaseObject(place, r, health)
        for i in range(r):
            for j in range(r):
                if isinstance(self.content[x+i][y+j], SpaceObject):
                    self.content[x+i][y+j] = b
                else:
                    raise Exception ('Base must be created only over space')

    def damageCell (self, place, count):
        """..."""
        [x,y] = place
        if isinstance (self.content[x][y], BaseObject):
            self.content[x][y].health -= count
        if isinstance (self.content[x][y], GroundObject):
            if self.content[x][y].weight > count:
                self.content[x][y].weight -= count
            else:
                self.content[x][y] = spaceObject

class MapObject ():
    """MapObject class used for describe every array cell. This class contain
    cell type.

    self.type is type of MapObject
    self.img  is image used for displaying this mapObject
    """
    def __init__ (self, img = 'generic'):
        self.img = img

class SpaceObject (MapObject):
    """SpaceObject is class which objects placed on map to describe blank space

    This class created as singleton, because it just a mark without properties.

    spaceObject is global object for this class. Please always use spaceObject,
    instead of creatind new SpaceObject()'s
    """
    def __init__ (self):
        MapObject.__init__(self)

    def __repr__ (self):
        return "_"

spaceObject = SpaceObject ()

class GroundObject (MapObject):
    """GroundObject is class for ground cell objects.

    self.weight is weight of groud cell. Must be from in (0,100] interval.

    For every ground cell must be created separete instance of GroundObject
    """
    def __init__ (self, weight):
        MapObject.__init__(self)
        self.weight = weight

    def __repr__ (self):
        return "#"

class BaseObject (MapObject):
    """BaseObject is class for users bases.

    self.health is health of user base. Default health is 100. When base health
    become zero user is lose.
    self.x, self.y is left upper corner of the base
    self.r base edge size. Base is squared

    Same instance of BaseObject must be placed on several connected cells.
    """
    def __init__ (self, place, r, health = 100):
        MapObject.__init__(self)
        [x, y] = place
        self.health = health
        self.x = x
        self.y = y
        self.r = r

    def __repr__ (self):
        return "B"
