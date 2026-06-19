import pygame

from src.core.constants import (
    FPS,
    GAME_SPEED,
    HEIGHT,
    PATH,
    RESTART_BUTTON_FRAME,
    SPEED_MILESTONES,
    WIDTH,
)
from src.entities.dino import Dino
from src.entities.cloud import Cloud
from src.entities.ground import Ground
from src.entities.obstacle import Obstacle
from src.managers.collision import Collision
from src.managers.font import Font
from src.managers.sound import SoundManager
from src.ui.effects import Background, Effects
from src.ui.hud import Hud
from src.utils.helpers import ImageUtils


JUMP_KEYS = (pygame.K_SPACE, pygame.K_UP)
START_KEYS = JUMP_KEYS + (pygame.K_RETURN,)
MILESTONE_INTERVAL = 100
TITLE_COLOR = (255, 247, 203)
ACCENT = (238, 76, 83)
CYAN = (131, 218, 234)
PANEL = (17, 30, 53, 218)


class Game:
    def __init__(self):
        # Note: Set up the window, clock, and main game state.
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__scene_surface = pygame.Surface((WIDTH, HEIGHT)).convert()
        self.__clock = pygame.Clock()
        pygame.display.set_caption("Dino Dash")

        self.__running = True
        self.__game_started = False
        self.__game_over = False
        self.__menu_tick = 0
        self.__game_over_tick = 0
        self.__shake_frames = 0
        self.__screen_flash = 0
        self.__fonts = {}
        self.__next_milestone = MILESTONE_INTERVAL
        self.__milestone_banner_score = 0
        self.__milestone_banner_timer = 0

        # Note: Create the main game objects.
        self.__background = Background()
        self.__effects = Effects()
        self.__cloud = Cloud()
        self.__ground = Ground()
        self.__dino = Dino()
        self.__obstacle = Obstacle()
        self.__hud = Hud()
        self.__sound = SoundManager()

        # Note: Cut the restart icon from the shared sprite sheet.
        sheet = pygame.image.load(str(PATH) + "/asset/Image/sprite_sheet.png")
        self.__restart_button_image = ImageUtils.get_image(sheet, RESTART_BUTTON_FRAME)
        self.__restart_icon = pygame.transform.smoothscale(
            self.__restart_button_image, (40, 44)
        )
        self.__start_button_rect = pygame.Rect(0, 0, 290, 66)
        self.__start_button_rect.center = (WIDTH // 2, HEIGHT // 2 + 156)
        self.__restart_button_rect = pygame.Rect(0, 0, 300, 66)
        self.__restart_button_rect.center = (WIDTH // 2, HEIGHT // 2 + 138)

    def __font(self, size):
        if size not in self.__fonts:
            self.__fonts[size] = Font(size).textFont
        return self.__fonts[size]

    def __draw_text(self, screen, text, size, color, center, shadow=True):
        font = self.__font(size)
        if shadow:
            shadow_text = font.render(text, True, (13, 24, 44))
            screen.blit(shadow_text, shadow_text.get_rect(center=(center[0] + 3, center[1] + 4)))
        rendered = font.render(text, True, color)
        screen.blit(rendered, rendered.get_rect(center=center))

    def __draw_button(self, screen, rect, text, icon=None):
        hovered = rect.collidepoint(pygame.mouse.get_pos())
        button_rect = rect.move(0, -3 if hovered else 0)
        shadow_rect = rect.move(0, 8)
        fill = (255, 108, 116) if hovered else ACCENT
        pygame.draw.rect(screen, (11, 19, 36), shadow_rect, border_radius=18)
        pygame.draw.rect(screen, fill, button_rect, border_radius=18)
        pygame.draw.rect(screen, (255, 247, 203), button_rect, 3, border_radius=18)

        font = self.__font(34)
        rendered = font.render(text, True, (255, 247, 203))
        text_rect = rendered.get_rect(center=button_rect.center)
        if icon:
            icon_rect = icon.get_rect(midleft=(button_rect.left + 30, button_rect.centery))
            screen.blit(icon, icon_rect)
            text_rect.centerx += 24
        screen.blit(rendered, text_rect)

    def __draw_overlay(self, screen, alpha):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((7, 12, 26, alpha))
        screen.blit(overlay, (0, 0))

    def __start_game(self):
        """Start the first run from a jump key press."""
        self.__game_started = True
        self.__sound.play("start")
        self.__try_jump()

    def __try_jump(self):
        if self.__dino.jump():
            self.__effects.spawn_jump(*self.__dino.feet_position)
            self.__sound.play("jump")

    def __restart_game(self):
        """Start a fresh run from a mouse click."""
        # Note: Reset every object that changes during a run.
        self.__game_started = True
        self.__game_over = False
        self.__game_over_tick = 0
        self.__shake_frames = 0
        self.__screen_flash = 0
        self.__next_milestone = MILESTONE_INTERVAL
        self.__milestone_banner_score = 0
        self.__milestone_banner_timer = 0
        self.__effects.clear()
        self.__cloud.reset()
        self.__ground.reset()
        self.__dino.reset()
        self.__obstacle.reset()
        self.__hud.reset_score()
        self.__sound.play("restart")

    def __current_game_speed(self):
        speed = GAME_SPEED
        score = int(self.__hud.score)
        for milestone_score, milestone_speed in sorted(SPEED_MILESTONES):
            if score < milestone_score:
                break
            speed = milestone_speed
        return speed

    def __handle_events(self):
        # Note: Handle quit, restart, and player input.
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.WINDOWCLOSE):
                self.__running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if (
                    not self.__game_started
                    and not self.__game_over
                    and self.__start_button_rect.collidepoint(event.pos)
                ):
                    self.__start_game()
                elif self.__game_over and self.__restart_button_rect.collidepoint(event.pos):
                    self.__restart_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.__sound.toggle()
                elif not self.__game_started and not self.__game_over and event.key in START_KEYS:
                    self.__start_game()
                elif self.__game_started and not self.__game_over and event.key in JUMP_KEYS:
                    self.__try_jump()

        if not self.__running:
            return

        keys = pygame.key.get_pressed()

        self.__dino.duck(
            keys[pygame.K_DOWN] and self.__game_started and not self.__game_over
        )

        # Holding SPACE now keeps jumping. Dino.jump() itself only starts a jump
        # when Dino is on the ground, so this does not create mid-air double jumps.
        if (
            self.__game_started
            and not self.__game_over
            and (keys[pygame.K_SPACE] or keys[pygame.K_UP])
        ):
            self.__try_jump()

    def __update(self):
        self.__menu_tick += 1
        self.__background.update(self.__game_started and not self.__game_over)
        self.__effects.update()

        if self.__shake_frames > 0:
            self.__shake_frames -= 1
        if self.__screen_flash > 0:
            self.__screen_flash -= 1
        if self.__milestone_banner_timer > 0:
            self.__milestone_banner_timer -= 1
        if self.__game_over:
            self.__game_over_tick += 1
            return

        # Note: Stop game movement while the Game Over screen is visible.
        if not self.__game_started:
            return

        # Note: Update moving objects and score while the game is running.
        game_speed = self.__current_game_speed()
        self.__cloud.update()
        self.__ground.update(game_speed)
        was_jumping = self.__dino.is_jumping
        self.__dino.update()
        if was_jumping and not self.__dino.is_jumping:
            self.__effects.spawn_land(*self.__dino.feet_position)
            self.__sound.play("land")
        self.__obstacle.update(game_speed)
        self.__hud.update()
        self.__check_score_milestone()

        # Note: A collision ends the current run and saves the high score.
        if Collision.collision_check(self.__dino, self.__obstacle):
            self.__game_over = True
            self.__game_over_tick = 0
            self.__shake_frames = 18
            self.__screen_flash = 16
            self.__hud.set_highest_score()
            self.__dino.duck(False)
            self.__effects.spawn_crash(*self.__dino.center_position)
            self.__sound.play("crash")

    def __check_score_milestone(self):
        score = int(self.__hud.score)
        if score < self.__next_milestone:
            return

        reached = self.__next_milestone
        while score >= self.__next_milestone:
            self.__next_milestone += MILESTONE_INTERVAL

        self.__milestone_banner_score = reached
        self.__milestone_banner_timer = 95
        self.__screen_flash = max(self.__screen_flash, 10)
        self.__effects.spawn_milestone(WIDTH // 2, HEIGHT // 2 - 90)
        self.__sound.play("milestone")

    def __draw_world(self, screen):
        self.__background.draw(screen)
        self.__cloud.draw(screen)
        self.__ground.draw(screen)
        self.__dino.draw(screen)
        self.__obstacle.draw(screen)
        self.__effects.draw(screen)
        self.__hud.draw(screen)

    def __draw_start_menu(self, screen):
        self.__draw_overlay(screen, 62)
        bob = int(pygame.math.Vector2(0, 1).rotate(self.__menu_tick * 2.2).y * 6)
        self.__draw_text(screen, "DINO DASH", 84, TITLE_COLOR, (WIDTH // 2, 196 + bob))
        self.__draw_text(screen, "CRYSTAL RUN", 34, CYAN, (WIDTH // 2, 266 + bob), False)
        self.__draw_text(
            screen,
            "BEST  " + self.__hud.highest_score,
            28,
            (255, 247, 203),
            (WIDTH // 2, HEIGHT // 2 + 34),
            False,
        )
        sound_text = "SOUND ON" if self.__sound.enabled else "SOUND OFF"
        self.__draw_text(
            screen,
            sound_text,
            22,
            CYAN,
            (WIDTH // 2, HEIGHT // 2 + 72),
            False,
        )
        self.__draw_button(screen, self.__start_button_rect, "START RUN")

    def __draw_milestone_banner(self, screen):
        if self.__milestone_banner_timer <= 0:
            return

        alpha = min(230, self.__milestone_banner_timer * 5)
        lift = max(0, 18 - self.__milestone_banner_timer // 5)
        banner = pygame.Surface((390, 86), pygame.SRCALPHA)
        pygame.draw.rect(banner, (17, 30, 53, alpha), banner.get_rect(), border_radius=20)
        pygame.draw.rect(banner, (131, 218, 234, min(210, alpha)), banner.get_rect(), 3, border_radius=20)
        screen.blit(banner, (WIDTH // 2 - 195, 108 - lift))
        self.__draw_text(
            screen,
            "MILESTONE",
            26,
            CYAN,
            (WIDTH // 2, 132 - lift),
            False,
        )
        self.__draw_text(
            screen,
            str(self.__milestone_banner_score).zfill(5),
            38,
            TITLE_COLOR,
            (WIDTH // 2, 168 - lift),
        )

    def __draw_game_over_menu(self, screen):
        self.__draw_overlay(screen, min(168, 88 + self.__game_over_tick * 4))
        panel_rect = pygame.Rect(0, 0, 540, 330)
        panel_rect.center = (WIDTH // 2, HEIGHT // 2 + 10)
        panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(panel, PANEL, panel.get_rect(), border_radius=22)
        pygame.draw.rect(panel, (255, 247, 203, 110), panel.get_rect(), 3, border_radius=22)
        screen.blit(panel, panel_rect)

        self.__draw_text(screen, "GAME OVER", 68, TITLE_COLOR, (WIDTH // 2, panel_rect.top + 72))
        self.__draw_text(
            screen,
            "SCORE  " + self.__hud.score,
            32,
            CYAN,
            (WIDTH // 2, panel_rect.top + 146),
            False,
        )
        self.__draw_text(
            screen,
            "BEST   " + self.__hud.highest_score,
            32,
            (255, 247, 203),
            (WIDTH // 2, panel_rect.top + 194),
            False,
        )
        sound_text = "SOUND ON" if self.__sound.enabled else "SOUND OFF"
        self.__draw_text(
            screen,
            sound_text,
            20,
            CYAN,
            (WIDTH // 2, panel_rect.top + 236),
            False,
        )
        self.__draw_button(screen, self.__restart_button_rect, "PLAY AGAIN", self.__restart_icon)

    def __shake_offset(self):
        if self.__shake_frames <= 0:
            return 0, 0
        strength = max(1, self.__shake_frames // 3)
        return (
            pygame.time.get_ticks() % (strength * 2 + 1) - strength,
            (pygame.time.get_ticks() // 3) % (strength * 2 + 1) - strength,
        )

    def __draw(self):
        # Note: Draw the current frame from background to foreground.
        self.__draw_world(self.__scene_surface)
        self.__screen.fill((7, 12, 26))
        self.__screen.blit(self.__scene_surface, self.__shake_offset())

        if not self.__game_started and not self.__game_over:
            self.__draw_start_menu(self.__screen)
        if self.__game_started and not self.__game_over:
            self.__draw_milestone_banner(self.__screen)
        if self.__game_over:
            self.__draw_game_over_menu(self.__screen)
        if self.__screen_flash > 0:
            flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash.fill((238, 76, 83, min(130, self.__screen_flash * 8)))
            self.__screen.blit(flash, (0, 0))

    def run(self):
        # Note: Main loop runs until the player closes the window.
        while self.__running:
            self.__handle_events()
            if not self.__running:
                break
            self.__update()
            self.__draw()
            self.__clock.tick(FPS)
            pygame.display.flip()
