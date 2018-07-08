import unittest
import bodies
import conversions as cv
import math


class TestEcliptic2Equatorial(unittest.TestCase):
    def setUp(self):
        self.body = bodies.SunFromPlanet(cv.deg2rad(0.98564736), 0, 1)
        self.precision = 0.01

    def test_ecliptic2equatorial_1(self):
        dec, ra = self.body.ecliptic2equatorial(0, 0, math.pi/4)
        self.assertAlmostEqual(dec, 0, delta=self.precision)
        self.assertAlmostEqual(ra, 0, delta=self.precision)

    def test_ecliptic2equatorial_2(self):
        dec, ra = self.body.ecliptic2equatorial(0, math.pi, math.pi/4)
        self.assertAlmostEqual(dec, 0, delta=self.precision)
        self.assertAlmostEqual(ra, math.pi, delta=self.precision)

    def test_ecliptic2equatorial_3(self):
        dec, ra = self.body.ecliptic2equatorial(0, math.pi, math.pi/4)
        self.assertAlmostEqual(dec, 0, delta=self.precision)
        self.assertAlmostEqual(ra, math.pi, delta=self.precision)

    def test_ecliptic2equatorial_4(self):
        dec, ra = self.body.ecliptic2equatorial(0, math.pi/2, math.pi/4)
        self.assertAlmostEqual(dec, math.pi/4, delta=self.precision)
        self.assertAlmostEqual(ra, math.pi/2, delta=self.precision)

    def test_ecliptic2equatorial_5(self):
        dec, ra = self.body.ecliptic2equatorial(0, 3 * math.pi / 2, math.pi / 4)
        self.assertAlmostEqual(dec, 7 * math.pi / 4, delta=self.precision)
        self.assertAlmostEqual(ra, - math.pi / 2, delta=self.precision)

    def test_ecliptic2equatorial_6(self):
        dec, ra = self.body.ecliptic2equatorial(- math.pi / 4, math.pi / 2, math.pi / 4)
        self.assertAlmostEqual(dec, 0, delta=self.precision)
        self.assertAlmostEqual(ra, math.pi / 2, delta=self.precision)

    def test_ecliptic2equatorial_7(self):
        dec, ra = self.body.ecliptic2equatorial(math.pi / 4, 3 * math.pi / 2, math.pi / 4)
        self.assertAlmostEqual(dec, 0, delta=self.precision)
        self.assertAlmostEqual(ra, - math.pi / 2, delta=self.precision)


if __name__ == '__main__':
    unittest.main()
