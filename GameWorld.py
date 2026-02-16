import pygame, random
from Builder import PlayerBuilder
from Menu import Button, Menu

from ObjectPool import EnemyPool
from Enums import Entities, GameEvents

class GameWorld:

    def __init__(self) -> None:
        pygame.init()
        self._gameObjects = []
        self._colliders = []
        self._events = {}
        self._player_score = 0

        builder = PlayerBuilder()
        builder.build()
        self._gameObjects.append(builder.get_gameObject())
        
        self._enemy_pool = EnemyPool(self)

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

    def subscribe(self, event, method):
        self._events[event] = method

    def enemy_death(self, gameObject):
        match gameObject._entity_type:
            case Entities.WALKING_GOOSE:
                self._player_score += 1
            case Entities.AGGRO_GOOSE:
                self._player_score += 3
            case Entities.SHEEP:
                self._player_score += 7
            case Entities.GOOSIFER:
                self._player_score += 10

    def spawn_enemy(self, entity_type, position):
        self.instantiate(self._enemy_pool.get_object(entity_type, position))

    def awake(self):

        self.subscribe(GameEvents.ENEMY_DEATH, self.enemy_death)

        for gameObject in self._gameObjects[:]:
            gameObject.awake(self)

    def start(self):

        self.spawn_enemy(Entities.GOOSIFER, pygame.math.Vector2(1000,500))

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._button.klik_i_din_rumpe()

            self._screen.fill("cornflowerblue")
            delta_time = self._clock.tick(60) / 1000.0

            for gameObject in self._gameObjects[:]:
                gameObject.update(delta_time)

            for i, collider1 in enumerate(self._colliders):
                for j in range(i+1, len(self._colliders)):
                    collider2 = self._colliders[j]
                    collider1.collision_check(collider2)

            self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]
            self._colliders = [obj for obj in self._colliders if not obj.gameObject.is_destroyed]

            pygame.display.flip()

        pygame.quit()

gw = GameWorld()

gw.awake()
gw.start()
gw.update()