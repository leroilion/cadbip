#!/usr/bin/env python3
'''
Copyright 2020 by Jérémy Cheynet.
All rights reserved.
This file is part of the cadip project, and is released under the
"GNU GENERAL PUBLIC LICENSE Version 3".
Please see the LICENSE file that should have been included as part of this package.
File name: cadenceur.test.py
Author: Jeremy Cheynet <jerem.cheynet@gmail.com>
'''
import unittest
import datetime
import cadenceur
import roadbook

# pylint: disable=protected-access
class CadenceurTest(unittest.TestCase):
    """ Test case for cadenceur object """

    def test_constructor(self):
        """ Test if constructor set default value """

        cad = cadenceur.Cadenceur()
        self.assertEqual(None, cad._zr)
        self.assertEqual(True, isinstance(cad._start_time, datetime.datetime))

    def test_start(self):
        """ Test start method """

        cad = cadenceur.Cadenceur()
        cad.start()
        now = datetime.datetime.now()
        self.assertLess(cad._start_time - now, datetime.timedelta(0, 1))

        tmp = datetime.datetime(2020, 1, 11, 13, 37, 42)
        cad.start(tmp)
        self.assertEqual(cad._start_time, tmp)

    def test_enter_zr(self):
        """ Test to enter zr in cadenceur """

        cad = cadenceur.Cadenceur()
        zr = roadbook.Zr() # pylint: disable=invalid-name
        zr.start_time = datetime.datetime(2020, 1, 11, 13, 37, 42)
        zr.add_speed(roadbook.Speed(0, 10))
        zr.add_speed(roadbook.Speed(1000, 20))
        zr.add_speed(roadbook.Speed(2000, 30))

        cad.enter_zr(zr)
        self.assertEqual(zr, cad._zr)
        self.assertEqual(zr.start_time, cad._start_time)

    def test_get_distance(self):
        """ Test method to get distance """

        cad = cadenceur.Cadenceur()
        zr = roadbook.Zr() # pylint: disable=invalid-name
        zr.start_time = datetime.datetime(2020, 1, 11, 14, 00, 00)
        zr.add_speed(roadbook.Speed(0, 10))
        zr.add_speed(roadbook.Speed(1000, 20))
        zr.add_speed(roadbook.Speed(2000, 30))
        # After 50s -> d = 500
        # After 100s -> d = 1000
        # After 125s -> d = 1500
        # After 150s -> d = 2000
        # After 250s -> d = 5000

        cad.enter_zr(zr)

        self.assertEqual(0, cad.get_distance(datetime.datetime(2020, 1, 11, 13, 59, 59)))
        self.assertEqual(0, cad.get_distance(datetime.datetime(2020, 1, 11, 14, 00, 00)))
        self.assertEqual(500, cad.get_distance(datetime.datetime(2020, 1, 11, 14, 00, 50)))
        self.assertEqual(1000, cad.get_distance(datetime.datetime(2020, 1, 11, 14, 1, 40)))
        self.assertEqual(1500, cad.get_distance(datetime.datetime(2020, 1, 11, 14, 2, 5)))
        self.assertEqual(2000, cad.get_distance(datetime.datetime(2020, 1, 11, 14, 2, 30)))
        self.assertEqual(5000, cad.get_distance(datetime.datetime(2020, 1, 11, 14, 4, 10)))


if __name__ == "__main__":
    unittest.main()
