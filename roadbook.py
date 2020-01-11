'''
Copyright 2020 by Jérémy Cheynet.
All rights reserved.
This file is part of the cadip project, and is released under the
"GNU GENERAL PUBLIC LICENSE Version 3".
Please see the LICENSE file that should have been included as part of this package.
File name: roadbook.py
Author: Jeremy Cheynet <jerem.cheynet@gmail.com>
'''
from enum import Enum
import datetime

class ZrGetter(Enum): # pylint: disable=too-few-public-methods
    """ Zr getter type """
    EXACT = 0
    NEXT = 1
    PREV = -1

class Distance(): # pylint: disable=too-few-public-methods
    """ Class Distance """

    def __init__(self, distance=0):
        self._distance = 0
        self._time = None
        self.distance = distance

    def __str__(self):
        return "{"+str(self._distance)+"}"

    @property
    def distance(self):
        """ Getter of distance """

        return self._distance

    @distance.setter
    def distance(self, distance):
        """ set a distance in object"""

        try:
            if float(distance) >= 0:
                self._distance = float(distance)
            else:
                raise ValueError('Distance can\'t be negative')
        except:
            raise ValueError('Distance must be a float')

    @property
    def time(self):
        """ Getter of time """

        return self._time

    @time.setter
    def time(self, time):
        """ set a time in object Distance """

        if isinstance(time, datetime.datetime):
            self._time = time

class Speed(Distance):
    """ Class Speed """
    def __init__(self, distance=0, speed=1):
        super(Speed, self).__init__(distance)
        self._speed = 1
        self.speed = speed

    def __str__(self):
        return "{"+str(self._distance)+";"+str(self._speed)+"}"

    @property
    def speed(self):
        """ Getter of speed """

        return self._speed

    @speed.setter
    def speed(self, speed):
        """ set a speed in object Speed """

        try:
            if float(speed) > 0:
                self._speed = float(speed)
            else:
                raise ValueError('Speed can\'t be negative or null')
        except:
            raise ValueError('Speed must be a float')

class Zr():
    """ A zr is consists of array of speed, array of cross, start time
        and number """

    def __init__(self, number=0):
        self._speeds = []
        self._start_time = datetime.datetime.now()
        self._number = 0
        self.number = number

    def __str__(self):
        pass

    @property
    def start_time(self):
        """ Getter of start time """

        return self._start_time

    @start_time.setter
    def start_time(self, time):
        """ Setter of start time """

        if isinstance(time, datetime.datetime):
            self._start_time = time
        else:
            raise ValueError('time must be a datetime object')

    @property
    def number(self):
        """ Getter of the number of the zr """

        return self._number

    @number.setter
    def number(self, number):
        """ Setter of the number of the zr """

        try:
            if int(number) == float(number):
                if int(number) >= 0:
                    self._number = int(number)
                else:
                    raise ValueError("Zr number must be positive")
            else:
                raise ValueError("Zr number must be an integer")
        except:
            raise ValueError("Zr number must be an integer")

    def add_speed(self, speed, data=None):
        """ Add speed in ZR """

        if isinstance(speed, Speed):
            if self._get_speed(speed.distance) is not None:
                raise ValueError("Speed already exist at this distance")

            self._speeds.append(speed)
        elif data is not None:
            if self._get_speed(speed) is not None:
                raise ValueError("Speed already exist at this distance")

            self._speeds.append(Speed(speed, data))
        else:
            raise ValueError("Cross must be a Cross")

    def delete_speed(self, speed):
        """ Delete speed in ZR """

        if isinstance(speed, Speed):
            distance = speed.distance
        else:
            try:
                distance = float(speed)
            except:
                raise ValueError("speed must be a distance or a Speed")

        for i in range(len(self._speeds)):
            if self._speeds[i].distance == distance:
                del self._speeds[i]
                return

    def _get_prev_speed(self, distance):
        """ private method to get previous speed """

        tmp = None
        for speed in self._speeds:
            if speed.distance <= distance:
                if not tmp is None:
                    if tmp.distance <= speed.distance:
                        tmp = speed
                else:
                    tmp = speed
        return tmp

    def _get_next_speed(self, distance):
        """ private method to get next speed """

        tmp = None
        for speed in self._speeds:
            if speed.distance >= distance:
                if not tmp is None:
                    if tmp.distance >= speed.distance:
                        tmp = speed
                else:
                    tmp = speed
        return tmp

    def _get_speed(self, distance):
        """ private method to get speed """

        for speed in self._speeds:
            if speed.distance == distance:
                return speed
        return None

    def get_speed(self, distance, status=ZrGetter.EXACT):
        """ public method to get speed """

        if not isinstance(status, ZrGetter):
            raise ValueError("Bad input")

        try:
            if status == ZrGetter.EXACT:
                return self._get_speed(float(distance))
            if status == ZrGetter.PREV:
                return self._get_prev_speed(float(distance))
            if status == ZrGetter.NEXT:
                return self._get_next_speed(float(distance))
        except:
            raise ValueError("distance must be a float")

        return None

class Roadbook():
    """ Class roadbook which contains many ZR """

    def __init__(self):
        self._zrs = []
        self._loaded_zr = None

    def __str__(self):
        pass

    def load_zr(self, number):
        """ Load ZR by number """

        for zr in self._zrs: # pylint: disable=invalid-name
            if zr.number == number:
                self._loaded_zr = zr
                return

        self._loaded_zr = Zr(number)
        self._zrs.append(self._loaded_zr)

    def get_loaded_zr(self):
        """ Get loaded zr """

        return self._loaded_zr

    def delete_zr(self, number):
        """ Delete ZR by number """

        for i in range(len(self._zrs)):
            if self._zrs[i].number == number:
                del self._zrs[i]
                if self._loaded_zr.number == number:
                    self._loaded_zr = None
                return

    def reset_zr(self, number):
        """ Reset a ZR by delete and load them """

        self.delete_zr(number)
        self.load_zr(number)

    def add_speed(self, speed, data=None):
        """ Add speed in loaded zr """

        if self._loaded_zr is None:
            raise BufferError("There is no loaded zr")

        return self._loaded_zr.add_speed(speed, data)

    def delete_speed(self, speed):
        """ delete speed in loaded zr """

        if self._loaded_zr is None:
            raise BufferError("There is no loaded zr")

        return self._loaded_zr.delete_speed(speed)

    def get_speed(self, distance, status=ZrGetter.EXACT):
        """ get speed in loaded zr """

        if self._loaded_zr is None:
            raise BufferError("There is no loaded zr")

        return self._loaded_zr.get_speed(distance, status)
