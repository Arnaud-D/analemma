import datetime as dt
import conversions as cv
import numpy as np

days_per_year = int(668.59 * 1.027)
one_day = 1


def time_coordinate(date):
    """Return the time coordinate for a given date."""
    reference = dt.datetime(2000, 1, 1, 12, 0, 0)  # also known as "J2000.0"
    delta = date - reference
    coordinate = delta.days + cv.seconds2days(delta.seconds)
    return coordinate


def sun_horizontal_coordinates(latitude, longitude, time):
    """Return the position of the sun in the horizontal coordinates system."""
    sun_latitude, sun_longitude = sun_ecliptic_coordinates(time)
    obliquity = mars_obliquity(time)
    declination, right_ascension = ecliptic2equatorial(sun_latitude, sun_longitude, obliquity)
    teq = equation_time(time)
    hour_angle = np.pi - (((time - 0.5) * 24) * cv.deg2rad(15) + longitude + teq)
    elevation, azimuth = equatorial2horizontal(latitude, longitude, declination, hour_angle)
    return elevation, azimuth


def equation_time(time):
    sun_latitude, sun_longitude = sun_ecliptic_coordinates(time)
    obliquity = mars_obliquity(time)
    _, right_ascension = ecliptic2equatorial(sun_latitude, sun_longitude, obliquity)
    teq = (sun_mean_longitude(time) - right_ascension) % (2 * np.pi)
    return teq


def sun_mean_longitude(time):
    a = cv.deg2rad(0.52403840)
    b = cv.deg2rad(270.3863)
    mean_longitude = (a * time + b) % (2 * np.pi)
    return mean_longitude


def sun_ecliptic_coordinates(time):
    """Return the position of the sun in the ecliptic coordinate system."""
    latitude = cv.deg2rad(1.85)
    a = cv.deg2rad(0.52402075)
    b = cv.deg2rad(19.38)
    mean_anomaly = (a * time + b) % (2 * np.pi)
    a = cv.deg2rad(10.691)
    b = cv.deg2rad(0.623)
    mean_longitude = sun_mean_longitude(time)
    longitude = (mean_longitude + a * np.sin(mean_anomaly) + b * np.sin(2 * mean_anomaly)) % (2 * np.pi)
    return latitude, longitude


def mars_obliquity(time):
    a = cv.deg2rad(0)
    b = cv.deg2rad(25.19)
    obliquity = (a * time + b) % (2 * np.pi)
    return obliquity


def ecliptic2equatorial(lat, long, obl):
    declination = np.arcsin(np.sin(lat) * np.cos(obl) + np.cos(lat) * np.sin(obl) * np.sin(long)) % (2 * np.pi)
    right_ascension = np.arctan2(np.sin(long) * np.cos(obl) - np.tan(lat) * np.sin(obl), np.cos(long))
    return declination, right_ascension


def equatorial2horizontal(lat, _, decl, h):
    elevation = np.arcsin(np.sin(lat) * np.sin(decl) + np.cos(lat) * np.cos(decl) * np.cos(h))
    azimuth = np.pi - np.arctan2(np.sin(h), np.cos(h) * np.sin(lat) - np.tan(decl) * np.cos(lat))
    return elevation, azimuth