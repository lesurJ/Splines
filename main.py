import matplotlib.pyplot as plt
import numpy as np
from splines import Bezier, CatmullRom, B, Cardinal


def generate_points(n=10):
    angles = np.sort(np.random.uniform(0, 2 * np.pi, n))
    r = np.random.uniform(0.7, 1, n)
    X = r * np.cos(angles)
    Y = r * np.sin(angles)
    return np.vstack((X, Y)).T


def plot(control_points, splines, names):
    number_of_splines = len(splines)
    fig, ax = plt.subplots(1, number_of_splines)
    fig.suptitle("Comparison between the different implemented splines.")

    for ids, (s, tangents) in enumerate(splines):
        ax[ids].plot(
            control_points[:, 0],
            control_points[:, 1],
            c="k",
            marker=".",
            linestyle="dashed",
            label="control points",
        )

        ax[ids].plot(s[:, 0], s[:, 1], c="r")
        alpha = 0.5
        for i in range(0, s.shape[0], 5):
            ax[ids].arrow(
                s[i, 0],
                s[i, 1],
                alpha * tangents[i, 0],
                alpha * tangents[i, 1],
                length_includes_head=True,
                head_width=0.01,
                color="b",
            )

        ax[ids].set_title(names[ids])
        ax[ids].grid()
        ax[ids].set_xlim(-1.25, 1.25)
        ax[ids].set_ylim(-1.25, 1.25)
        ax[ids].set_aspect("equal", "box")
    plt.show()


if __name__ == "__main__":
    control_points = generate_points()

    splines = []
    names = []

    for s in [Bezier(), CatmullRom(), B(), Cardinal()]:
        names.append(s.get_name())
        splines.append(s.get_spline(control_points, 50))

    plot(control_points, splines, names)
