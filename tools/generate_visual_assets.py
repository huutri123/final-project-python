from pathlib import Path
import random

import pygame


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "asset" / "Image"
FONT_PATH = ROOT / "asset" / "font" / "arcadeclassic.regular.ttf"


def make_surface(size):
    return pygame.Surface(size, pygame.SRCALPHA)


def draw_crystal(surface, points, fill, edge):
    pygame.draw.polygon(surface, edge, points)
    inset = []
    cx = sum(x for x, _ in points) / len(points)
    cy = sum(y for _, y in points) / len(points)
    for x, y in points:
        inset.append((int(cx + (x - cx) * 0.82), int(cy + (y - cy) * 0.82)))
    pygame.draw.polygon(surface, fill, inset)


def make_dino(frame=0, duck=False, blink=False):
    outline = (12, 52, 63)
    main = (43, 196, 151)
    shade = (21, 126, 122)
    belly = (255, 218, 93)
    crest = (255, 97, 111)
    eye_white = (248, 252, 255)

    if duck:
        surf = make_surface((119, 60))
        leg_shift = 5 if frame else 0
        pygame.draw.polygon(surf, outline, [(27, 42), (2, 32), (0, 25), (30, 28), (48, 41)])
        pygame.draw.polygon(surf, shade, [(28, 39), (6, 31), (28, 30), (47, 42)])
        pygame.draw.ellipse(surf, outline, (25, 17, 59, 33))
        pygame.draw.ellipse(surf, main, (28, 19, 53, 28))
        pygame.draw.ellipse(surf, belly, (39, 28, 30, 16))
        pygame.draw.rect(surf, outline, (72, 11, 36, 31), border_radius=12)
        pygame.draw.rect(surf, main, (75, 14, 31, 25), border_radius=10)
        pygame.draw.rect(surf, outline, (96, 21, 21, 13), border_radius=6)
        pygame.draw.rect(surf, main, (96, 22, 18, 10), border_radius=5)
        pygame.draw.line(surf, outline, (102, 34), (115, 34), 2)
        pygame.draw.circle(surf, eye_white, (96, 20), 4)
        if blink:
            pygame.draw.line(surf, outline, (92, 20), (100, 20), 2)
        else:
            pygame.draw.circle(surf, outline, (97, 20), 2)
        pygame.draw.polygon(surf, crest, [(72, 21), (89, 16), (85, 27), (71, 28)])
        for x, height in ((34, 11), (45, 13), (56, 10)):
            pygame.draw.polygon(surf, outline, [(x - 1, 20), (x + 4, 7), (x + 10, 21)])
            pygame.draw.polygon(surf, (112, 238, 186), [(x + 1, 20), (x + 4, 10), (x + 8, 20)])
        pygame.draw.rect(surf, outline, (40 + leg_shift, 43, 10, 15), border_radius=3)
        pygame.draw.rect(surf, shade, (42 + leg_shift, 43, 7, 12), border_radius=3)
        pygame.draw.rect(surf, outline, (62 - leg_shift, 42, 10, 16), border_radius=3)
        pygame.draw.rect(surf, shade, (64 - leg_shift, 42, 7, 13), border_radius=3)
        pygame.draw.rect(surf, outline, (35 + leg_shift, 55, 20, 5), border_radius=2)
        pygame.draw.rect(surf, outline, (59 - leg_shift, 55, 19, 5), border_radius=2)
        pygame.draw.line(surf, shade, (73, 34), (84, 39), 4)
        return surf

    surf = make_surface((88, 94))
    pygame.draw.polygon(surf, outline, [(28, 61), (4, 52), (0, 43), (28, 43), (45, 58)])
    pygame.draw.polygon(surf, shade, [(27, 58), (7, 50), (28, 46), (43, 59)])
    pygame.draw.ellipse(surf, outline, (20, 33, 49, 40))
    pygame.draw.ellipse(surf, main, (24, 36, 42, 33))
    pygame.draw.ellipse(surf, belly, (36, 47, 25, 19))
    pygame.draw.rect(surf, outline, (51, 18, 27, 39), border_radius=11)
    pygame.draw.rect(surf, main, (54, 21, 22, 32), border_radius=9)
    pygame.draw.rect(surf, outline, (63, 16, 23, 22), border_radius=8)
    pygame.draw.rect(surf, main, (65, 18, 19, 18), border_radius=7)
    pygame.draw.rect(surf, outline, (73, 28, 15, 11), border_radius=5)
    pygame.draw.rect(surf, main, (73, 29, 12, 8), border_radius=4)
    pygame.draw.circle(surf, eye_white, (73, 23), 4)
    if blink:
        pygame.draw.line(surf, outline, (69, 23), (77, 23), 2)
    else:
        pygame.draw.circle(surf, outline, (74, 23), 2)
    pygame.draw.line(surf, outline, (78, 38), (86, 38), 2)
    pygame.draw.polygon(surf, crest, [(52, 35), (69, 37), (62, 47), (50, 43)])
    pygame.draw.line(surf, shade, (53, 51), (66, 58), 4)

    for x, height in ((33, 11), (43, 14), (54, 11)):
        pygame.draw.polygon(surf, outline, [(x - 1, 38), (x + 4, 38 - height), (x + 10, 39)])
        pygame.draw.polygon(surf, (112, 238, 186), [(x + 1, 38), (x + 4, 40 - height), (x + 8, 38)])

    if frame == 0:
        legs = ((36, 68, 10, 20, -5), (57, 66, 10, 15, 5))
    else:
        legs = ((36, 66, 10, 15, -5), (57, 68, 10, 20, 5))
    for x, y, w, h, foot in legs:
        pygame.draw.rect(surf, outline, (x - 1, y - 1, w + 3, h + 3), border_radius=4)
        pygame.draw.rect(surf, shade, (x, y, w, h), border_radius=3)
        pygame.draw.rect(surf, outline, (x + min(0, foot), y + h - 1, 20, 6), border_radius=2)
    return surf


def make_cactus(kind):
    sizes = [(48, 100), (98, 100), (68, 70)]
    surf = make_surface(sizes[kind])
    w, h = surf.get_size()
    random.seed(12 + kind)
    stems = {
        0: [(24, 12, 13, 86), (13, 42, 11, 43), (33, 52, 10, 35)],
        1: [(34, 7, 14, 91), (58, 20, 13, 77), (17, 39, 12, 59), (76, 46, 10, 49)],
        2: [(31, 6, 13, 63), (17, 26, 10, 40), (43, 35, 10, 32)],
    }[kind]
    for x, y, sw, sh in stems:
        points = [(x + sw // 2, y), (x + sw, y + 11), (x + sw - 2, y + sh), (x + 2, y + sh), (x, y + 11)]
        draw_crystal(surf, points, (88, 222, 205), (25, 113, 134))
        pygame.draw.line(surf, (192, 249, 230), (x + sw // 2, y + 6), (x + sw // 2 - 2, y + sh - 8), 2)
        pygame.draw.line(surf, (168, 86, 190), (x + sw - 4, y + 17), (x + sw - 4, y + sh - 7), 2)
    pygame.draw.ellipse(surf, (83, 57, 104), (max(1, w // 2 - 20), h - 11, min(42, w - 2), 11))
    return surf


def make_bird(frame):
    surf = make_surface((92, 80))
    wing_color = (176, 70, 178)
    body_color = (245, 120, 133)
    edge = (79, 48, 108)
    if frame == 0:
        left_wing = [(42, 40), (7, 14), (28, 45)]
        right_wing = [(51, 40), (83, 15), (65, 47)]
    else:
        left_wing = [(42, 40), (10, 62), (30, 42)]
        right_wing = [(51, 40), (82, 62), (64, 43)]
    pygame.draw.polygon(surf, edge, left_wing)
    pygame.draw.polygon(surf, wing_color, [(int(x * 0.92 + 42 * 0.08), int(y * 0.92 + 40 * 0.08)) for x, y in left_wing])
    pygame.draw.polygon(surf, edge, right_wing)
    pygame.draw.polygon(surf, wing_color, [(int(x * 0.92 + 51 * 0.08), int(y * 0.92 + 40 * 0.08)) for x, y in right_wing])
    pygame.draw.ellipse(surf, body_color, (35, 31, 27, 19))
    pygame.draw.circle(surf, body_color, (62, 34), 9)
    pygame.draw.polygon(surf, (250, 210, 91), [(70, 34), (86, 29), (73, 41)])
    pygame.draw.circle(surf, (246, 250, 255), (64, 31), 3)
    pygame.draw.circle(surf, (25, 28, 58), (65, 31), 1)
    pygame.draw.line(surf, edge, (39, 52), (35, 58), 2)
    pygame.draw.line(surf, edge, (52, 52), (58, 59), 2)
    return surf


def make_ground():
    surf = make_surface((2400, 240))
    random.seed(7)
    pygame.draw.rect(surf, (73, 57, 79), (0, 22, 2400, 218))
    pygame.draw.rect(surf, (76, 193, 141), (0, 0, 2400, 16))
    pygame.draw.rect(surf, (36, 125, 113), (0, 16, 2400, 9))
    for x in range(0, 2400, 37):
        color = random.choice([(92, 210, 154), (246, 211, 105), (102, 224, 206)])
        pygame.draw.line(surf, color, (x, 0), (x + random.randint(6, 18), 0), 3)
    for x in range(0, 2400, 18):
        y = random.randint(35, 220)
        color = random.choice([(92, 66, 104), (59, 48, 72), (112, 83, 121), (242, 164, 92)])
        pygame.draw.rect(surf, color, (x, y, random.randint(4, 18), random.randint(2, 5)), border_radius=2)
    for x in range(0, 2400, 170):
        pygame.draw.polygon(surf, (58, 45, 70), [(x, 72), (x + 85, 35), (x + 170, 74), (x + 170, 126), (x, 126)])
    return surf


def make_cloud():
    surf = make_surface((88, 27))
    pygame.draw.ellipse(surf, (237, 251, 255), (0, 10, 35, 13))
    pygame.draw.ellipse(surf, (237, 251, 255), (17, 3, 38, 21))
    pygame.draw.ellipse(surf, (237, 251, 255), (48, 9, 36, 14))
    pygame.draw.line(surf, (131, 218, 234), (9, 22), (78, 22), 2)
    return surf


def make_restart_button():
    surf = make_surface((61, 69))
    pygame.draw.ellipse(surf, (19, 37, 63, 80), (5, 8, 51, 55))
    pygame.draw.ellipse(surf, (255, 247, 203), (3, 4, 52, 52))
    pygame.draw.ellipse(surf, (238, 76, 83), (10, 11, 38, 38))
    pygame.draw.arc(surf, (255, 247, 203), (18, 19, 24, 24), 0.7, 5.3, 4)
    pygame.draw.polygon(surf, (255, 247, 203), [(36, 14), (47, 18), (39, 26)])
    return surf


def draw_centered_text(surface, text, rect, size, color):
    font = pygame.font.Font(str(FONT_PATH), size)
    rendered = font.render(text, True, color)
    target = rendered.get_rect(center=pygame.Rect(rect).center)
    surface.blit(rendered, target)


def make_sprite_sheet():
    sheet = make_surface((2446, 194))
    sheet.blit(make_cloud(), (170, 2))
    sheet.blit(make_bird(0), (260, 2))
    sheet.blit(make_bird(1), (352, 2))
    draw_centered_text(sheet, "GAME OVER", (1294, 29, 381, 21), 28, (33, 37, 61))
    sheet.blit(make_restart_button(), (151, 120))
    sheet.blit(make_dino(0, duck=True), (2206, 34))
    sheet.blit(make_dino(1, duck=True, blink=True), (2324, 34))
    return sheet


def main():
    pygame.init()
    pygame.font.init()
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    pygame.image.save(make_dino(0), IMAGE_DIR / "dino_run1.png")
    pygame.image.save(make_dino(1), IMAGE_DIR / "dino_run2.png")
    pygame.image.save(make_dino(0), IMAGE_DIR / "standing_still.png")
    pygame.image.save(make_dino(0, blink=True), IMAGE_DIR / "standing_still_eye_closed.png")
    for index in range(3):
        pygame.image.save(make_cactus(index), IMAGE_DIR / f"cactus_{index + 1}.png")
    pygame.image.save(make_ground(), IMAGE_DIR / "ground.png")
    pygame.image.save(make_sprite_sheet(), IMAGE_DIR / "sprite_sheet.png")


if __name__ == "__main__":
    main()
