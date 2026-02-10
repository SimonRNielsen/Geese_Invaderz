import pygame
from Builder import PlayerBuilder

class GameWorld:

    def __init__(self) -> None:
        pygame.init()
        self._gameObjects = []
        self._colliders = []

        builder = PlayerBuilder()
        builder.build()
        self._gameObjects.append(builder.get_gameObject())

        self._screen = pygame.display.set_mode((1920,1080))
        self._running = True
        self._clock = pygame.time.Clock()

    @property
    def screen(self):
        return self._screen
    
    @property
    def colliders(self):
        return self._colliders
    
    def instantiate(self, gameObject):
        gameObject.awake(self)
        gameObject.start()
        self._gameObjects.append(gameObject)

    def awake(self):
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self)

    def start(self):
        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def update(self):
        while self._running:

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            self._screen.fill("cornflowerblue")
            delta_time = self._clock.tick(60) / 1000.0

            for gameObject in self._gameObjects[:]:
                gameObject.update(delta_time)

            for i, collider1 in enumerate(self._colliders):
                for j in range(i+1, len(self._colliders)):
                    collider2 = self._colliders[j]
                    collider1.collision_check(collider2)

            self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]

            pygame.display.flip()

        pygame.quit()

gw = GameWorld()

gw.awake()
gw.start()
gw.update()