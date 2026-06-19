import json
from pathlib import Path

import pygame
from src.core.constants import PATH


DEFAULT_GAME_DATA = {
    "highscore": "00000",
    "sound_enabled": True,
}


class ImageUtils:
    """Shared image helpers."""

    @staticmethod
    def get_image(sheet, rect):
        """Cut one image from a sprite sheet."""
        # Note: Create a transparent surface with the requested sprite size.
        image = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), rect)
        return image

    @staticmethod
    def create_visible_pixel_mask(surface: pygame.Surface) -> pygame.mask.Mask:
        """Create a collision mask from visible, non-white pixels only.

        The source sprites use a white background. A normal rect collision sees that
        whole rectangle as solid, so the game can end before the dino visually touches
        a cactus. This mask keeps only the dark sprite pixels as the hit area.
        """
        # Note: Build a mask manually so white sprite backgrounds are ignored.
        mask = pygame.mask.Mask(surface.get_size())

        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                red, green, blue, alpha = surface.get_at((x, y))
                is_visible = alpha > 0
                is_background = red > 245 and green > 245 and blue > 245

                if is_visible and not is_background:
                    mask.set_at((x, y), 1)

        return mask

class Data:
    DATA_PATH = Path(PATH) / "data" / "game_data.json"
    LEGACY_HIGHSCORE_PATH = Path(PATH) / "data" / "highscore.json"

    @staticmethod
    def __read_json(path):
        try:
            with path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    @staticmethod
    def __normalize(data):
        normalized = DEFAULT_GAME_DATA.copy()
        if isinstance(data, dict):
            normalized.update(data)
        normalized["highscore"] = str(normalized.get("highscore", "00000")).zfill(5)
        normalized["sound_enabled"] = bool(normalized.get("sound_enabled", True))
        return normalized

    @staticmethod
    def GetData():
        # Note: Read game data, falling back to the old high score file.
        data = Data.__read_json(Data.DATA_PATH)
        if data is None:
            data = Data.__read_json(Data.LEGACY_HIGHSCORE_PATH)
        return Data.__normalize(data)

    @staticmethod
    def SaveData(data):
        # Note: Save merged game data back to the main JSON file.
        merged = Data.GetData()
        if isinstance(data, dict):
            merged.update(data)
        merged = Data.__normalize(merged)
        Data.DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        with Data.DATA_PATH.open("w", encoding="utf-8") as file:
            json.dump(merged, file, indent=2)
