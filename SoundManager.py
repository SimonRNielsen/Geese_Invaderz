import pygame
from Enums import Music, SFX

class SoundManager:

    def __init__(self):
        pygame.mixer.init()
        self._current_music = None
        self._sfx = {}
        self.load_sfxs()
        self.play_music(Music.MENU)
        self._footsteps = pygame.mixer.Channel(1)
        self._last_footstep = None
            
    def load_sfxs(self):
        for i in SFX:
            self._sfx[i] = pygame.mixer.Sound(i.value)

    def play_music(self, music_enum):
        if self._current_music == music_enum:
            return
        self._current_music = music_enum
        pygame.mixer.music.fadeout(2000)
        pygame.mixer.music.load(music_enum.value)
        pygame.mixer.music.play(-1)

    def play_sound(self, sound):
        if sound in self._sfx.keys():
            self._sfx[sound].stop()
            self._sfx[sound].play()
        else:
            print(f"missing sound for {sound}")

    def play_footsteps(self, movement):
        if movement is 0:
            self._footsteps.stop()
            self._last_footstep = None
        elif not self._footsteps.get_busy():
            if self._last_footstep is SFX.PLAYER_WALK_ONE:
                self._footsteps.play(self._sfx[SFX.PLAYER_WALK_TWO])
                self._last_footstep = SFX.PLAYER_WALK_TWO
            else:
                self._footsteps.play(self._sfx[SFX.PLAYER_WALK_ONE])
                self._last_footstep = SFX.PLAYER_WALK_ONE