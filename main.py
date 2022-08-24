import os
import pygame
from pygame.math import Vector2
import time
import timeit
import random
import numpy as np

from actor import Actor


class PiViz:
    screen = None

    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"

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
        actors = []

        clock = pygame.time.Clock()
        actors = []

        for _ in range(10):
            actors.append(Actor(self.screen, Vector2(1920*random.random(), 1080*random.random()),
                                20, 20, (255, 255, 255), 100))

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            dt = clock.tick()

            self.screen.fill((0, 0, 0))

            for actor in actors:
                actor.animate(self.screen, dt, actors)

            pygame.display.flip()


if __name__ == "__main__":
    viz = PiViz()
    frames = 1000
    n_actors = 200
    t = timeit.timeit(lambda: viz.run(frames, n_actors), number=1)
    print(f"{n_actors} actors for {frames} frames in {t}s, {frames/t} fps")
