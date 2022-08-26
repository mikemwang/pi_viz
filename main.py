import os
import pygame
from pygame.math import Vector2
import time
import timeit
import random
import numpy as np

from actor import Actor
from quadtree import Point, Rect, QuadTree


class PiViz:
    screen = None

    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"

        self.start_time = time.time()

        os.putenv('SDL_FBDEV', '/dev/fb0')

        # solves the ALSA lib error, apparently
        os.environ['SDL_AUDIODRIVER'] = 'dsp'

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

        for i in range(n_actors):
            actors.append(Actor(Vector2(random.uniform(0, 1920), random.uniform(0, 1080)),
                                Vector2(random.uniform(-1,1), random.uniform(-1,1)),
                                20, 
                                20, 
                                (255, 255, 255), 
                                200, 
                                200))

        running = True
        idx = 0
        while running:
            if idx > frames:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            dt = clock.tick()
            w, h = 2*self.w, 2*self.h
            tree = QuadTree(Rect(w/2, h/2, w, h))
            for actor in actors:
                tree.insert(Point(actor.position.x, actor.position.y, actor))

            self.screen.fill((0, 0, 0))
            for actor in actors:
                actor.animate(self.screen, 60, tree)

            pygame.display.flip()
            idx += 1


if __name__ == "__main__":
    viz = PiViz()
    frames = 1000
    n_actors = 10
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()
    viz.run(1000, 100)
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()
    #viz.run(frames, 100)
    #t = timeit.timeit(lambda: viz.run(frames, n_actors), number=1)
    #print(f"{n_actors} actors for {frames} frames in {t}s, {frames/t} fps")

    #for i in range(25):
    #    t = timeit.timeit(lambda: viz.run(frames, n_actors+i*10), number=1)
    #    #print(f"{n_actors} actors for {frames} frames in {t}s, {frames/t} fps")
    #    print(f"{n_actors+i*10},{1000/t}")
