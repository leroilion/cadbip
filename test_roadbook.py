#!/usr/bin/env python3
'''
Copyright 2020 by Jérémy Cheynet.
All rights reserved.
This file is part of the cadip project, and is released under the
"GNU GENERAL PUBLIC LICENSE Version 3".
Please see the LICENSE file that should have been included as part of this package.
File name: roadbook.test.py
Author: Jeremy Cheynet <jerem.cheynet@gmail.com>
'''
import unittest
import datetime
import roadbook

# pylint: disable=protected-access
class DistanceTest(unittest.TestCase):
    """ Test case for distance object """

    def test_constructor(self):
        """ Test if constructor set default value """

        distance = roadbook.Distance()
        self.assertEqual(0, distance.distance)

        distance = roadbook.Distance(24.42)
        self.assertEqual(24.42, distance.distance)

    def test_set_distance(self):
        """ Test exception and set distance value """

        distance = roadbook.Distance()

        with self.assertRaises(ValueError):
            distance.distance = "test"

        with self.assertRaises(ValueError):
            distance.distance = -1

        distance.distance = 0
        self.assertEqual(0, distance.distance)

        distance.distance = 1
        self.assertEqual(1, distance.distance)

        distance.distance = 0.542
        self.assertEqual(0.542, distance.distance)

class SpeedTest(unittest.TestCase):
    """ Test case for speed object """

    def test_constructor(self):
        """ Test if constructor set default value """

        speed = roadbook.Speed()
        self.assertEqual(speed.distance, 0)
        self.assertEqual(speed.speed, 1)

        speed = roadbook.Speed(42.5, 3.5)
        self.assertEqual(speed.distance, 42.5)
        self.assertEqual(speed.speed, 3.5)

    def test_set_speed(self):
        """ Test exception of speed =  """

        speed = roadbook.Speed()

        with self.assertRaises(ValueError):
            speed.speed = -1

        with self.assertRaises(ValueError):
            speed.speed = 0

        with self.assertRaises(ValueError):
            speed.speed = "test"

        speed.speed = 24.42
        self.assertEqual(speed.speed, 24.42)

class ZrTest(unittest.TestCase):
    """ Test ZR """

    def test_constructor(self):
        """ Test default value in constructor """

        zr = roadbook.Zr() # pylint: disable=invalid-name
        now = datetime.datetime.now()
        self.assertEqual(0, len(zr._speeds))
        self.assertLess(zr.start_time - now, datetime.timedelta(0, 1))
        self.assertEqual(0, zr._number)

        zr = roadbook.Zr(5) # pylint: disable=invalid-name
        self.assertEqual(5, zr._number)

    def test_zr_number(self):
        """ Test zr number """

        zr = roadbook.Zr() # pylint: disable=invalid-name

        with self.assertRaises(ValueError):
            zr.number = "test"

        with self.assertRaises(ValueError):
            zr.number = 3.5

        with self.assertRaises(ValueError):
            zr.number = -5

        zr.number = 12
        self.assertEqual(zr.number, 12)

    def test_zr_start_time(self):
        """ Test zr set start time """

        zr = roadbook.Zr() # pylint: disable=invalid-name

        with self.assertRaises(ValueError):
            zr.start_time = "test"

        with self.assertRaises(ValueError):
            zr.start_time = 3

        now = datetime.datetime.now()
        zr.start_time = now
        self.assertEqual(now, zr.start_time)


    def test_zr_manage_speed(self):
        """ Test to add, delete, get speed """

        zr = roadbook.Zr() # pylint: disable=invalid-name
        self.assertEqual(0, len(zr._speeds))

        with self.assertRaises(ValueError):
            zr.add_speed("test")

        speed1 = roadbook.Speed(0.5, 42.5)
        zr.add_speed(speed1)
        self.assertEqual(1, len(zr._speeds))
        self.assertTrue(speed1 in zr._speeds)

        with self.assertRaises(ValueError):
            zr.add_speed(speed1)

        zr.add_speed(1.42, 43.8)
        self.assertEqual(2, len(zr._speeds))

        speed3 = roadbook.Speed(2.254, 12.953)
        zr.add_speed(speed3)
        self.assertEqual(3, len(zr._speeds))
        self.assertTrue(speed3 in zr._speeds)

        self.assertEqual(speed1, zr.get_speed(0.5))
        self.assertEqual(speed1, zr.get_speed(0.49999, roadbook.ZrGetter.NEXT))
        self.assertEqual(speed1, zr.get_speed(0.50001, roadbook.ZrGetter.PREV))

        self.assertEqual(speed3, zr.get_speed(2.254))
        self.assertEqual(speed3, zr.get_speed(2.253, roadbook.ZrGetter.NEXT))
        self.assertEqual(speed3, zr.get_speed(2.255, roadbook.ZrGetter.PREV))

        zr.delete_speed(1.42)
        self.assertEqual(2, len(zr._speeds))
        self.assertEqual(speed3, zr.get_speed(1, roadbook.ZrGetter.NEXT))
        self.assertEqual(speed1, zr.get_speed(2, roadbook.ZrGetter.PREV))

        zr.delete_speed(roadbook.Speed(2.254))
        self.assertEqual(1, len(zr._speeds))
        self.assertEqual(None, zr.get_speed(1, roadbook.ZrGetter.NEXT))
        self.assertEqual(speed1, zr.get_speed(5, roadbook.ZrGetter.PREV))

class RoadbookTest(unittest.TestCase):
    """ Test Roadbook """

    def test_load(self):
        """ Test default value in constructor """

        road_book = roadbook.Roadbook()
        self.assertEqual(0, len(road_book._zrs))

        road_book.load_zr(5)
        self.assertEqual(1, len(road_book._zrs))
        self.assertEqual(5, road_book._loaded_zr.number)

        road_book.load_zr(10)
        self.assertEqual(2, len(road_book._zrs))
        self.assertEqual(10, road_book._loaded_zr.number)

        road_book.load_zr(5)
        self.assertEqual(2, len(road_book._zrs))
        self.assertEqual(5, road_book._loaded_zr.number)

        road_book.delete_zr(5)
        self.assertEqual(1, len(road_book._zrs))
        self.assertEqual(None, road_book._loaded_zr)


if __name__ == "__main__":
    unittest.main()
