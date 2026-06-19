from pathlib import Path

# Screen
# Note: Window size and frame rate.
FPS = 60
WIDTH = 1200
HEIGHT = 720

# Colors
# Note: Shared colors used by drawing code.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)

# Game
# Note: Basic movement and jump physics.
GAME_SPEED = 10
# Score milestones increase the world speed in controlled steps.
SPEED_MILESTONES = (
    (100, 12),
    (200, 16),
    (300, 24),
    (400, 32),
    (500, 45),
)
GRAVITY = 1
JUMP_VELOCITY = 17
GROUND_HEIGHT = int(WIDTH / 2.5)

# Dino
# Note: Dino position and sprite-sheet frames.
DINO_WIDTH = 50
DINO_HEIGHT = 50
DINO_BASE_ANIMATION_SPEED = 0.2
DINO_X = 250
DINO_DUCK1 = (2206, 34, 119, 60)
DINO_DUCK2 = (2324, 34, 119, 60)
DINO_DUCK_FRAME_1 = DINO_DUCK1
DINO_DUCK_FRAME_2 = DINO_DUCK2

# UI sprites
# Note: Rectangle for the Game Over text inside sprite_sheet.png.
GAME_OVER_FRAME = (1294, 29, 381, 21)
# Note: Rectangle for the restart button inside sprite_sheet.png.
RESTART_BUTTON_FRAME = (151, 120, 61, 69)

# Background sprites
# Note: Rectangle for the cloud background inside sprite_sheet.png.
CLOUD_FRAME = (170, 2, 88, 27)
CLOUD_COUNT = 3
CLOUD_SPEED = 2
CLOUD_MIN_Y = 120
CLOUD_MAX_Y = 230

# Obstacles
# Note: Obstacle spawn spacing and size settings.
OBSTACLE_SPAWN_DELAY = 90  # frames
OBSTACLE_SPAWN_MARGIN = 100
# This minimum gap is based on the current jump arc and speed so the player has
# enough room to land or prepare the next jump before another cactus arrives.
OBSTACLE_MIN_GAP = 360
OBSTACLE_MAX_GAP = 620
# A random time window keeps spawning unpredictable without waiting for the
# previous obstacle to fully leave the screen.
OBSTACLE_MIN_SPAWN_FRAMES = 20
OBSTACLE_MAX_SPAWN_FRAMES = 75
OBSTACLE_RETRY_MIN_FRAMES = 5
OBSTACLE_RETRY_MAX_FRAMES = 15
CACTUS_WIDTH = 30
CACTUS_HEIGHT = 50
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
# Note: Rectangles for the bird obstacle inside sprite_sheet.png.
BIRD_FRAME_1 = (260, 2, 92, 80)
BIRD_FRAME_2 = (352, 2, 92, 80)
# Note: Bird has two flight heights. The high one targets the dino head.
BIRD_LOW_Y = GROUND_HEIGHT - 55
BIRD_HIGH_Y = GROUND_HEIGHT - 105

# Path
# Note: Project root used to load assets and data files.
ROOT_DIR = Path(__file__).resolve().parents[2]
PATH = ROOT_DIR
ASSET_DIR = ROOT_DIR / "asset"
IMAGE_DIR = ASSET_DIR / "Image"
FONT_DIR = ASSET_DIR / "font"
