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

__doc__ = """testing.py -- create simple map and test viewer and phisics"""

import paths
from gamelib import (maprepr, runner)


myMap = maprepr.Map(100, 65)
# create base
myMap.createBase((10, 10), 5)
myMap.createBase((50, 50), 5)
for i in range(30,40):
    for j in range(30, 40):
        myMap.createGround((i, j), 10 * (i-29))

for i in range(60,70):
    for j in range(30, 40):
        myMap.createGround((i, j), 10 * (70-i))

# viewer.runTest (myMap, 10)
runner.run (myMap, 10)
