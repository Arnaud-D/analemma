import matplotlib.pyplot as plt
import conversions as cv
import datetime as dt
import numpy as np


def plot_analemma_study(body, body_name, special_place_lat, special_place_long, special_place_name):
    general_long = 0
    hours_of_the_day = [9, 12, 15]
    mean_obliquity = cv.rad2deg(body.obliquity(0))

    # Equatorial
    eq_elevations, eq_azimuths = analemma_list(body, 0, general_long, hours_of_the_day)
    # Tropical
    trop_elevations, trop_azimuths = analemma_list(body, mean_obliquity, general_long, hours_of_the_day)
    # Circumpolar
    cpol_elevations, cpol_azimuths = analemma_list(body, 90 - mean_obliquity, general_long, hours_of_the_day)
    # Polar
    pol_elevations, pol_azimuths = analemma_list(body, 90, general_long, hours_of_the_day)
    # Special place
    sp_elevations, sp_azimuths = analemma_list(body, special_place_lat, special_place_long, hours_of_the_day)
    # Random latitude
    rd_elevations, rd_azimuths = analemma_list(body, np.random.rand() * 90, general_long, hours_of_the_day)

    # Plots
    fig, ax = plt.subplots(2, 3)
    title_prefix = "{} analemma - ".format(body_name)
    for i in range(len(hours_of_the_day)):
        plot_analemma(ax[0, 0], eq_elevations[i], eq_azimuths[i], title_prefix + "Equator")

    for i in range(len(hours_of_the_day)):
        plot_analemma(ax[1, 0], trop_elevations[i], trop_azimuths[i], title_prefix + "Tropic")

    for i in range(len(hours_of_the_day)):
        plot_analemma(ax[0, 1], cpol_elevations[i], cpol_azimuths[i], title_prefix + "Polar circle")

    for i in range(len(hours_of_the_day)):
        plot_analemma(ax[1, 1], pol_elevations[i], pol_azimuths[i], title_prefix + "North Pole")

    for i in range(len(hours_of_the_day)):
        plot_analemma(ax[0, 2], sp_elevations[i], sp_azimuths[i], title_prefix + special_place_name)

    for i in range(len(hours_of_the_day)):
        plot_analemma(ax[1, 2], rd_elevations[i], rd_azimuths[i], title_prefix + "Random place")

    plt.show()


def analemma_list(celestial_body, latitude, longitude, hours_of_the_day):
    elevations_list = []
    azimuths_list = []
    for h in hours_of_the_day:
        eq_el, eq_az = analemma(celestial_body, latitude, longitude, h)
        elevations_list.append(eq_el)
        azimuths_list.append(eq_az)
    return elevations_list, azimuths_list


def analemma(point_of_view, latitude, longitude, hour_of_the_day):
    latitude_rad = cv.deg2rad(latitude)
    longitude_rad = cv.deg2rad(longitude)
    elevations_rad, azimuths_rad = analemma_rad(point_of_view, latitude_rad, longitude_rad, hour_of_the_day)
    elevations = [cv.rad2deg(el_rad) for el_rad in elevations_rad]
    azimuths = [cv.rad2deg(az_rad) for az_rad in azimuths_rad]
    return elevations, azimuths


def analemma_rad(point_of_view, latitude, longitude, hour_of_the_day):
    elevations = []
    azimuths = []
    hour, minute, second = cv.hour2hms(hour_of_the_day)
    date = dt.datetime(2018, 1, 1, hour, minute, second)
    time = point_of_view.time_coordinate(date)
    one_day = point_of_view.one_day

    def position(t):
        return point_of_view.horizontal_coordinates(latitude, longitude, t)

    for d in range(point_of_view.days_per_revolution + 1):
        el, az = position(time)
        elevations.append(el)
        azimuths.append(az)
        time = time + one_day
    return elevations, azimuths


def plot_analemma(axis, elevations, azimuths, title):
    axis.plot(azimuths, elevations)
    axis.set_xlabel("Azimuth (°)")
    axis.set_ylabel("Elevation (°)")
    axis.set_xlim([30, 330])
    axis.set_xticks([30 + i*30 for i in range(11)])
    axis.set_ylim([0, 90])
    axis.set_yticks([i * 15 for i in range(7)])
    axis.set_title(title)
    axis.grid()
