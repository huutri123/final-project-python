from src.entities.dino import Dino
from src.entities.obstacle import Obstacle


class Collision:
    @classmethod
    def collision_check(cls, dino: Dino, obstacle: Obstacle) -> bool:
        """Return True only when visible dino pixels touch visible obstacle pixels."""
        # Note: Get the current hit boxes from the dino and obstacle.
        dino_rect = dino.collision_rect
        obstacle_rect = obstacle.collision_rect

        # Quick reject: if the sprite rectangles do not overlap, masks cannot touch.
        if not dino_rect.colliderect(obstacle_rect):
            return False

        # Note: Offset tells pygame how the two masks are positioned relative to each other.
        offset = (
            obstacle_rect.x - dino_rect.x,
            obstacle_rect.y - dino_rect.y,
        )
        return dino.collision_mask.overlap(obstacle.collision_mask, offset) is not None
