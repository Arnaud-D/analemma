import analemma as an
import bodies


def main():
    print("This is Analemma v1.0.0")
    an.plot_analemma_study(bodies.SunFromEarth(), "Earth", 51.477, 0, "Greenwich")
    an.plot_analemma_study(bodies.SunFromCircularEarth(), "Circular Earth", 51.477, 0, "Greenwich")
    an.plot_analemma_study(bodies.SunFromVerticalEarth(), "Vertical Earth", 51.477, 0, "Greenwich")
    an.plot_analemma_study(bodies.SunFromCircularVerticalEarth(), "Vertical Circular Earth", 51.477, 0, "Greenwich")
    an.plot_analemma_study(bodies.SunFromMars(), "Mars", 4.59, 137.44, "Curiosity")
    an.plot_analemma_study(bodies.SunFromMars(), "Mars", 19.13, 0, "Pathfinder")


if __name__ == "__main__":
    main()
