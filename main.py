import matplotlib.pyplot as plt
import numpy as np
from splines import Bezier, CatmullRom, B_spline


def generate_points(n=10):
    angles = np.sort(np.random.uniform(0, 2 * np.pi, n))
    r = np.random.uniform(0.7, 1, n)
    X = r * np.cos(angles)
    Y = r * np.sin(angles)
    return np.vstack((X, Y)).T


def plot(control_points, splines, names):
    _, ax = plt.subplots()
    ax.plot(
        control_points[:, 0],
        control_points[:, 1],
        c="k",
        marker=".",
        linestyle="dashed",
        label="control points",
    )
    for s, n in zip(splines, names):
        ax.plot(s[:, 0], s[:, 1], label=n)

    ax.legend()
    ax.grid()
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal", "box")
    plt.show()


if __name__ == "__main__":
    control_points = generate_points()

    splines = []
    names = []

    for s in [Bezier(), CatmullRom(), B_spline()]:
        names.append(s.get_name())
        splines.append(s.get_spline(control_points, 50))

    plot(control_points, splines, names)
