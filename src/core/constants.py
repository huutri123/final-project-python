"""Game-wide constants and asset paths."""
from pathlib import Path

# Screen
# Note: Window size and target frame rate.
FPS = 60
WIDTH = 1200
HEIGHT = 720

# Colors
# Note: Shared colors for rendering.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)

# Game physics
# Note: Movement speed, jump physics, and ground placement.
GAME_SPEED = 10
# Score milestones increase the world speed in controlled steps.
SPEED_MILESTONES = (
    (500, 12),
    (1000, 14),
    (1500, 16),
)
GRAVITY = 1
JUMP_VELOCITY = 17
GROUND_HEIGHT = int(WIDTH / 2.5)

# Dino
# Note: Dino animation and sprite-sheet frame positions.
DINO_BASE_ANIMATION_SPEED = 0.2

DINO_X = 250
DINO_DUCK_FRAME_1 = (2206, 34, 119, 60)
DINO_DUCK_FRAME_2 = (2324, 34, 119, 60)

# Obstacles
# Note: Obstacle spawn spacing and size settings.
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

# Paths
# Note: Asset folders resolved from the project root.
ROOT_DIR = Path(__file__).resolve().parents[2]
ASSET_DIR = ROOT_DIR / "asset"
IMAGE_DIR = ASSET_DIR / "Image"
FONT_DIR = ASSET_DIR / "font"

if __name__=="__main__":
    print()
