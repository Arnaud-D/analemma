import datetime as dt
import conversions as cv
import numpy as np


class PointOfView:
    def trajectory_horizontal(self, latitude, longitude):
        raise NotImplementedError

    def trajectory_equatorial(self):
        raise NotImplementedError

    def trajectory_ecliptic(self):
        raise NotImplementedError

    def revolution_speed(self):
        raise NotImplementedError

    def days_per_year(self):
        return int(np.floor(1 / cv.rad2deg(self.revolution_speed()) * 360) + 1)

    def one_day(self):
        return 1


class Planet(PointOfView):
    def ecliptic_coordinates(self, time):
        raise NotImplementedError

    def obliquity(self, time):
        raise NotImplementedError

    def revolution_speed(self):
        raise NotImplementedError

    def initial_longitude(self):
        raise NotImplementedError

    def equation_time(self, time):
        raise NotImplementedError

    def trajectory_horizontal(self, latitude, longitude):
        return lambda time: self.horizontal_coordinates(latitude, longitude, time)

    def trajectory_equatorial(self):
        return self.equatorial_coordinates

    def trajectory_ecliptic(self):
        return self.ecliptic_coordinates

    def equatorial_coordinates(self, time):
        sun_latitude, sun_longitude = self.ecliptic_coordinates(time)
        obliquity = self.obliquity(time)
        declination, right_ascension = self.ecliptic2equatorial(sun_latitude, sun_longitude, obliquity)
        return declination, right_ascension

    def horizontal_coordinates(self, latitude, longitude, time):
        """Return the position of the sun in the horizontal coordinates system."""
        sun_latitude, sun_longitude = self.ecliptic_coordinates(time)
        obliquity = self.obliquity(time)
        declination, right_ascension = self.ecliptic2equatorial(sun_latitude, sun_longitude, obliquity)
        teq = self.equation_time(time)
        hour_angle = np.pi - (((time - 0.5) * 24) * cv.deg2rad(15) + longitude + teq)
        elevation, azimuth = self.equatorial2horizontal(latitude, longitude, declination, hour_angle)
        return elevation, azimuth

    @staticmethod
    def ecliptic2equatorial(lat, long, obl):
        declination = np.arcsin(np.sin(lat) * np.cos(obl) + np.cos(lat) * np.sin(obl) * np.sin(long)) % (2 * np.pi)
        right_ascension = np.arctan2(np.sin(long) * np.cos(obl) - np.tan(lat) * np.sin(obl), np.cos(long))
        return declination, right_ascension

    @staticmethod
    def equatorial2horizontal(lat, _, decl, h):
        elevation = np.arcsin(np.sin(lat) * np.sin(decl) + np.cos(lat) * np.cos(decl) * np.cos(h))
        azimuth = np.pi - np.arctan2(np.sin(h), np.cos(h) * np.sin(lat) - np.tan(decl) * np.cos(lat))
        return elevation, azimuth

    @staticmethod
    def time_coordinate(date):
        """Return the time coordinate for a given date."""
        reference = dt.datetime(2000, 1, 1, 12, 0, 0)  # also known as "J2000.0"
        delta = date - reference
        coordinate = delta.days + cv.seconds2days(delta.seconds)
        return coordinate


class EarthPov(Planet):
    def obliquity(self, time):
        a = cv.deg2rad(0.00000036)
        b = cv.deg2rad(23.439)
        return (a * time + b) % (2 * np.pi)

    def revolution_speed(self):
        return cv.deg2rad(0.98564736)

    def initial_longitude(self):
        return cv.deg2rad(280.459)

    def ecliptic_coordinates(self, time):
        """Return the position of the sun in the ecliptic coordinate system."""
        latitude = 0
        a = cv.deg2rad(0.98560028)
        b = cv.deg2rad(357.529)
        mean_anomaly = (a * time + b) % (2 * np.pi)
        a = cv.deg2rad(1.915)
        b = cv.deg2rad(0.020)
        mean_longitude = self.sun_mean_longitude(time)
        longitude = (mean_longitude + a * np.sin(mean_anomaly) + b * np.sin(2 * mean_anomaly)) % (2 * np.pi)
        return latitude, longitude

    def equation_time(self, time):
        sun_latitude, sun_longitude = self.ecliptic_coordinates(time)
        obliquity = self.obliquity(time)
        _, right_ascension = self.ecliptic2equatorial(sun_latitude, sun_longitude, obliquity)
        teq = (self.sun_mean_longitude(time) - right_ascension) % (2 * np.pi)
        return teq

    def sun_mean_longitude(self, time):
        return (self.revolution_speed() * time + self.initial_longitude()) % (2 * np.pi)


class VerticalEarthPov(Planet):
    def obliquity(self, time):
        return 0

    def revolution_speed(self):
        return cv.deg2rad(0.98564736)

    def initial_longitude(self):
        return cv.deg2rad(280.459)

    def ecliptic_coordinates(self, time):
        """Return the position of the sun in the ecliptic coordinate system."""
        latitude = 0
        a = cv.deg2rad(0.98560028)
        b = cv.deg2rad(357.529)
        mean_anomaly = (a * time + b) % (2 * np.pi)
        a = cv.deg2rad(1.915)
        b = cv.deg2rad(0.020)
        mean_longitude = self.sun_mean_longitude(time)
        longitude = (mean_longitude + a * np.sin(mean_anomaly) + b * np.sin(2 * mean_anomaly)) % (2 * np.pi)
        return latitude, longitude

    def equation_time(self, time):
        sun_latitude, sun_longitude = self.ecliptic_coordinates(time)
        obliquity = self.obliquity(time)
        _, right_ascension = self.ecliptic2equatorial(sun_latitude, sun_longitude, obliquity)
        teq = (self.sun_mean_longitude(time) - right_ascension) % (2 * np.pi)
        return teq

    def sun_mean_longitude(self, time):
        return (self.revolution_speed() * time + self.initial_longitude()) % (2 * np.pi)


class CircularEartPov(Planet):
    """Earth model with constant obliquity and circular orbit."""
    def obliquity(self, time):
        return cv.deg2rad(23.439)

    def revolution_speed(self):
        return cv.deg2rad(0.98564736)

    def initial_longitude(self):
        return cv.deg2rad(280.459)

    def ecliptic_coordinates(self, time):
        latitude = 0
        longitude = self.revolution_speed() * time + self.initial_longitude()
        return latitude, longitude

    def equation_time(self, time):
        sun_latitude, sun_longitude = self.ecliptic_coordinates(time)
        obliquity = self.obliquity(time)
        _, right_ascension = self.ecliptic2equatorial(sun_latitude, sun_longitude, obliquity)
        teq = (sun_longitude - right_ascension) % (2 * np.pi)
        return teq


class CircularVerticalEarth(Planet):
    """Earth model with constant obliquity and circular orbit."""
    def obliquity(self, time):
        return 0

    def revolution_speed(self):
        return cv.deg2rad(0.98564736)

    def initial_longitude(self):
        return cv.deg2rad(280.459)

    def ecliptic_coordinates(self, time):
        latitude = 0
        longitude = self.revolution_speed() * time + self.initial_longitude()
        return latitude, longitude

    def equation_time(self, time):
        sun_latitude, sun_longitude = self.ecliptic_coordinates(time)
        obliquity = self.obliquity(time)
        _, right_ascension = self.ecliptic2equatorial(sun_latitude, sun_longitude, obliquity)
        teq = (sun_longitude - right_ascension) % (2 * np.pi)
        return teq


class MarsPov(Planet):
    def initial_longitude(self):
        return cv.deg2rad(270.3863)

    def days_per_year(self):
        return int(668 * 1.027) + 1

    def one_day(self):
        return 1

    def revolution_speed(self):
        return cv.deg2rad(0.52403840)

    def equatorial_coordinates(self, time):
        sun_latitude, sun_longitude = self.ecliptic_coordinates(time)
        obliquity = self.obliquity(time)
        declination, right_ascension = self.ecliptic2equatorial(sun_latitude, sun_longitude, obliquity)
        return declination, right_ascension

    def ecliptic_coordinates(self, time):
        """Return the position of the sun in the ecliptic coordinate system."""
        latitude = cv.deg2rad(1.85)
        a = cv.deg2rad(0.52402075)
        b = cv.deg2rad(19.38)
        mean_anomaly = (a * time + b) % (2 * np.pi)
        a = cv.deg2rad(10.691)
        b = cv.deg2rad(0.623)
        mean_longitude = self.sun_mean_longitude(time)
        longitude = (mean_longitude + a * np.sin(mean_anomaly) + b * np.sin(2 * mean_anomaly)) % (2 * np.pi)
        return latitude, longitude

    def equation_time(self, time):
        sun_latitude, sun_longitude = self.ecliptic_coordinates(time)
        obliquity = self.obliquity(time)
        _, right_ascension = self.ecliptic2equatorial(sun_latitude, sun_longitude, obliquity)
        teq = (self.sun_mean_longitude(time) - right_ascension) % (2 * np.pi)
        return teq

    def sun_mean_longitude(self, time):
        a = self.revolution_speed()
        b = self.initial_longitude()
        mean_longitude = (a * time + b) % (2 * np.pi)
        return mean_longitude

    def obliquity(self, _):
        return cv.deg2rad(25.19)
