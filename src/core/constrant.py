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
GRAVITY = 1
JUMP_VELOCITY = 17
GROUND_HEIGHT = WIDTH // 2.5

# Dino
# Note: Dino position and sprite-sheet frames.
DINO_WIDTH = 50
DINO_HEIGHT = 50
DINO_X = 250
DINO_DUCK1 = (2206, 34, 119, 60)
DINO_DUCK2 = (2324, 34, 119, 60)

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
# Note: Obstacle sizing and spawn timing values.
OBSTACLE_SPAWN_DELAY = 90  # frames
CACTUS_WIDTH = 30
CACTUS_HEIGHT = 50
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
# Note: Rectangles for the bird obstacle inside sprite_sheet.png.
BIRD_FRAME_1 = (260, 2, 92, 80)
BIRD_FRAME_2 = (352, 2, 92, 80)
# Note: Bird has two flight heights. The high one targets the dino head.
BIRD_LOW_Y = GROUND_HEIGHT - 55
BIRD_HIGH_Y = GROUND_HEIGHT - 120

# Path
# Note: Project root used to load assets and data files.
PATH = Path(__file__).parent.parent.parent

if __name__=="__main__":
    print(PATH)
