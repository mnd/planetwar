#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014  Nikolay Merinov

# Author: Nikolay Merinov <nikolay.merinov@member.fsf.org>

__doc__ = """runner.py -- module that runs game with precreated maps"""

from gamelib import maprepr, stepper, rocket, viewer
import time

def run (myMap, size):
    proc = stepper.Stepper (myMap)        #rockets processor
    view = viewer.View(myMap, size)              #viewer
    player = 0
    while 1:
        # 1. Select place from where you would start rocket
        [rx, ry] = view.selectStartPlace (myMap.bases[player])
        # 2. Select speed and vector
        [px, py] = view.selectPowerVector ((rx, ry), (rx + 0.5, ry + 0.5))
        # 3. Launch rocket
        proc.launch_rocket (rocket.SimpleRocket ((rx + 0.5, ry + 0.5),
                                                 (px, py), 30))
        # 4. Display rocket fly
        while proc.is_inprogress ():
            view.step (proc.rockets, (rx,ry), ((rx + 0.5, ry + 0.5), (px, py)))
            time.sleep (0.2)
            proc.step ()
        # 5. Change user and repeat
        player = (player + 1) % 2

def runTest (myMap, size):
    proc = stepper.Stepper (myMap)
    proc.launch_rocket (rocket.SimpleRocket ((32.5, 22.5), (2.2, 0.0), 40))
    proc.launch_rocket (rocket.SimpleRocket ((22.5, 32.5), (0.0, 1.7), 70))

    view = viewer.View(myMap, size)
    while 1:
        view.step (proc.rockets)
        proc.step ()
        time.sleep (0.3)
