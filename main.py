import matplotlib.pyplot as plt
import numpy as np
from splines import Bezier, CatmullRom, B, Cardinal


def generate_points(random=False):
    if random:
        n = 13
        angles = np.sort(np.random.uniform(0, 2 * np.pi, n))
        r = np.random.uniform(0.5, 1, n)
        X = r * np.cos(angles)
        Y = r * np.sin(angles)
        control_points = np.vstack((X, Y)).T
    else:
        control_points = np.array(
            [[0, 0], [0, 1], [1, 0], [2, 0], [2, 1], [1.2, 0.4], [1, 1]]
        )
    return control_points


def overall_plot(control_points, splines, with_tangents=False):
    fig, ax = plt.subplots(4, 2, height_ratios=[4, 1, 4, 1], figsize=(7, 7))
    fig.suptitle(
        "Comparison between the implemented splines and their associated curvatures."
    )
    fig.tight_layout()

    for ids, s in enumerate(splines):
        spline_points = s.get_spline_points()

        id1, id2 = np.divmod(ids, 2)
        id1 *= 2
        ax[id1][id2].plot(
            control_points[:, 0],
            control_points[:, 1],
            c="k",
            marker=".",
            linestyle="dashed",
            label="control points",
        )

        if spline_points.shape[0] == 1:
            ax[id1][id2].scatter(
                spline_points[0, 0],
                spline_points[0, 1],
                c="r",
                label="spline",
            )
        else:
            ax[id1][id2].plot(
                spline_points[:, 0],
                spline_points[:, 1],
                c="r",
                label="spline",
            )

        if with_tangents:
            alpha = 0.5
            spline_tangents = s.get_spline_tangents()
            for i in range(0, spline_points.shape[0]):
                ax[id1][id2].arrow(
                    spline_points[i, 0],
                    spline_points[i, 1],
                    alpha * spline_tangents[i, 0],
                    alpha * spline_tangents[i, 1],
                    length_includes_head=True,
                    head_width=0.01,
                    color="b",
                )

        ax[id1][id2].set_title(s.get_name())
        ax[id1][id2].grid()
        ax[id1][id2].legend()
        ax[id1][id2].set_aspect("equal", "box")

        spline_curvature = s.get_spline_curvature()
        ax[id1 + 1][id2].plot(spline_curvature, linestyle="dashed", c="k")
        ax[id1 + 1][id2].scatter(np.arange(spline_curvature.shape[0]), spline_curvature)
        ax[id1 + 1][id2].grid()
    plt.show()


if __name__ == "__main__":
    control_points = generate_points()

    splines = [Bezier(), CatmullRom(), B(), Cardinal(s=0.25)]
    u = np.linspace(0, 1, 100)

    for s in splines:
        s.compute_spline(control_points, u)
        s.plot()
        s.plot_basis_functions()

    overall_plot(control_points, splines)
