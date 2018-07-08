import datetime as dt
import conversions as cv
import math as ma


class BodyFromPov:
    def horizontal_coordinates(self, latitude, longitude, time):
        raise NotImplementedError


class SunFromPlanet(BodyFromPov):
    def ecliptic_coordinates(self, time):
        raise NotImplementedError

    def obliquity(self, time):
        raise NotImplementedError

    def __init__(self, revolution_speed, initial_longitude, solar_day_duration):
        self.revolution_speed = revolution_speed
        self.initial_longitude = initial_longitude
        self.solar_day_duration = solar_day_duration
        self.days_per_revolution = int(ma.floor(1 / cv.rad2deg(self.revolution_speed) * 360) + 1)

    def horizontal_coordinates(self, latitude, longitude, time):
        """Return the position of the sun in the horizontal coordinates system."""
        sun_latitude, sun_longitude = self.ecliptic_coordinates(time)
        obliquity = self.obliquity(time)
        declination, right_ascension = self.ecliptic2equatorial(sun_latitude, sun_longitude, obliquity)
        teq = self.equation_time(time)
        local_days = time / self.solar_day_duration
        hour_angle = ma.pi - (cv.hours2rad(local_days * 24 - 12)) + teq
        elevation, azimuth = self.equatorial2horizontal(latitude, longitude, declination, hour_angle)
        return elevation, azimuth

    def equation_time(self, time):
        sun_latitude, sun_longitude = self.ecliptic_coordinates(time)
        obliquity = self.obliquity(time)
        _, right_ascension = self.ecliptic2equatorial(sun_latitude, sun_longitude, obliquity)
        teq = (self.mean_longitude(time) - right_ascension) % (2 * ma.pi)
        return teq

    def mean_longitude(self, time):
        return (self.revolution_speed * time + self.initial_longitude) % (2 * ma.pi)

    @staticmethod
    def equatorial2horizontal(lat, _, decl, h):
        elevation = ma.asin(ma.sin(lat) * ma.sin(decl) + ma.cos(lat) * ma.cos(decl) * ma.cos(h))
        azimuth = ma.pi - ma.atan2(ma.sin(h), ma.cos(h) * ma.sin(lat) - ma.tan(decl) * ma.cos(lat))
        return elevation, azimuth

    @staticmethod
    def ecliptic2equatorial(lat, long, obl):
        declination = ma.asin(ma.sin(lat) * ma.cos(obl) + ma.cos(lat) * ma.sin(obl) * ma.sin(long)) % (2 * ma.pi)
        right_ascension = ma.atan2(ma.sin(long) * ma.cos(obl) - ma.tan(lat) * ma.sin(obl), ma.cos(long))
        return declination, right_ascension


class SunFromSimplePlanet(SunFromPlanet):
    def __init__(self, revolution_speed, initial_longitude, solar_day_duration,
                 mean_obliquity, mean_anomaly_speed, initial_mean_anomaly, k1, k2):
        super().__init__(revolution_speed, initial_longitude, solar_day_duration)
        self.mean_obliquity = mean_obliquity
        self.mean_anomaly_speed = mean_anomaly_speed
        self.initial_mean_anomaly = initial_mean_anomaly
        self.k1 = k1
        self.k2 = k2

    def ecliptic_coordinates(self, time):
        latitude = 0
        mean_anomaly = (self.mean_anomaly_speed * time + self.initial_mean_anomaly) % (2 * ma.pi)
        mean_longitude = self.mean_longitude(time)
        longitude = (mean_longitude + self.k1 * ma.sin(mean_anomaly) + self.k2 * ma.sin(2 * mean_anomaly)) % (2 * ma.pi)
        return latitude, longitude

    def obliquity(self, time):
        return self.mean_obliquity

    @staticmethod
    def time_coordinate(date):
        """Return the time coordinate for a given date."""
        reference = dt.datetime(2000, 1, 1, 12, 0, 0)  # also known as "J2000.0"
        delta = date - reference
        coordinate = delta.days + cv.seconds2days(delta.seconds)
        return coordinate


class SunFromEarth(SunFromPlanet):
    def __init__(self):
        super().__init__(cv.deg2rad(0.98564736), cv.deg2rad(280.459), 1)

    def ecliptic_coordinates(self, time):
        latitude = 0
        a = cv.deg2rad(0.98560028)
        b = cv.deg2rad(357.529)
        mean_anomaly = (a * time + b) % (2 * ma.pi)
        a = cv.deg2rad(1.915)
        b = cv.deg2rad(0.020)
        mean_longitude = self.mean_longitude(time)
        longitude = (mean_longitude + a * ma.sin(mean_anomaly) + b * ma.sin(2 * mean_anomaly)) % (2 * ma.pi)
        return latitude, longitude

    def obliquity(self, time):
        a = cv.deg2rad(0.00000036)
        b = cv.deg2rad(23.439)
        return (a * time + b) % (2 * ma.pi)

    @staticmethod
    def time_coordinate(date):
        """Return the time coordinate for a given date."""
        reference = dt.datetime(2000, 1, 1, 12, 0, 0)  # also known as "J2000.0"
        delta = date - reference
        coordinate = delta.days + cv.seconds2days(delta.seconds)
        return coordinate


class SunFromCircularEarth(SunFromSimplePlanet):
    def __init__(self):
        revolution_speed = cv.deg2rad(0.98564736)
        initial_longitude = cv.deg2rad(280.459)
        solar_day_duration = 1
        obliquity = cv.deg2rad(23.439)
        mean_anomaly_speed = revolution_speed
        initial_mean_anomaly = 0
        k1 = 0
        k2 = 0
        super().__init__(revolution_speed, initial_longitude, solar_day_duration,
                         obliquity, mean_anomaly_speed, initial_mean_anomaly, k1, k2)


class SunFromEllipticEarth(SunFromSimplePlanet):
    def __init__(self):
        revolution_speed = cv.deg2rad(0.98564736)
        initial_longitude = cv.deg2rad(280.459)
        solar_day_duration = 1
        obliquity = cv.rad2deg(23.439)
        mean_anomaly_speed = revolution_speed
        initial_mean_anomaly = cv.deg2rad(357.529)
        k1 = cv.deg2rad(1.915)
        k2 = cv.deg2rad(0.020)
        super().__init__(revolution_speed, initial_longitude, solar_day_duration,
                         obliquity, mean_anomaly_speed, initial_mean_anomaly, k1, k2)


class SunFromVerticalEarth(SunFromSimplePlanet):
    def __init__(self):
        revolution_speed = cv.deg2rad(0.98564736)
        initial_longitude = cv.deg2rad(280.459)
        solar_day_duration = 1
        obliquity = 0
        mean_anomaly_speed = revolution_speed
        initial_mean_anomaly = cv.deg2rad(357.529)
        k1 = cv.deg2rad(1.915)
        k2 = cv.deg2rad(0.020)
        super().__init__(revolution_speed, initial_longitude, solar_day_duration,
                         obliquity, mean_anomaly_speed, initial_mean_anomaly, k1, k2)


class SunFromCircularVerticalEarth(SunFromSimplePlanet):
    def __init__(self):
        revolution_speed = cv.deg2rad(0.98564736)
        initial_longitude = cv.deg2rad(280.459)
        solar_day_duration = 1
        obliquity = 0
        mean_anomaly_speed = revolution_speed
        initial_mean_anomaly = cv.deg2rad(357.529)
        k1 = 0
        k2 = 0
        super().__init__(revolution_speed, initial_longitude, solar_day_duration,
                         obliquity, mean_anomaly_speed, initial_mean_anomaly, k1, k2)


class SunFromMars(SunFromSimplePlanet):
    def __init__(self):
        revolution_speed = cv.deg2rad(0.52403840)
        initial_longitude = cv.deg2rad(270.3863)
        solar_day_duration = 1 * 1.027491252
        obliquity = cv.deg2rad(25.19)
        mean_anomaly_speed = revolution_speed
        initial_mean_anomaly = cv.deg2rad(19.38)
        k1 = cv.deg2rad(10.691)
        k2 = cv.deg2rad(0.623)
        self.days_per_revolution = 669
        super().__init__(revolution_speed, initial_longitude, solar_day_duration,
                         obliquity, mean_anomaly_speed, initial_mean_anomaly, k1, k2)
