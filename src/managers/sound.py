from pathlib import Path

import pygame

from src.core.constants import PATH
from src.utils.helpers import Data


class SoundManager:
    def __init__(self):
        data = Data.GetData() or {}
        self.__enabled = bool(data.get("sound_enabled", True))
        self.__available = self.__init_mixer()
        self.__sounds = {}
        if self.__available:
            self.__load_sounds()

    def __init_mixer(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except pygame.error:
            return False
        return True

    def __load_sounds(self):
        sound_dir = Path(PATH) / "asset" / "Sound"
        files = {
            "jump": "jump.wav",
            "land": "land.wav",
            "crash": "crash.wav",
            "start": "start.wav",
            "restart": "restart.wav",
            "toggle": "toggle.wav",
            "milestone": "milestone.wav",
        }
        for name, filename in files.items():
            path = sound_dir / filename
            if path.exists():
                self.__sounds[name] = pygame.mixer.Sound(str(path))

        volumes = {
            "jump": 0.42,
            "land": 0.32,
            "crash": 0.48,
            "start": 0.44,
            "restart": 0.42,
            "toggle": 0.28,
            "milestone": 0.46,
        }
        for name, volume in volumes.items():
            if name in self.__sounds:
                self.__sounds[name].set_volume(volume)

    @property
    def enabled(self):
        return self.__enabled and self.__available

    def play(self, name):
        if not self.enabled:
            return
        sound = self.__sounds.get(name)
        if sound:
            sound.play()

    def toggle(self):
        if not self.__available:
            return False
        self.__enabled = not self.__enabled
        if self.__enabled:
            self.play("toggle")
        else:
            pygame.mixer.stop()
        Data.SaveData({"sound_enabled": self.__enabled})
        return self.__enabled
