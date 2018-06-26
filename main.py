import analemma as an
import conversions as cv


def paris_analemma():
    latitude = 48.8589507
    longitude = 2.2770205
    hour_of_the_day = 10
    elevations, azimuths = an.analemma(latitude, longitude, hour_of_the_day)
    hour, minute, second = cv.hour2hms(hour_of_the_day)
    title = "Analemme à Paris à {:02.0f}h{:02.0f}".format(hour, minute, second)
    an.plot(elevations, azimuths, title)


def tropic_analemma():
    latitude = 23.439
    longitude = 0
    hour_of_the_day = 12
    elevations, azimuths = an.analemma(latitude, longitude, hour_of_the_day)
    hour, minute, second = cv.hour2hms(hour_of_the_day)
    title = "Analemme au tropique du Cancer à {:02.0f}h{:02.0f}".format(hour, minute, second)
    an.plot(elevations, azimuths, title)


def pole_analemma():
    latitude = 90
    longitude = 0
    hour_of_the_day = 12
    elevations, azimuths = an.analemma(latitude, longitude, hour_of_the_day)
    hour, minute, second = cv.hour2hms(hour_of_the_day)
    title = "Analemme au pôle Nord à {:02.0f}h{:02.0f}".format(hour, minute, second)
    an.plot(elevations, azimuths, title)


def main():
    print("This is Analemma v0.2.0")
    paris_analemma()
    tropic_analemma()
    pole_analemma()


if __name__ == "__main__":
    main()
