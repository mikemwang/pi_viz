import os
import pygame
import time


class Pyscope:
    screen = None

    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")

        if disp_no:
            print("I'm running under X display = {0}".format(disp_no))

        os.putenv('SDL_FBDEV', '/dev/fb0')
        pygame.init()

        size = (pygame.display.Info().current_w,
                pygame.display.Info().current_h)
        print("Framebuffer size: %d x %d" % (size[0], size[1]))
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def test(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        self.screen.fill(red)
        # Update the display
        pygame.display.update()


# Create an instance of the PyScope class
scope = Pyscope()
scope.test()
time.sleep(10)
