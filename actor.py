import math
import pygame
import random
from pygame.math import Vector2, Vector3
import numpy as np


class Actor:

    def __init__(self,
                 surface,
                 position: Vector2,
                 length: float,
                 width: float,
                 color=(0, 0, 0),
                 max_speed=200,
                 max_acceleration=200):
        self.surface = surface
        self.position = position
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.length = length
        self.width = width
        self.color = color
        self.body_pts = None
        self.transformed_pts = None

        self.goal = None

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

    def seek(self, pt, dt, weight=1):
        desired = pt - self.position
        desired.scale_to_length(self.max_speed)
        steer = desired - self.velocity
        steer.scale_to_length(min(steer.length(), self.max_acceleration))
        self.apply_force(weight*steer, dt)
        #stopping_distance = 0.5 * self.velocity.length_squared() / self.max_acceleration

        # if vec.length() < 1.1*stopping_distance:
        #    self.apply_force(Vector2(self.max_acceleration, 0).rotate(
        #        self.velocity.as_polar()[1]-180), dt)
        # else:
        #    self.apply_force(weight*vec, dt)

    def avoid(self, pt, dt, weight=50):
        vec = pt - self.position
        vec.scale_to_length(10000/vec.length())
        self.apply_force(weight*vec.rotate(180), dt)
        pygame.draw.line(self.surface, (255, 0, 0), self.position,
                         self.position+weight*vec.rotate(180)*dt)

    def update(self, dt_ms):
        dt = dt_ms / 1000.0
        self.acceleration.xy = 0, 0

        if not self.goal or (self.position - self.goal).length_squared() < 400:
            self.goal = Vector2(random.random()*1920, random.random()*1080)
        pygame.draw.circle(self.surface, self.color, self.goal, 10)
        self.seek(self.goal, dt, weight=50)
        #self.avoid(Vector2(400, 325), dt, weight=50)
        # self.limit_acceleration()
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
