import numpy as np


class Pose:
    def __init__(self, x, y, theta):
        self._pose = np.array([x, y, theta])

    @property
    def pose(self):
        return self._pose

    @pose.setter
    def pose(self, new_pose: np.array):
        if not isinstance(new_pose, np.ndarray):
            raise TypeError(f"{type(new_pose)} is not of type np.ndarray")

        if new_pose.shape != self._pose.shape:
            raise ValueError(
                f"Attempted to set pose with shape {new_pose.shape} that is unlike {self._pose.shape}")
        self._pose = new_pose

    @property
    def position(self):
        return self._pose[:2]

    @property
    def theta(self):
        return self._pose[2]

    @property
    def x(self):
        return self._pose[0]

    @property
    def y(self):
        return self._pose[1]


if __name__ == "__main__":
    a = Pose(1, 2, 3)
    print(a.pose)
    a.pose = np.array([3, 2, 1])
    print(a.pose)
    print(a.position)
    print(a.theta)
