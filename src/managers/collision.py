from src.entities.dino import Dino
from src.entities.obstacle import Obstacle


class Collision:
    @classmethod
    def collision_check(cls, dino: Dino, obstacle: Obstacle) -> bool:
        """Return True when the dino touches the current obstacle."""
        return dino.collision_rect.colliderect(obstacle.collision_rect)
