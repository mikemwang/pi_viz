import math
import pygame
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

        self.max_speed = max_speed
        self.max_speed_squared = self.max_speed**2
        self.max_acceleration = max_acceleration  # lower = more "inertia"
        self.max_acceleration_squared = self.max_acceleration**2
        self.arrival_radius_sq = 200**2

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
        if self.velocity.length_squared() == 0:
            self.velocity += self.acceleration*dt
        elif self.velocity.length_squared() > self.max_speed_squared:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity*dt

    def limit_acceleration(self):
        if self.acceleration.length_squared() > self.max_acceleration_squared:
            self.acceleration.scale_to_length(self.max_acceleration)

    def seek(self, pt, dt, weight=1):
        desired = pt - self.position
        if desired.length_squared() > self.arrival_radius_sq:
            desired.scale_to_length(self.max_speed)
        else:
            desired.scale_to_length(self.max_speed*(desired.length_squared()/self.arrival_radius_sq))
        steer = desired - self.velocity
        if steer.length_squared() > 0:
            steer.scale_to_length(min(steer.length(), self.max_acceleration))
        self.apply_force(weight*steer, dt)

    def avoid(self, pt, dt, weight=50):
        vec = pt - self.position
        if vec.length_squared() > 1:
            vec.scale_to_length(1000/vec.length())
        else:
            vec.scale_to_length(1000)
        self.apply_force(weight*vec.rotate(180), dt)
        pygame.draw.line(self.surface, (255, 0, 0), self.position,
                         self.position+weight*vec.rotate(180)*dt)

    def update(self, dt_ms, all_actors=None):
        dt = dt_ms / 1000.0
        self.acceleration.xy = 0, 0

        self.seek(Vector2(960, 540), dt, weight=50)
        if all_actors:
            for actor in all_actors:
                if actor is self:
                    continue
                self.avoid(actor.position, dt, weight=20)

        # self.limit_acceleration()
        self.apply_velocity(dt)

    def render(self, surface):
        self.transformed_pts = self.translate(
            self.rotate(self.local_pts(), self.velocity), self.position)
        pygame.draw.polygon(surface,
                            self.color,
                            [row for row in self.transformed_pts],
                            3)

    def animate(self, surface, dt_ms, all_actors):
        self.update(dt_ms, all_actors)
        self.render(surface)
