import math
import numpy as np

SIN = [math.sin(i) for i in range(0, 360)]
COS = [math.cos(i) for i in range(0, 360)]

ROTATION_MATRIX = [np.array([[math.cos(i*math.pi/180), -math.sin(i*math.pi/180)],
                             [math.sin(i*math.pi/180), math.cos(i*math.pi/180)]]) for i in range(0, 360)]

