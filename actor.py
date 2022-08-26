import math
import pygame
from pygame.math import Vector2, Vector3
import numpy as np
from lut import ROTATION_MATRIX


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
        self.velocity = velocity.normalize()
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

        self.detection_radius = 75

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
        #theta = math.atan2(vec.y, vec.x)
        #cos = math.cos(theta)
        #sin = math.sin(theta)
        theta = int(math.atan2(vec.y, vec.x)*180/math.pi)
        #cos = COS[theta]
        #sin = SIN[theta]
        #return np.array([[cos, -sin], [sin, cos]]).dot(pts.T).T
        return ROTATION_MATRIX[theta].dot(pts.T).T

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
        if desired.length_squared() < 0.0001:
            return
        if desired.length_squared() > self.arrival_radius_sq:
            desired.scale_to_length(self.max_speed)
        else:
            desired.scale_to_length(self.max_speed*(desired.length_squared()/self.arrival_radius_sq))
        steer = desired - self.velocity
        if steer.length_squared() > 0.0001:
            steer.scale_to_length(min(steer.length(), self.max_acceleration))
        self.apply_force(weight*steer, dt)

    def avoid(self, pt, dt, weight=1):
        vec = pt - self.position
        if vec.length_squared() > 1:
            vec.scale_to_length(1000/vec.length())
        else:
            vec.scale_to_length(1000)
        self.apply_force(weight*vec.rotate(180), dt)

    def update(self, dt_ms, all_actors):
        dt = dt_ms / 1000.0
        self.acceleration.xy = 0, 0
        dim = max(0.5*self.width, 0.5*self.length) 
        if self.position.x < -dim:
            self.position.x = 1920 + dim
        elif self.position.x > 1920 + dim:
            self.position.x = -dim

        if self.position.y < -dim:
            self.position.y = 1080 + dim
        elif self.position.y > 1080 + dim:
            self.position.y = -dim

        actors = []
        all_actors.query_radius(self.position, self.detection_radius, actors)
        #actors = [actor.payload for actor in actors]

        # seek centroid
        centroid = Vector2(0,0)
        n = 0

        # seek orientation
        dir = Vector2(0,0)

        for actor in actors:
            # calc centroid
            centroid += actor.position
            n += 1

            # calc direction
            try:
                dir += actor.velocity.normalize()
            except ValueError:
                pass
                
            # avoid colliding
            if (actor.position - self.position).length_squared() < 2500:
                if actor is self:
                    continue
                self.avoid(actor.position, dt, weight=20)

        # apply centroid
        if n > 0:
            centroid /= n
            self.seek(centroid, dt, weight=50)

        # apply orientation
        try:
            dir.scale_to_length(self.max_speed)
            steer = dir - self.velocity
            if steer.length_squared() > self.max_acceleration_squared:
                steer.scale_to_length(min(steer.length(), self.max_acceleration))
            self.apply_force(50*steer, dt) 
        except ValueError:
            pass

        # self.limit_acceleration()
        self.apply_velocity(dt)

    def render(self, surface):
        #self.transformed_pts = self.translate(
        #    self.rotate(self.local_pts(), self.velocity), self.position)
        #pygame.draw.polygon(surface,
        #                    self.color,
        #                    [row for row in self.transformed_pts],
        #                    3)

        pygame.draw.circle(surface, self.color, self.position, 6, 3)

        #rect = pygame.Rect(0, 0, 0, 0)
        #rect.x = self.position.x
        #rect.y = self.position.y
        #rect.w = self.width
        #rect.h = self.length
        #pygame.draw.rect(self.surface, self.color, rect, width=3)

    def animate(self, surface, dt_ms, all_actors):
        self.update(dt_ms, all_actors)
        self.render(surface)
