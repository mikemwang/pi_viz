import math
import pygame
from pygame.math import Vector2, Vector3
import numpy as np


class Actor:

    def __init__(self,
                 position: Vector2,
                 velocity: Vector2,
                 length: float,
                 width: float,
                 color=(0, 0, 0),
                 max_speed=200,
                 max_acceleration=200):
        self.position = position
        self.velocity = velocity
        self.acceleration = Vector2(0, 0)
        self.length = length
        self.width = width
        self.color = color
        self.body_pts = None
        self.transformed_pts = None

        self.max_speed = max_speed
        self.max_speed_squared = self.max_speed**2
        self.max_acceleration = max_acceleration  # lower = more "inertia"
        self.max_acceleration_squared = self.max_acceleration**2

    def local_pts(self):
        """ Calculate all visualization points in the local coordinate system
        """
        # the body of the actor
        self.body_pts = np.array([[self.length/2, 0],
                                  [-self.length/2, -self.width/2],
                                  [-self.length/4, 0],
                                  [-self.length/2, self.width/2]])

        return self.body_pts

    def rotate(self, pts, vec: Vector2):
        theta = math.atan2(vec.y, vec.x)
        cos = math.cos(theta)
        sin = math.sin(theta)

        return np.array([[cos, -sin], [sin, cos]]).dot(pts.T).T

    def translate(self, pts, delta: Vector2):
        return pts + delta

    def apply_force(self, force: Vector2, dt):
        self.acceleration += force*dt

    def apply_velocity(self, dt):
        self.velocity += self.acceleration*dt

        if self.velocity.length_squared() > self.max_speed_squared:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity*dt

    def limit_acceleration(self):
        if self.acceleration.length_squared() > self.max_acceleration_squared:
            self.acceleration.scale_to_length(self.max_acceleration)

    def update(self, dt_ms):
        dt = dt_ms / 1000.0
        self.apply_force(Vector2(-100000.0, 0), dt)
        self.limit_acceleration()
        self.apply_velocity(dt)

    def render(self, surface):
        self.transformed_pts = self.translate(
            self.rotate(self.local_pts(), self.velocity), self.position)
        pygame.draw.polygon(surface,
                            self.color,
                            [row for row in self.transformed_pts],
                            3)

    def animate(self, surface, dt_ms):
        self.update(dt_ms)
        self.render(surface)
