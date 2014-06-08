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

__doc__ = """rocket.py -- rockets class with coodrinates and speed.

Every rocket must implement methods for changing their speed according to
gravity of ground objects, for changing position according to therir speed.

Also rocket must contain power and type (create ground, anihilate ground, etc)
of it's explosion. Collapsing and map changes on exploude would be calculated
with separated world master module."""


from gamelib import maprepr
import math

class ExplosionType ():
    """RocketType is static class that contains codes for MapObject types.

    ANIHILATE	is type id for rockets that just destroy groud around cell
    			where rocket explodes.
    GROUND		type id for rockets that create new grounds around explosion
    			place.
    """
    ANIHILATE = 0
    GROUND = 1


class RocketObject ():
    """RocketObject class used as base class for every rocket.

    self.x, self.y is currect coordinates. It's fixed point value.
    self.x_speed, slef.y_speed is current rocket speed.
    self.explosion_type describe type of explosion. This information woud be used
    for world processing when rocket exploded.
    self.explosion_power contain integer number describe power on specified type
    explosion.

    self.step () just move rocket to new place according to it's speed.
    self.get_place () return currect coordinates of the rocket
    self.get_speed () return currect speed of the rocket
    self.is_exploded ([(place, object)]) get list of object intersected through
    last step and return information if rocket exploded and where it's happens
    self.change_speed (place, object) must be call for every object that can
    perform gravity interaction with rocket.

    So world interraction with rocket looks like

    while (rocket exist):
      start = rocket.get_place()
      end = rocket.step()
      if (rocket.is_exploded(objects_in_range (start, end))):
        EXPLODE
        break
      if (end not on map):
        break
      for (place, object in near end):
        rocket.change_speed (place, object)
    """

    def __init__ (self, t, power, start_place, start_speed):
        [x,y] = start_place
        [sx, sy] = start_speed
        self.x = x
        self.y = y
        self.x_speed = sx
        self.y_speed = sy
        self.explosion_type = t
        self.explosion_power = power

    def step (self):
        """Change rocket coodrinates according to rocket speed.
        Return new rocket coordinates."""
        return self.get_place ()

    def get_speed (self):
        """Return current rocket speed"""
        return (self.x_speed, self.y_speed)

    def get_place (self):
        """Return current rocket place"""
        return (self.x, self.y)

    def is_exploded (self, intersected_objects):
        """intersected_objects is a list of tuples (place, object) with objects
        that was intersected between start and end position of current step.
        INCLUDING both start and end position. So it can have single element
        only if rocket not cross square borded.

        Reurns tuple (is_exploded, place) that can be both (True, object_place)
        and (False, self.get_place())"""
        return (True, intersected_objects[0][0])

    def change_speed (self, place, ground):
        """Change speed of the rocket according to surrounding ground weights and
        positions. This method must be called for every piec of ground that can
        have impact on rocket speed."""
        pass


class SimpleRocket (RocketObject):
    """ANIHILATE type rocket that explode on first contact with ground"""
    def __init__ (self, place, speed, power = 20):
        RocketObject.__init__ (self, ExplosionType.ANIHILATE, power, place, speed)

    def step (self):
        self.x += self.x_speed
        self.y += self.y_speed
        return self.get_place ()

    def change_speed (self, place, weight):
        [x, y] = place
        x += 0.5                          # center of square weight
        y += 0.5                          #

        [xs, ys] = recalc_speed (self.get_place(),(x,y),weight)
        self.x_speed += xs
        self.y_speed += ys

    def is_exploded (self, intersected_objects):
        for place_object in intersected_objects:
            [place, obj] = place_object
            if not isinstance(obj, maprepr.SpaceObject):
                return (True, place)
        return (False, self.get_place ())

GRAVITY_CONSTANT = 0.015
def recalc_speed (me, place, weight):
    [x,y] = place
    [ox, oy] = me
    distance = math.sqrt (((x - ox) ** 2) + ((y - oy) ** 2))
    vectored_speed = GRAVITY_CONSTANT * weight / (distance ** 2)
    speed_x = vectored_speed * ((x - ox) / distance)
    speed_y = vectored_speed * ((y - oy) / distance)

    return (speed_x, speed_y)
