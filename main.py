import os
import pygame
from pygame.math import Vector2
import time
import timeit
import random


class Actor:

    def __init__(self, pos: Vector2, vel: Vector2, radius, color):
        self.pos = pos
        self.vel = vel
        self.r = radius
        self.color = color
        self.last_x = None
        self.last_y = None

    def clear(self, surface, bg=(0, 0, 0)):
        if self.last_x is None:
            return None

        return pygame.draw.circle(surface, bg, (self.last_x, self.last_y),
                                  self.r)

    def render(self, dt, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.r)
        self.last_x = self.x
        self.last_y = self.y
        self.x += self.v_x * dt / 1000.0
        self.y += self.v_y * dt / 1000.0


class PiViz:
    screen = None

    def __init__(self, fps):
        "Ininitializes a new pygame screen using the framebuffer"

        self.fps = fps
        self.start_time = time.time()

        os.putenv('SDL_FBDEV', '/dev/fb0')

        try:
            pygame.init()
        except pygame.error:
            print("failed to init pygame")

        size = (pygame.display.Info().current_w,
                pygame.display.Info().current_h)
        self.w, self.h = size[0], size[1]
        print("Framebuffer size: %d x %d" % (size[0], size[1]))
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def elapsed_time(self):
        return time.time() - self.start_time

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def run(self, frames, n_actors):
        x, y = self.w/2, self.h/2

        actors = []

        clock = pygame.time.Clock()

        for _ in range(n_actors):
            actors.append(Actor(x + random.random()*10,
                                y + random.random()*10,
                                random.uniform(-50, 50),
                                random.uniform(-50, 50),
                                25,
                                (random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255)
                                 )))
        i = 0

        while i < frames:
            dt = clock.tick()
            x += 1
            i += 1

            # for actor in actors:
            #    rects.append(actor.clear(self.screen))

            self.screen.fill((0, 0, 0))

            for actor in actors:
                actor.render(dt, self.screen)

            # pygame.display.update(rects)
            pygame.display.flip()


if __name__ == "__main__":
    viz = PiViz(30)
    frames = 1000
    n_actors = 200
    t = timeit.timeit(lambda: viz.run(frames, n_actors), number=1)
    print(f"{n_actors} actors for {frames} frames in {t}s, {frames/t} fps")
