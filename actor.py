import math
import pygame
from pygame.math import Vector2, Vector3
import numpy as np


class Actor:

    def __init__(self,
                 pose: np.array,
                 length: float,
                 width: float,
                 color=(0, 0, 0)):
        self.pose = pose  # x, y, heading in radians
        self.length = length
        self.width = width
        self.color = color
        self.speed = 0  # cannot reverse, so no negative
        self.steer = 0  # negative is left of centerline, right is positive
        self.max_steer_radians = math.pi/4
        self.max_steer_rate = math.pi/4  # radians / sec
        self.max_speed = 35
        self.body_pts = None
        self.transformed_pts = None

    def local_pts(self):
        """ Calculate all visualization points in the local coordinate system
        """
        # the body of the actor
        self.body_pts = np.array([[self.length/2, 0],
                                  [-self.length/2, -self.width/2],
                                  [-self.length/4, 0],
                                  [-self.length/2, self.width/2]])

        return self.body_pts

    def rotate(self, pts, theta):
        cos = math.cos(theta)
        sin = math.sin(theta)

        return np.array([[cos, -sin], [sin, cos]]).dot(pts.T).T

    def translate(self, pts, delta):
        return pts + delta

    def update(self, dt):
        seconds = dt / 1000.0

        if self.steer != 0:
            # positive if rightward steering
            r = (self.length - self.width/3) / math.cos(math.pi/2 - self.steer)

            # the origin of the steering circle is determined also by the
            # heading of the car, i.e. pose[2]
            c = np.array([[0, r]])
            c = self.rotate(c, self.pose[2])

        # we'll use the steer angle to create a circular path whose radius is
        # infinite (i.e. no steering) when steer angle is 0
        # and coincident with the center of the actor when steer angle is PI/2

        # TODO: apply acceleration to velocity
        #self.pos += self.speed*self.heading*seconds
        self.pose[2] += seconds

    def render(self, surface):
        self.transformed_pts = self.translate(
            self.rotate(self.local_pts(), self.pose[2]), self.pose[:2])
        pygame.draw.polygon(surface,
                            self.color,
                            [row for row in self.transformed_pts],
                            3)
        pygame.draw.circle(surface,
                           self.color,
                           self.pose[0:2],
                           3,
                           0)
