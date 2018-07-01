import analemma as an
import bodies as pov


def main():
    print("This is Analemma v0.5.0")
    an.plot_analemma_study(pov.SunFromEarth(), "Earth", 51.477, 0, "Greenwich")
    an.plot_analemma_study(pov.SunFromCircularEarth(), "Circular Earth", 51.477, 0, "Greenwich")
    an.plot_analemma_study(pov.SunFromVerticalEarth(), "Vertical Earth", 51.477, 0, "Greenwich")
    an.plot_analemma_study(pov.SunFromCircularVerticalEarth(), "Vertical Circular Earth", 51.477, 0, "Greenwich")
    an.plot_analemma_study(pov.SunFromMars(), "Mars", 4.59, 137.44, "Curiosity")


if __name__ == "__main__":
    main()
