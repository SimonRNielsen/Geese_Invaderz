import pygame

class Healthbar:
    def __init__(self, entity, screen):
        self._entity = entity
        self._screen = screen

        self._width = 300
        self._height = 32
        self._margin = 20
        self._border_radius = 8
        self._padding = 6
    
    def _get_color(self, ratio):
        if ratio > 0.6:
            return (60, 200, 80) #Grøn
        elif ratio > 0.3:
            return (230, 200, 60) #Gul
        else:
            return (220, 70, 70) #Rød
    
    def draw(self):

        ratio = max(0, self._entity.health / self._entity.max_health)

        x = self._screen.get_width() - self._width - self._margin
        y = self._margin

        #Baggrund
        bg_rect = pygame.Rect(x, y, self._width, self._height)
        pygame.draw.rect(
            self._screen,
            (30, 30, 30),
            bg_rect,
            border_radius = self._border_radius
        )

        #Healthbar
        inner_width = int((self._width - self._padding * 2) * ratio)
        fg_rect = pygame.Rect(
            x + self._padding,
            y + self._padding,
            inner_width,
            self._height - self._padding * 2
        )

        pygame.draw.rect(
            self._screen,
            self._get_color(ratio),
            fg_rect,
            border_radius = self._border_radius - 3
        )

        #Outline
        pygame.draw.rect(
            self._screen,
            (180, 180, 180),
            bg_rect,
            4,
            border_radius = self._border_radius
        )

class LevelTimer:
    def __init__(self, screen):
        self._screen = screen
        self._time = 0
        self._active = False
        self._font = pygame.font.SysFont("CopperplateGothicBold", 36)
    
    def start(self, seconds):
        self._time = seconds
        self._active = True
    
    def set_time(self, time_left):
        self._time = max(0, int(time_left))
    
    def hide(self):
        self._active = False
    
    def draw(self):
        if not self._active:
            return
        
        text = self._font.render(f"{self._time}", True, (255, 255, 255))
        rect = text.get_rect(center=(self._screen.get_width()/2, 40))
        self._screen.blit(text, rect)

class EnemyDeath:
    def __init__(self, screen, gameworld):
        self._screen = screen
        self._gameworld = gameworld
        self._active = False
        self._font = pygame.font.SysFont("CopperplateGothicBold", 36)

    def start(self):
        self._active = True
    
    def hide(self):
        self._active = False
    
    def draw(self):
        if not self._active:
            return
        
        text = self._font.render(f"Enemies killed: {self._gameworld.killed_enemies}", True, (255, 255, 255))
        rect = text.get_rect(center=(self._screen.get_width() * 2/3, 40))
        self._screen.blit(text, rect)