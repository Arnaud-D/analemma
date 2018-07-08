import matplotlib.pyplot as plt
import conversions as cv
import datetime as dt
import numpy as np


def plot_analemma_study(body, body_name, special_place_lat, special_place_long, special_place_name):
    # Data
    general_long = 0
    hours_of_the_day = [9, 12, 15]
    mean_obliquity = cv.rad2deg(body.obliquity(0))
    max_lat = 90

    # Analemmas
    eq_el, eq_az = analemma_list(body, 0, general_long, hours_of_the_day)  # Equatorial
    trop_el, trop_az = analemma_list(body, mean_obliquity, general_long, hours_of_the_day)  # Tropical
    cpol_el, cpol_az = analemma_list(body, max_lat - mean_obliquity, general_long, hours_of_the_day)  # Circumpolar
    pol_el, pol_az = analemma_list(body, max_lat, general_long, hours_of_the_day)  # Polar
    sp_el, sp_az = analemma_list(body, special_place_lat, special_place_long, hours_of_the_day)  # Special place
    rd_el, rd_az = analemma_list(body, np.random.rand() * max_lat, general_long, hours_of_the_day)  # Random place

    # Plots
    fig, ax = plt.subplots(2, 3)
    title_prefix = "{} analemma - ".format(body_name)
    for i in range(len(hours_of_the_day)):
        plot_analemma(ax[0, 0], eq_el[i], eq_az[i], title_prefix + "Equator")
        plot_analemma(ax[1, 0], trop_el[i], trop_az[i], title_prefix + "Tropic")
        plot_analemma(ax[0, 1], cpol_el[i], cpol_az[i], title_prefix + "Polar circle")
        plot_analemma(ax[1, 1], pol_el[i], pol_az[i], title_prefix + "North Pole")
        plot_analemma(ax[0, 2], sp_el[i], sp_az[i], title_prefix + special_place_name)
        plot_analemma(ax[1, 2], rd_el[i], rd_az[i], title_prefix + "Random place")

    plt.show()


def plot_analemma(axis, elevations, azimuths, title):
    axis.plot(azimuths, elevations, '.')
    axis.lines[-1].set_markersize(0.2)
    axis.set_xlabel("Azimuth (°)")
    axis.set_xlim([0, 360])
    axis.set_xticks([i * 60 for i in range(7)])
    axis.set_ylabel("Elevation (°)")
    axis.set_ylim([0, 90])
    axis.set_yticks([i * 15 for i in range(7)])
    axis.set_title(title)
    axis.grid()


def analemma_list(celestial_body, latitude, longitude, hours_of_the_day):
    elevations_list = []
    azimuths_list = []
    for h in hours_of_the_day:
        eq_el, eq_az = analemma(celestial_body, latitude, longitude, h)
        elevations_list.append(eq_el)
        azimuths_list.append(eq_az)
    return elevations_list, azimuths_list


def analemma(celestial_body, latitude, longitude, hour_of_the_day):
    latitude_rad = cv.deg2rad(latitude)
    longitude_rad = cv.deg2rad(longitude)
    elevations_rad, azimuths_rad = analemma_rad(celestial_body, latitude_rad, longitude_rad, hour_of_the_day)
    elevations = [cv.rad2deg(el_rad) for el_rad in elevations_rad]
    azimuths = [cv.rad2deg(az_rad) for az_rad in azimuths_rad]
    return elevations, azimuths


def analemma_rad(celestial_body, latitude, longitude, hour_of_the_day):
    initial_midnight = dt.datetime(2000, 1, 1, 0, 0, 0)
    one_day = celestial_body.solar_day_duration
    fractional_day = hour_of_the_day / 24 * one_day
    initial_time = celestial_body.time_coordinate(initial_midnight) + fractional_day
    elevations = []
    azimuths = []
    observation_times = [initial_time + n * one_day for n in range(celestial_body.days_per_revolution + 1)]
    for t in observation_times:
        e, a = celestial_body.horizontal_coordinates(latitude, longitude, t)
        elevations.append(e)
        azimuths.append(a)

    return elevations, azimuths
