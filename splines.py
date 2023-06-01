import numpy as np
import matplotlib.pyplot as plt


class Spline(object):
    def __init__(self, characteristic_matrix):
        self.characteristic_matrix = characteristic_matrix
        self.spline_points = None
        self.spline_tangents = None
        self.spline_curvature = None

    def get_name(self):
        return self.__class__.__name__

    def get_spline_points(self):
        return self.spline_points

    def get_spline_tangents(self):
        return self.spline_tangents

    def get_spline_curvature(self):
        return self.spline_curvature

    def _get_t_vector(self, t):
        return np.vstack(
            (np.ones(t.shape[0]), np.power(t, 1), np.power(t, 2), np.power(t, 3))
        ).T

    def _get_t_vector_diff(self, t):
        return np.vstack(
            (
                np.zeros(t.shape[0]),
                np.ones(t.shape[0]),
                2 * np.power(t, 1),
                3 * np.power(t, 2),
            )
        ).T

    def _get_t_vector_diff2(self, t):
        return np.vstack(
            (
                np.zeros(t.shape[0]),
                np.zeros(t.shape[0]),
                2 * np.ones(t.shape[0]),
                6 * np.power(t, 1),
            )
        ).T

    def compute_spline(self, control_points, u, reparameterize=True, f=10):
        nb_segments = (
            int((control_points.shape[0] - 1) // 3)
            if self.type == "shifting"
            else control_points.shape[0] - 3
        )

        if np.isscalar(u):
            u = np.array([u])

        if reparameterize and f > 0:
            u = self._reparameterize_mixing_parameter(control_points, u, int(f))

        # segmentID is the integer part => will decide which segment (i.e. set of 4 control points) to use
        # t is the decimal part  => will serve to mix the 4 control points of the segment (t in [0,1])
        t, segmentIDs = np.modf(u * nb_segments)
        segmentIDs = segmentIDs.astype(np.int)
        t[np.where(segmentIDs == nb_segments)] = 1
        segmentIDs[np.where(segmentIDs == nb_segments)] = nb_segments - 1

        t_vector = self._get_t_vector(t)
        t_vector_diff = self._get_t_vector_diff(t)
        t_vector_diff2 = self._get_t_vector_diff2(t)

        spline_points = np.array([]).reshape(0, control_points.shape[1])
        spline_tangents = np.array([]).reshape(0, control_points.shape[1])
        spline_curvature = np.array([])

        uniqueIDs, uniqueIndices, counts = np.unique(
            segmentIDs, return_index=True, return_counts=True
        )
        for unique, index, count in zip(uniqueIDs, uniqueIndices, counts):
            control_points_subset = self._get_control_points_subset(
                control_points, unique
            )

            points = (
                t_vector[index : index + count, :]
                @ self.characteristic_matrix
                @ control_points_subset
            )
            spline_points = np.vstack((spline_points, points))

            points = (
                t_vector_diff[index : index + count, :]
                @ self.characteristic_matrix
                @ control_points_subset
            )
            spline_tangents = np.vstack((spline_tangents, points))

            points = (
                t_vector_diff2[index : index + count, :]
                @ self.characteristic_matrix
                @ control_points_subset
            )
            spline_curvature = np.hstack(
                (spline_curvature, np.linalg.norm(points, axis=1))
            )

        self.spline_points = spline_points
        self.spline_tangents = spline_tangents
        self.spline_curvature = spline_curvature

    def _get_control_points_subset(self, control_points, id):
        if self.type == "shifting":
            return control_points[3 * id : 3 * id + 4]
        elif self.type == "sliding":
            return control_points[id : id + 4]

    def _reparameterize_mixing_parameter(self, control_points, u, f):
        u_resampled = np.linspace(0, 1, f * len(u))
        self.compute_spline(control_points, u_resampled, reparameterize=False)

        norms = np.linalg.norm(np.diff(self.spline_points, axis=0), axis=1)
        cumsum = np.concatenate(([0], np.cumsum(norms)))
        cumsum /= cumsum[-1]

        return np.interp(u, cumsum, u_resampled)

    def plot_basis_functions(self):
        t = np.linspace(0, 1, 50)
        t_vector = self._get_t_vector(t)
        basis_functions = t_vector @ self.characteristic_matrix

        _, ax = plt.subplots()
        for i in range(4):
            ax.plot(t, basis_functions[:, i], label=rf"$w_{i+1}$")
        ax.grid()
        ax.legend()
        ax.set_aspect("equal", "box")
        ax.set_xlim([-0.1, 1.1])
        ax.set_ylim([-0.1, 1.1])
        ax.set_title(f"Basis functions for the {self.get_name()} spline.")
        ax.set_xlabel(r"Mixing parameter $t$")
        ax.set_ylabel(r"Weight $w$")
        plt.show()


class Bezier(Spline):
    def __init__(self):
        characteristic_matrix = np.array(
            [[1, 0, 0, 0], [-3, 3, 0, 0], [3, -6, 3, 0], [-1, 3, -3, 1]]
        )
        super().__init__(characteristic_matrix)
        self.type = "shifting"


class B(Spline):
    def __init__(self):
        characteristic_matrix = (1 / 6) * np.array(
            [[1, 4, 1, 0], [-3, 0, 3, 0], [3, -6, 3, 0], [-1, 3, -3, 1]]
        )
        super().__init__(characteristic_matrix)
        self.type = "sliding"


class Cardinal(Spline):
    def __init__(self, s):
        self.s = s
        characteristic_matrix = np.array(
            [
                [0, 1, 0, 0],
                [-s, 0, s, 0],
                [2 * s, s - 3, 3 - 2 * s, -s],
                [-s, 2 - s, s - 2, s],
            ]
        )
        super().__init__(characteristic_matrix)
        self.type = "sliding"

    def get_name(self):
        return super().get_name() + f" (s={self.s})"


class CatmullRom(Cardinal):
    def __init__(self):
        super().__init__(s=0.5)
