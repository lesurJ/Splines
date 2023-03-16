import numpy as np


class Spline(object):
    def __init__(self, characteristic_matrix, dimension=2):
        self.dim = dimension
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
        return self._get_spline(control_points, t_vector)


class FullSpline(Spline):
    def __init__(self, characteristic_matrix):
        super().__init__(characteristic_matrix)

    def _get_spline(self, control_points, t_vector):
        nb_sub_spline = len(control_points) // 3
        out = np.zeros(shape=(0, self.dim))

        for _ in range(nb_sub_spline):
            points = t_vector @ self.characteristic_matrix @ control_points[:4]
            out = np.vstack((out, points))
            control_points = np.roll(control_points, shift=-3, axis=0)
        return out


class PartialSpline(Spline):
    def __init__(self, characteristic_matrix):
        super().__init__(characteristic_matrix)

    def _get_spline(self, control_points, t_vector):
        nb_sub_spline = len(control_points) - 3
        out = np.zeros(shape=(0, self.dim))

        for _ in range(nb_sub_spline):
            points = t_vector @ self.characteristic_matrix @ control_points[:4]
            out = np.vstack((out, points))
            control_points = np.roll(control_points, shift=-1, axis=0)
        return out


class Bezier(FullSpline):
    def __init__(self):
        characteristic_matrix = np.array(
            [[1, 0, 0, 0], [-3, 3, 0, 0], [3, -6, 3, 0], [-1, 3, -3, 1]]
        )
        super().__init__(characteristic_matrix)


class CatmullRom(PartialSpline):
    def __init__(self):
        characteristic_matrix = 0.5 * np.array(
            [[0, 2, 0, 0], [-1, 0, 1, 0], [2, -5, 4, -1], [-1, 3, -3, 1]]
        )
        super().__init__(characteristic_matrix)


class B_spline(PartialSpline):
    def __init__(self):
        characteristic_matrix = (1 / 6) * np.array(
            [[1, 4, 1, 0], [-3, 0, 3, 0], [3, -6, 3, 0], [-1, 3, -3, 1]]
        )
        super().__init__(characteristic_matrix)
