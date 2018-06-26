import matplotlib.pyplot as plt
import conversions as cv
import datetime as dt
import earthposition as ep

days_per_year = 365


def analemma(latitude, longitude, hour_of_the_day):
    latitude_rad = cv.deg2rad(latitude)
    longitude_rad = cv.deg2rad(longitude)
    elevations_rad, azimuths_rad = analemma_rad(latitude_rad, longitude_rad, hour_of_the_day)
    elevations = [cv.rad2deg(el_rad) for el_rad in elevations_rad]
    azimuths = [cv.rad2deg(az_rad) for az_rad in azimuths_rad]
    return elevations, azimuths


def analemma_rad(latitude, longitude, hour_of_the_day):
    elevations = []
    azimuths = []
    hour, minute, second = cv.hour2hms(hour_of_the_day)
    date = dt.datetime(2018, 1, 1, hour, minute, second)
    one_day = dt.timedelta(1)
    for d in range(days_per_year + 1):
        time = ep.time_coordinate(date)
        el, az = ep.sun_horizontal_coordinates(latitude, longitude, time)
        elevations.append(el)
        azimuths.append(az)
        date += one_day
    return elevations, azimuths


def plot(elevations, azimuths, title):
    plt.figure()
    plt.plot(azimuths, elevations)
    plt.xlabel("Azimuth (°)")
    plt.ylabel("Elevation (°)")
    plt.title(title)
    plt.grid()
    plt.show()
