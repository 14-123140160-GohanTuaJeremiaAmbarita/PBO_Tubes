import pygame
from settings import FENCE_WIDTH


def check_collision(px, py, ex, ey, er):
    distance_squared = (px - ex) ** 2 + (py - ey) ** 2
    return distance_squared <= er**2


def check_fence_collision(px, py, fx, fy, fheight, fwidth):
    return fx < px < fx + fwidth and fy < py < fy + fheight
