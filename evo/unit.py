import random
import math
import pygame

FULL_WINDOW = 1920, 1080
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
YELLANGE = (255, 192, 0)
ORANGE = (255, 128, 0)
DARK_BLUE = (0, 0, 128)
BLUE = (0, 0, 225)
LIGHT_BLUE = (135, 208, 250)
RED = (255, 0, 0)
DARK_RED = (128, 0, 0)
GREEN = (64, 255, 64)
LIGHT_GREEN = (128, 255, 128)
BLACK = (0, 0, 0)
BROWN = (96, 38, 0)
GREY = (128, 128, 128)
PURPLE = (128, 0, 128)
PINK = (255, 20, 147)
PEACH = (240, 128, 128)
RASPBERRY = (220, 20, 60)
TURQUOISE = (0, 128, 128)
COLORS = [TURQUOISE, PINK, PEACH, RASPBERRY, PURPLE, YELLOW, YELLANGE, ORANGE, DARK_BLUE, BLUE, LIGHT_BLUE, RED, DARK_RED, GREEN, LIGHT_GREEN, BROWN, GREY]


def chance(a, b=100):
    return random.randint(1, b) <= a


def qrange(a, b):
    return math.sqrt((b.cords[0]-a.cords[0])**2+(b.cords[1]-a.cords[1])**2)


class Unit:
    def __init__(self, r=128, g=128, b=128, speed=3, size=10, cords=None, life=600, rad=100):
        self.r = r
        self.g = g
        self.b = b
        self.speed = speed
        self.size = size
        self.ang = random.randint(0, 314)/50
        if cords is None:
            self.cords = random.randint(0, FULL_WINDOW[0]-1), random.randint(0, FULL_WINDOW[1]-1)
        else:
            self.cords = cords
        self.life = life
        self.foods = 0
        self.rad = rad

    def color(self):
        return self.r, self.g, self.b

    def find(self, food):
        for f in food:
            r = qrange(self, f)
            if r < self.rad:
                if r < self.size:
                    food.remove(f)
                    self.life += 300
                    self.foods += 1
                else:
                    vec = f.cords[0]-self.cords[0], f.cords[1]-self.cords[1]
                    vec = vec[0]/r, vec[1]/r
                    ang = math.asin(-vec[1])
                    ang = math.pi - ang if vec[0] < 0 else ang
                    self.ang = -ang
                    break

    def move(self):
        if self.cords[0] < 0 or self.cords[0] >= FULL_WINDOW[0]:
            self.ang = math.pi - self.ang
        if self.cords[1] < 0 or self.cords[1] >= FULL_WINDOW[1]:
            self.ang = math.pi + self.ang
        self.cords = self.cords[0] + math.cos(self.ang)*self.speed, self.cords[1] + math.sin(self.ang)*self.speed

    def live(self, units):
        self.life -= 1
        if self.foods >= 2:
            self.foods -= 2

            units.append(self.clone())
        if self.life <= 0:
            units.remove(self)

    def clone(self):
        a, b, c = self.color()
        speed = self.speed
        size = self.size
        life = self.life
        rad = self.rad
        if chance(50):
            a = a+20 if chance(50) else a-20
            a = min(255, max(0, a))
        if chance(50):
            b = b+20 if chance(50) else b-20
            b = min(255, max(0, b))
        if chance(50):
            c = c+20 if chance(50) else c-20
            c = min(255, max(0, c))
        if chance(30):
            speed = speed + 1 if chance(50) else speed - 1
            speed = min(25, max(1, speed))
        if chance(30):
            size = size + 1 if chance(50) else size - 1
            size = min(25, max(1, size))
        if chance(30):
            life = life + 100 if chance(50) else life - 100
            a = max(0, a)
        if chance(30):
            rad = rad + 10 if chance(50) else rad - 10
            a = max(size, a)
        return Unit(cords=self.cords, r=a, g=b, b=c, speed=speed, size=size, life=life, rad=rad)

    def blit(self, sc):
        pygame.draw.circle(sc, self.color(), self.cords, self.size)
        pygame.draw.circle(sc, (0,0,0), self.cords, self.size+2, 2)


class Food:
    def __init__(self):
        self.color = random.choice(COLORS)
        self.cords = random.randint(0, FULL_WINDOW[0]-1), random.randint(0, FULL_WINDOW[1]-1)

    def blit(self, sc):
        pygame.draw.circle(sc, self.color, self.cords, 5)