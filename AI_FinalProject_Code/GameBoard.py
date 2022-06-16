from enum import IntEnum
import pygame
from pygame.locals import *


class MAP_ENTRY_TYPE(IntEnum):
    MAP_EMPTY = 0,
    MAP_PLAYER_ONE = 1,
    MAP_PLAYER_TWO = 2,
    MAP_NONE = 3,  # out of map range


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]
        self.steps = []

    def click(self, x, y, type):
        self.map[y][x] = type.value
        self.steps.append((x, y))