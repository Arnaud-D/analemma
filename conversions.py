from math import pi

rad_per_deg = pi / 180   # number of radians per degrees
deg_per_rad = 180 / pi  # number of degrees per radians
minutes_per_hour = 60  # number of minutes per hour
seconds_per_hour = 3600  # number of seconds per hour
seconds_per_minute = 60  # number of seconds per minutes
seconds_per_day = 86400  # number of seconds per day


def rad2deg(a):
    """Convert radians to degrees."""
    return a * deg_per_rad


def deg2rad(a):
    """Convert degrees to radians."""
    return a * rad_per_deg


def seconds2days(s):
    """Convert seconds to days (1 day = 86400 seconds)."""
    return s / seconds_per_day


def hours2rad(h):
    """Convert hours to radians (24 h = 2 pi rad)."""
    return h / 24 * 2 * pi
