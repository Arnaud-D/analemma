import analemma as an
import conversions as cv
import matplotlib.pyplot as plt
import marsposition as mp
import earthposition as ep


def paris_analemma():
    latitude = 48.8589507
    longitude = 2.2770205
    hour_of_the_day = 10
    elevations, azimuths = an.analemma(latitude, longitude, hour_of_the_day, ep)
    hour, minute, second = cv.hour2hms(hour_of_the_day)
    title = "Analemme à Paris à {:02.0f}h{:02.0f}".format(hour, minute, second)
    an.plot(elevations, azimuths, title)


def tropic_analemma():
    latitude = 23.439
    longitude = 0
    hour_of_the_day = 12
    elevations, azimuths = an.analemma(latitude, longitude, hour_of_the_day, ep)
    hour, minute, second = cv.hour2hms(hour_of_the_day)
    title = "Analemme au tropique du Cancer à {:02.0f}h{:02.0f}".format(hour, minute, second)
    an.plot(elevations, azimuths, title)


def pole_analemma():
    latitude = 90
    longitude = 0
    hour_of_the_day = 12
    elevations, azimuths = an.analemma(latitude, longitude, hour_of_the_day, ep)
    hour, minute, second = cv.hour2hms(hour_of_the_day)
    title = "Analemme au pôle Nord à {:02.0f}h{:02.0f}".format(hour, minute, second)
    an.plot(elevations, azimuths, title)


def pathfinder_analemma():
    latitude = 19.125
    longitude = 33.25
    # hour_of_the_day = 9 + 50/60
    hour_of_the_day = 14.5
    elevations, azimuths = an.analemma(latitude, longitude, hour_of_the_day, mp)
    hour, minute, second = cv.hour2hms(hour_of_the_day)
    title = "Analemme à proximité de Pathfinder {:02.0f}h{:02.0f}".format(hour, minute, second)
    an.plot(elevations, azimuths, title)


def multiple_analemmas():
    latitude = 48.8589507
    longitude = 2.2770205
    hour_of_the_day = [i for i in range(1, 24)]
    elevations_seq = []
    azimuths_seq = []
    for h in hour_of_the_day:
        elevations, azimuths = an.analemma(latitude, longitude, h, ep)
        elevations_seq.append(elevations)
        azimuths_seq.append(azimuths)

    plt.figure()
    for i in range(len(hour_of_the_day)):
        plt.plot(azimuths_seq[i], elevations_seq[i])
    plt.grid()
    plt.xlim([0, 360])
    plt.xticks([i*60 for i in range(7)])
    plt.ylim([-90, 90])
    plt.yticks([-90 + i * 30 for i in range(7)])
    plt.title("Analemmes à différentes heures de la journée à Paris.")
    plt.xlabel("Azimuth (°)")
    plt.ylabel("Élévation (°)")
    plt.show()


def main():
    print("This is Analemma v0.3.0")
    pathfinder_analemma()
    paris_analemma()
    tropic_analemma()
    pole_analemma()
    multiple_analemmas()


if __name__ == "__main__":
    main()
