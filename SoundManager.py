import pygame
from Enums import Music, SFX

class SoundManager:

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(32)
        pygame.mixer.set_reserved(2)
        self._current_music = None
        self._sfx = {}
        self._music = {}
        self.load_sfxs()
        self._music_channel = pygame.mixer.Channel(0)
        self._footsteps = pygame.mixer.Channel(1)
        self.play_music(Music.MENU)
        self._last_footstep = None
            
    def load_sfxs(self):
        for i in SFX:
            self._sfx[i] = pygame.mixer.Sound(i.value)
        for m in Music:
            self._music[m] = pygame.mixer.Sound(m.value)

    def play_music(self, music_enum):
        if self._current_music == music_enum:
            return
        self._current_music = music_enum
        self._music_channel.fadeout(1000)
        self._music_channel.play(self._music[music_enum], loops=-1, fade_ms=1000)

    def play_sound(self, sound):
        if sound in self._sfx.keys():
            self._sfx[sound].stop()
            self._sfx[sound].play()

    def play_footsteps(self, movement):
        if movement == 0:
            self._footsteps.stop()
            self._last_footstep = None
        elif not self._footsteps.get_busy():
            if self._last_footstep is SFX.PLAYER_WALK_ONE:
                self._footsteps.play(self._sfx[SFX.PLAYER_WALK_TWO])
                self._last_footstep = SFX.PLAYER_WALK_TWO
            else:
                self._footsteps.play(self._sfx[SFX.PLAYER_WALK_ONE])
                self._last_footstep = SFX.PLAYER_WALK_ONE