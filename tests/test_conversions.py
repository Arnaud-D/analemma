import conversions as cv
import math
import unittest


class TestRad2Deg(unittest.TestCase):
    def test_rad2deg_1(self):
        self.assertEqual(cv.rad2deg(0), 0)

    def test_rad2deg_2(self):
        self.assertEqual(cv.rad2deg(math.pi), 180)


class TestDeg2Rad(unittest.TestCase):
    def test_deg2rad_1(self):
        self.assertEqual(cv.deg2rad(0), 0)

    def test_deg2rad_2(self):
        self.assertEqual(cv.deg2rad(180), math.pi)


class TestHours2Rad(unittest.TestCase):
    def test_hours2rad_1(self):
        self.assertEqual(cv.hours2rad(0), 0)

    def test_hours2rad_2(self):
        self.assertEqual(cv.hours2rad(12), math.pi)


class TestSeconds2Days(unittest.TestCase):
    def test_seconds2days_1(self):
        self.assertEqual(cv.seconds2days(0), 0)

    def test_seconds2days_2(self):
        self.assertEqual(cv.seconds2days(86400), 1)


if __name__ == "__main__":
    unittest.main()
