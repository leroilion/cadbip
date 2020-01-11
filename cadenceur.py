'''
Copyright 2020 by Jérémy Cheynet.
All rights reserved.
This file is part of the cadip project, and is released under the
"GNU GENERAL PUBLIC LICENSE Version 3".
Please see the LICENSE file that should have been included as part of this package.
File name: cadenceur.py
Author: Jeremy Cheynet <jerem.cheynet@gmail.com>
'''
import datetime
import roadbook

class Cadenceur():
    """ Class cadenseur to compute distance """

    def __init__(self):
        self._zr = None
        self._start_time = datetime.datetime.now()

    def start(self, time=None):
        """ Method to start ZR. If time is set, this function set start time """

        if time is None:
            self._start_time = datetime.datetime.now()
        else:
            self._start_time = time

    def enter_zr(self, zr): # pylint: disable=invalid-name
        """ This method is to insert zr in cadenceur """

        if isinstance(zr, roadbook.Zr):
            self._zr = zr
            self._start_time = zr.start_time

    def reset(self):
        """ Method to reset cadenceur """

        self._zr = None
        self._start_time = datetime.datetime.now()

    def get_distance(self, time=None):
        """ Get distance compute with loaded zr """

        if time is None:
            time = datetime.datetime.now()
        if self._start_time > time:
            return 0
        diff = time - self._start_time

        distance = 0
        first_speed = self._zr.get_speed(0, roadbook.ZrGetter.NEXT)
        while diff >= datetime.timedelta(0):
            next_speed = self._zr.get_speed(first_speed.distance + 1, roadbook.ZrGetter.NEXT)
            tmp = first_speed.speed * diff.total_seconds()
            if next_speed is None or distance + tmp <= next_speed.distance:
                return distance + tmp

            distance = next_speed.distance
            time_in_s = (next_speed.distance - first_speed.distance) / first_speed.speed
            diff = diff - datetime.timedelta(seconds=time_in_s)
            first_speed = next_speed

    def get_zr_number(self):
        """ Method to get the zr number """

        return self._zr.number
