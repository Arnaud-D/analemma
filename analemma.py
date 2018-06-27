import matplotlib.pyplot as plt
import conversions as cv
import datetime as dt


def analemma(latitude, longitude, hour_of_the_day, module):
    latitude_rad = cv.deg2rad(latitude)
    longitude_rad = cv.deg2rad(longitude)
    elevations_rad, azimuths_rad = analemma_rad(latitude_rad, longitude_rad, hour_of_the_day, module)
    elevations = [cv.rad2deg(el_rad) for el_rad in elevations_rad]
    azimuths = [cv.rad2deg(az_rad) for az_rad in azimuths_rad]
    return elevations, azimuths


def analemma_rad(latitude, longitude, hour_of_the_day, module):
    elevations = []
    azimuths = []
    hour, minute, second = cv.hour2hms(hour_of_the_day)
    date = dt.datetime(2018, 1, 1, hour, minute, second)
    time = module.time_coordinate(date)
    one_day = module.one_day
    for d in range(module.days_per_year + 1):
        el, az = module.sun_horizontal_coordinates(latitude, longitude, time)
        elevations.append(el)
        azimuths.append(az)
        time = time + one_day
    return elevations, azimuths


def plot(elevations, azimuths, title):
    plt.figure()
    plt.plot(azimuths, elevations)
    plt.xlabel("Azimuth (°)")
    plt.ylabel("Elevation (°)")
    plt.title(title)
    plt.grid()
    plt.show()
