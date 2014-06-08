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

__doc__ = """stepper.py -- main cycles for processing rockets on map"""

from gamelib import maprepr, rocket
import math

class Stepper ():
    """This class get map and navigate rocket through world"""
    def __init__ (self, gamemap):
        self.map = gamemap
        self.rockets = []

    def launch_rocket (self, r):
        """Create new rocket in the world"""
        self.rockets.append (r)

    def is_inprogress (self):
        """Stop processing when we has no one rocket"""
        return (len (self.rockets) != 0)

    def step (self):
        """Move all rockets to one step and change it's speed after step.
        Also call function for processing explosion, if needed.

        See RocketObject.__doc__ for working with rocket algorithm.

        TODO: Need normal algorithm for finding crossed points."""
        epsilon = 0.01
        grav_epsilon = 30                 #how many blocks affect our rocket
        for r in self.rockets[:]:
            [sx, sy] = r.get_place ()
            [ex, ey] = r.step ()          #move rocket
            # get crossed points
            x_step = ex > sx and 1 or -1
            y_step = ey > sy and 1 or -1
            x = int (sx)
            y = int (sy)
            points = [(x, y)]
            while not (x == int (ex) and y == int (ey)):
                if (int(ey) == y):
                    x += x_step
                    points.append ((x,y))
                    continue
                if (int(ex) == x):
                    y += y_step
                    points.append ((x,y))
                    continue
                x_at_y_border = (((y + (y_step == 1 and 1 or 0) - sy) / (ey - sy))
                                 *(ex - sx)) + sx
                if ((x_step == 1 and x_at_y_border < x + 1.0 - epsilon)
                    or (x_step == -1 and x_at_y_border > x + epsilon)):
                    y += y_step
                elif ((x_step == 1 and (x_at_y_border > x + 1.0 - epsilon
                                        and x_at_y_border < x + 1.0 + epsilon))
                      or (x_step == -1 and (x_at_y_border < x + epsilon
                                            and x_at_y_border > x - epsilon))):
                    x += x_step
                    y += y_step
                else:
                    x += x_step
                points.append ((x, y))
            crossed = []
            for p in points:
                [ox, oy] = p
                if not (ox < 0 or oy < 0
                        or ox > self.map.width-1 or oy > self.map.height-1):
                    crossed.append ((p, self.map.content[ox][oy]))
            # test if rocket explouded
            [is_exploded, explosion_place] = r.is_exploded (crossed)
            if is_exploded:
                self.explode (r, explosion_place)
                self.rockets.remove (r)
                continue
            if ex < 0 or ey < 0 or ex > self.map.width-1 or ey > self.map.height-1:
                self.rockets.remove (r)
                continue
            # change rocket speed
            for ox in range (max (0, int (ex) - grav_epsilon),
                             min (self.map.width-1, int (ex) + grav_epsilon)):
                for oy in range (max (0, int (ey) - grav_epsilon),
                                 min (self.map.height-1, int (ey) + grav_epsilon)):
                    if isinstance (self.map.content[ox][oy], maprepr.GroundObject):
                        r.change_speed ((ox, oy), self.map.content[ox][oy].weight)

    def explode (self, r, place):
        """Process map according to explosion type"""
        [ox, oy] = place
        if (r.explosion_type == rocket.ExplosionType.ANIHILATE):
            for x in xrange (max (0, ox-5), min (self.map.width-1, ox+5)):
                for y in xrange (max (0, oy-5), min (self.map.height-1, oy+5)):
                    distantion = math.sqrt ((ox - x)**2 + (oy - y)**2)
                    self.map.damageCell((x, y),
                                        r.explosion_power * (6-distantion) / 12)
