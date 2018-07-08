import math

rad_per_deg = math.pi / 180
deg_per_rad = 180 / math.pi
minutes_per_hour = 60
seconds_per_hour = 3600
seconds_per_minute = 60
seconds_per_day = 86400


def rad2deg(a):
    return a * deg_per_rad


def deg2rad(a):
    return a * rad_per_deg


def hour2hms(h):
    hour = int(math.floor(h))
    minute = int((h % 1) * minutes_per_hour)
    second = int(((h // 60) % 1) * seconds_per_hour)
    return hour, minute, second


def seconds2days(s):
    return s / seconds_per_day


def hours2rad(h):
    return h / 24 * 2 * math.pi
