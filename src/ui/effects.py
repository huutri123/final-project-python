import math
import random

import pygame

from src.core.constants import GROUND_HEIGHT, HEIGHT, WIDTH


SKY_TOP = (21, 27, 57)
SKY_MID = (41, 91, 122)
SKY_BOTTOM = (246, 183, 112)
SUN = (255, 219, 128)
FAR_HILLS = (70, 91, 120)
MID_HILLS = (52, 136, 135)
NEAR_HILLS = (35, 96, 95)


def _lerp(a, b, t):
    return int(a + (b - a) * t)


def _mix(color_a, color_b, t):
    return tuple(_lerp(color_a[index], color_b[index], t) for index in range(3))


class Background:
    def __init__(self):
        self.__tick = 0
        self.__far_offset = 0
        self.__mid_offset = 0
        self.__near_offset = 0
        self.__gradient = pygame.Surface((WIDTH, HEIGHT))
        self.__stars = [
            (
                random.randint(30, WIDTH - 30),
                random.randint(28, 210),
                random.choice((1, 1, 2)),
                random.random() * math.tau,
            )
            for _ in range(46)
        ]
        self.__build_gradient()

    def __build_gradient(self):
        for y in range(HEIGHT):
            upper_t = min(1, y / (HEIGHT * 0.56))
            lower_t = max(0, (y - HEIGHT * 0.42) / (HEIGHT * 0.42))
            color = _mix(SKY_TOP, SKY_MID, upper_t)
            color = _mix(color, SKY_BOTTOM, lower_t * 0.62)
            pygame.draw.line(self.__gradient, color, (0, y), (WIDTH, y))

    def update(self, running):
        self.__tick += 1
        ambient_speed = 0.35
        speed = 1.0 if running else ambient_speed
        self.__far_offset = (self.__far_offset + speed * 0.28) % 340
        self.__mid_offset = (self.__mid_offset + speed * 0.56) % 300
        self.__near_offset = (self.__near_offset + speed * 0.9) % 260

    def __draw_sun(self, screen):
        sun_x = WIDTH - 178
        sun_y = 118 + int(math.sin(self.__tick * 0.012) * 5)
        glow = pygame.Surface((180, 180), pygame.SRCALPHA)
        for radius, alpha in ((82, 26), (58, 38), (36, 52)):
            pygame.draw.circle(glow, (*SUN, alpha), (90, 90), radius)
        screen.blit(glow, (sun_x - 90, sun_y - 90))
        pygame.draw.circle(screen, SUN, (sun_x, sun_y), 34)
        pygame.draw.circle(screen, (255, 247, 203), (sun_x - 8, sun_y - 10), 9)

    def __draw_stars(self, screen):
        for x, y, size, phase in self.__stars:
            pulse = (math.sin(self.__tick * 0.04 + phase) + 1) / 2
            color = _mix((131, 218, 234), (255, 247, 203), pulse)
            pygame.draw.circle(screen, color, (x, y), size)

    def __draw_hills(self, screen, base_y, height, step, offset, color):
        start = int(-step - offset)
        for x in range(start, WIDTH + step * 2, step):
            points = [
                (x, GROUND_HEIGHT + 18),
                (int(x + step * 0.18), base_y),
                (int(x + step * 0.5), base_y - height),
                (int(x + step * 0.82), base_y + 10),
                (x + step, GROUND_HEIGHT + 18),
            ]
            pygame.draw.polygon(screen, color, points)

    def draw(self, screen):
        screen.blit(self.__gradient, (0, 0))
        self.__draw_stars(screen)
        self.__draw_sun(screen)
        self.__draw_hills(screen, 410, 92, 340, self.__far_offset, FAR_HILLS)
        self.__draw_hills(screen, 432, 72, 300, self.__mid_offset, MID_HILLS)
        self.__draw_hills(screen, 456, 54, 260, self.__near_offset, NEAR_HILLS)


class Effects:
    def __init__(self):
        self.__particles = []

    def clear(self):
        self.__particles.clear()

    def __add_particle(self, x, y, vx, vy, radius, color, life, gravity=0.0):
        self.__particles.append(
            {
                "x": x,
                "y": y,
                "vx": vx,
                "vy": vy,
                "radius": radius,
                "color": color,
                "life": life,
                "max_life": life,
                "gravity": gravity,
            }
        )

    def spawn_jump(self, x, y):
        for _ in range(16):
            self.__add_particle(
                x + random.randint(-18, 10),
                y - random.randint(1, 7),
                random.uniform(-3.2, -0.6),
                random.uniform(-2.2, -0.2),
                random.randint(3, 7),
                random.choice(((255, 217, 132), (126, 220, 193), (91, 75, 104))),
                random.randint(18, 32),
                0.08,
            )

    def spawn_land(self, x, y):
        for side in (-1, 1):
            for _ in range(8):
                self.__add_particle(
                    x + random.randint(-8, 8),
                    y - 5,
                    random.uniform(1.4, 3.8) * side,
                    random.uniform(-1.6, -0.2),
                    random.randint(2, 6),
                    random.choice(((255, 247, 203), (118, 224, 206), (242, 164, 92))),
                    random.randint(16, 26),
                    0.1,
                )

    def spawn_crash(self, x, y):
        for _ in range(46):
            angle = random.random() * math.tau
            speed = random.uniform(2.2, 7.4)
            self.__add_particle(
                x,
                y,
                math.cos(angle) * speed,
                math.sin(angle) * speed - 1.5,
                random.randint(3, 8),
                random.choice(((238, 76, 83), (255, 247, 203), (95, 226, 178), (168, 86, 190))),
                random.randint(28, 54),
                0.16,
            )

    def spawn_milestone(self, x, y):
        for index in range(72):
            angle = math.tau * index / 72
            speed = random.uniform(2.1, 5.8)
            self.__add_particle(
                x,
                y,
                math.cos(angle) * speed,
                math.sin(angle) * speed,
                random.randint(3, 8),
                random.choice(((255, 247, 203), (131, 218, 234), (95, 226, 178), (238, 76, 83))),
                random.randint(34, 62),
                0.02,
            )
        for _ in range(28):
            self.__add_particle(
                x + random.randint(-120, 120),
                y + random.randint(-24, 24),
                random.uniform(-0.8, 0.8),
                random.uniform(-2.8, -0.6),
                random.randint(2, 5),
                random.choice(((255, 217, 132), (255, 247, 203), (126, 220, 193))),
                random.randint(26, 48),
                0.06,
            )

    def update(self):
        alive = []
        for particle in self.__particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += particle["gravity"]
            particle["life"] -= 1
            particle["radius"] *= 0.975
            if particle["life"] > 0 and particle["radius"] > 0.8:
                alive.append(particle)
        self.__particles = alive

    def draw(self, screen):
        for particle in self.__particles:
            radius = max(1, int(particle["radius"]))
            alpha = max(0, min(255, int(255 * particle["life"] / particle["max_life"])))
            dot = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(dot, (*particle["color"], alpha), (radius + 1, radius + 1), radius)
            screen.blit(dot, (particle["x"] - radius, particle["y"] - radius))
