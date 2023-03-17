import numpy as np


class Spline(object):
    def __init__(self, characteristic_matrix):
        self.characteristic_matrix = characteristic_matrix

    def get_name(self):
        return self.__class__.__name__

    def get_spline(self, control_points, number_of_interpolated_points):
        lin_sp = np.linspace(0, 1, number_of_interpolated_points)
        t_vector = np.vstack(
            (
                np.power(lin_sp, 0),
                np.power(lin_sp, 1),
                np.power(lin_sp, 2),
                np.power(lin_sp, 3),
            )
        ).T

        t_vector_diff = np.vstack(
            (
                np.zeros(number_of_interpolated_points),
                np.power(lin_sp, 0),
                2 * np.power(lin_sp, 1),
                3 * np.power(lin_sp, 2),
            )
        ).T

        nb_sub_spline = (
            len(control_points) // 3
            if self.type == "shifting"
            else len(control_points) - 3
        )
        shift = -3 if self.type == "shifting" else -1

        spline_points = np.zeros(shape=(0, control_points.shape[1]))
        spline_tangent_points = np.zeros(shape=(0, control_points.shape[1]))
        for _ in range(nb_sub_spline):
            points = t_vector @ self.characteristic_matrix @ control_points[:4]
            spline_points = np.vstack((spline_points, points[:-1, :]))
            points = t_vector_diff @ self.characteristic_matrix @ control_points[:4]
            spline_tangent_points = np.vstack((spline_tangent_points, points[:-1, :]))

            control_points = np.roll(control_points, shift=shift, axis=0)
        return spline_points, spline_tangent_points


class Bezier(Spline):
    def __init__(self):
        characteristic_matrix = np.array(
            [[1, 0, 0, 0], [-3, 3, 0, 0], [3, -6, 3, 0], [-1, 3, -3, 1]]
        )
        super().__init__(characteristic_matrix)
        self.type = "shifting"


class CatmullRom(Spline):
    def __init__(self):
        characteristic_matrix = 0.5 * np.array(
            [[0, 2, 0, 0], [-1, 0, 1, 0], [2, -5, 4, -1], [-1, 3, -3, 1]]
        )
        super().__init__(characteristic_matrix)
        self.type = "sliding"


class B(Spline):
    def __init__(self):
        characteristic_matrix = (1 / 6) * np.array(
            [[1, 4, 1, 0], [-3, 0, 3, 0], [3, -6, 3, 0], [-1, 3, -3, 1]]
        )
        super().__init__(characteristic_matrix)
        self.type = "sliding"


class Cardinal(Spline):
    def __init__(self, s=0.25):
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
