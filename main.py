import matplotlib.pyplot as plt
import numpy as np
from splines import Bezier, CatmullRom, B, Cardinal


def generate_points(n=13):
    angles = np.sort(np.random.uniform(0, 2 * np.pi, n))
    r = np.random.uniform(0.5, 1, n)
    X = r * np.cos(angles)
    Y = r * np.sin(angles)
    return np.vstack((X, Y)).T


def plot(control_points, splines, names, with_tangents=False):
    number_of_splines = len(splines)
    fig, ax = plt.subplots(1, number_of_splines)
    fig.suptitle("Comparison between the implemented splines.")

    for ids, (s, tangents) in enumerate(splines):
        ax[ids].plot(
            control_points[:, 0],
            control_points[:, 1],
            c="k",
            marker=".",
            linestyle="dashed",
            label="control points",
        )

        if s.shape[0] == 1:
            ax[ids].scatter(s[:, 0], s[:, 1], c="r", marker=".", label="spline")
        else:
            ax[ids].plot(s[:, 0], s[:, 1], c="r", label="spline")
        if with_tangents:
            alpha = 0.5
            for i in range(0, s.shape[0]):
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
        ax[ids].legend()
        ax[ids].set_xlim(-1.1, 1.1)
        ax[ids].set_ylim(-1.1, 1.1)
        ax[ids].set_aspect("equal", "box")
    plt.show()


if __name__ == "__main__":
    control_points = generate_points()

    splines = []
    names = []

    u = np.linspace(0, 1, 31)
    for s in [Bezier(), CatmullRom(), B(), Cardinal()]:
        names.append(s.get_name())
        splines.append(s.get_spline(control_points, u))

    plot(control_points, splines, names)
