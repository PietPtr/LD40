import random
import pygame
import math

class Asteroid(object):
    def __init__(self, pos):
        self.pos = pos
        gray = random.randint(50, 200)
        self.color = (gray, gray, gray)
        self.size = random.randint(5, 15)
        self.velocity = [0, 0]


    def update(self, dt, player):
        dist = math.sqrt(math.pow(self.pos[0] - player.pos[0], 2) + \
                         math.pow(self.pos[1] - player.pos[1], 2))

        unit = [0, 0]
        unit[0] = (player.pos[0] - self.pos[0]) / dist
        unit[1] = (player.pos[1] - self.pos[1]) / dist

        G = 100
        force = [0, 0]
        force[0] = G * ((player.size * self.size) / dist) * unit[0]
        force[1] = G * ((player.size * self.size) / dist) * unit[1]

        self.velocity[0] += force[0] * dt
        self.velocity[1] += force[1] * dt

        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

    def draw(self, screen, view):
        x = int(self.pos[0] + view[0])
        y = int(self.pos[1] + view[1])

        pygame.draw.circle(screen, self.color, (x, y), self.size)
