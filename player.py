import pygame
import utils
import math
from asteroid import Asteroid

class Player(object):
    def __init__(self, screensize):
        self.pos = [50, 50]
        self.size = 10
        self.velocity = [0, 0]
        self.level = 0
        self.screensize = screensize
        self.color = (0, 150, 0)
        # self.goal = [utils.randint_seeded(self.level, 0, screensize[0]),
        #              utils.randint_seeded(self.level, 0, screensize[1])]
        #
        # self.asteroids = []
        # for i in range(0, self.level + 5):
        #     apos = [utils.randint_seeded(self.level + 2 + i * 10, 0, screensize[0]),
        #             utils.randint_seeded(self.level + 1 + i * 11, 0, screensize[1])]
        #     self.asteroids.append(Asteroid(apos))
        self.goal = [0, 0]
        self.goalsize = 30
        self.asteroids = []
        self.levelling = -1
        self.levelup()

    def update_gameover(self, dt):
        self.size -= 1 * dt
        if self.size < 1:
            self.size = 1

        self.velocity[0] /= 1.01
        self.velocity[1] /= 1.01

        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

    def update(self, dt):
        if self.levelling < 0:
            SPEEDMOD = 5000
            if (pygame.key.get_pressed()[pygame.K_UP]):
                self.velocity[1] -= SPEEDMOD / self.size * dt
            if (pygame.key.get_pressed()[pygame.K_DOWN]):
                self.velocity[1] += SPEEDMOD / self.size * dt
            if (pygame.key.get_pressed()[pygame.K_LEFT]):
                self.velocity[0] -= SPEEDMOD / self.size * dt
            if (pygame.key.get_pressed()[pygame.K_RIGHT]):
                self.velocity[0] += SPEEDMOD / self.size * dt

        i = 0
        for asteroid in self.asteroids:
            dist = math.sqrt(math.pow(asteroid.pos[0] - self.pos[0], 2) + \
                             math.pow(asteroid.pos[1] - self.pos[1], 2))

            asteroid.update(dt, self)

            if dist < asteroid.size + self.size and self.levelling < 0:
                self.size = math.sqrt(math.pow(asteroid.size, 2) + math.pow(self.size, 2))
                del self.asteroids[i]
            i += 1

        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

        goaldist = math.sqrt(math.pow(self.goal[0] - self.pos[0], 2) + \
                             math.pow(self.goal[1] - self.pos[1], 2))

        self.color = (self.size * 2, 150, self.size * 2)

        if goaldist < 30 + self.size and self.levelling <= 0:
            self.levelup()

        if (pygame.time.get_ticks() - self.levelling) > 1400 and self.levelling > 0:
            self.generate_new_level()

        if (pygame.time.get_ticks() - self.levelling) > 1800 and self.levelling > 0:
            self.levelling = -1


    def levelup(self):
        self.level += 1

        if self.level != 1:
            self.levelling = pygame.time.get_ticks()
            self.velocity = [0, 0]
        else:
            self.generate_new_level()

    def generate_new_level(self):
        self.asteroids = []
        for i in range(0, self.level + 2):
            apos = [utils.randint_seeded(self.level + 2 + i * 10, 0, self.screensize[0]),
                    utils.randint_seeded(self.level + 1 + i * 11, 0, self.screensize[1])]
            self.asteroids.append(Asteroid(apos))

        self.goal = [utils.randint_seeded(self.level + 4, self.screensize[0] / 2, self.screensize[0] - 50),
                     utils.randint_seeded(self.level + 3, 50, self.screensize[1] - 50)]

        self.pos = [utils.randint_seeded(self.level + 5, 0, self.screensize[0] / 3), \
                    utils.randint_seeded(self.level + 6, 50, self.screensize[1] - 50)]

    def draw(self, screen, view, font):
        elapse_since_level = (pygame.time.get_ticks() - self.levelling)

        x = int(self.pos[0] + view[0])
        y = int(self.pos[1] + view[1])

        if self.levelling < 0:
            pygame.draw.circle(screen, self.color, (x, y), int(self.size))
        else:
            drawrad = self.size - elapse_since_level / 1000 * self.size
            if drawrad < 1:
                drawrad = 1
            pygame.draw.circle(screen, self.color, (x, y), int(drawrad))

        x = int(self.goal[0] + view[0])
        y = int(self.goal[1] + view[1])

        if self.levelling < 0:
            self.goalsize = 30 + int(math.sin(pygame.time.get_ticks() / 300) * 3)

        pygame.draw.circle(screen, (20, 240, 10, 50), (x, y), int(self.goalsize), 1)

        for asteroid in self.asteroids:
            asteroid.draw(screen, view)

        WAIT_TIME = 800
        if elapse_since_level >= WAIT_TIME and self.levelling > 0 and elapse_since_level < 2 * WAIT_TIME:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, \
                (elapse_since_level - WAIT_TIME) / 200 * self.screensize[0] / 2,\
                 self.screensize[1]))

            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.screensize[0], 0, \
                -(elapse_since_level - WAIT_TIME) / 200 * self.screensize[0] / 2,\
                 self.screensize[1]))

        leveltext = font.render("level " + str(self.level), 0, (20, 240, 10))
        screen.blit(leveltext, (10, 10))

        
