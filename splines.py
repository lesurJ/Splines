import numpy as np


class Spline(object):
    def __init__(self, characteristic_matrix):
        self.characteristic_matrix = characteristic_matrix

    def get_name(self):
        return self.__class__.__name__

    def get_spline(self, control_points, u):
        nb_segments = (
            int((control_points.shape[0] - 1) // 3)
            if self.type == "shifting"
            else control_points.shape[0] - 3
        )

        if np.isscalar(u):
            u = np.array([u])

        # segmentID is the integer part => will decide which segment (i.e. set of 4 control points) to use
        # t is the decimal part  => will serve to mix the 4 control points of the segment (t in [0,1])
        t, segmentIDs = np.modf(u * nb_segments)
        segmentIDs = segmentIDs.astype(np.int)
        t[np.where(segmentIDs == nb_segments)] = 1
        segmentIDs[np.where(segmentIDs == nb_segments)] = nb_segments - 1

        t_vector = np.vstack(
            (
                np.power(t, 0),
                np.power(t, 1),
                np.power(t, 2),
                np.power(t, 3),
            )
        ).T

        t_vector_diff = np.vstack(
            (
                np.zeros(t.shape[0]),
                np.power(t, 0),
                2 * np.power(t, 1),
                3 * np.power(t, 2),
            )
        ).T

        spline_points = np.zeros(shape=(0, control_points.shape[1]))
        spline_tangents = np.zeros(shape=(0, control_points.shape[1]))

        uniqueIDs, uniqueIndices, counts = np.unique(
            segmentIDs, return_index=True, return_counts=True
        )
        for unique, index, count in zip(uniqueIDs, uniqueIndices, counts):
            points = (
                t_vector[index : index + count, :]
                @ self.characteristic_matrix
                @ self.get_set_of_control_points(control_points, unique)
            )
            spline_points = np.vstack((spline_points, points))
            points = (
                t_vector_diff[index : index + count, :]
                @ self.characteristic_matrix
                @ self.get_set_of_control_points(control_points, unique)
            )
            spline_tangents = np.vstack((spline_tangents, points))
        return spline_points, spline_tangents

    def get_set_of_control_points(self, control_points, id):
        if self.type == "shifting":
            return control_points[3 * id : 3 * id + 4]
        elif self.type == "sliding":
            return control_points[id : id + 4]


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


class CatmullRom(Cardinal):
    def __init__(self):
        super().__init__(s=0.5)
