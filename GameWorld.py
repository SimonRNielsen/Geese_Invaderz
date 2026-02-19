from typing import List
import pygame, random
from Builder import PlayerBuilder
from Menu import Button, Menu
from SoundManager import SoundManager
from ObjectPool import EnemyPool, ProjectilePool

from Enums import Entities, Assets, Button_Types, GameEvents
from UI import Healthbar


class GameWorld:

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Geese invaderz")
        self._sound_manager = SoundManager()
        self._screen = pygame.display.set_mode((1920,1080))
        self._running = True
        self._clock = pygame.time.Clock()
        self._gameObjects = []
        self._colliders = []
        self._events = {}
        self._player_score = 0
        self._text_button: List[Button] = []

        self._enemies_killed = 0

        builder = PlayerBuilder()
        builder.build()
        self._player = builder.get_gameObject()
        self._gameObjects.append(self._player)

        player_entity = builder.get_gameObject().get_component("Entity")
        self._healthbar = Healthbar(player_entity, self.screen)

        #self._gameObjects.append(self._player)
        self._enemy_pool = EnemyPool(self)
        self._projectile_pool = ProjectilePool(self)
        
        self._start_manu = Menu(self, Assets.START_MENU)
        self._menu_bool = True

    @property
    def screen(self):
        return self._screen
    
    @property
    def colliders(self):
        return self._colliders

    @property
    def texts(self):
        return self._text_button
    
    @property
    def player_alive(self):
        return self._player
    
    @property
    def menu_bool(self):
        return self.menu_bool
    
    @menu_bool.setter
    def menu_bool(self, value):
        self._menu_bool = value
    
    def spawn_main_menu(self):
        Menu(self, Assets.START_MENU)
    
    def reset_game(self):
        self._gameObjects = []
        self._colliders = []
        self._events = {}
        self._player_score = 0
        self._enemies_killed = 0
        builder = PlayerBuilder()
        builder.build()
        self._gameObjects.append(builder.get_gameObject())
        self._enemy_pool = EnemyPool(self)
        self._projectile_pool = ProjectilePool(self)
    
    def reset_game(self):
        self._gameObjects = []
        self._colliders = []
        self._events = {}
        self._player_score = 0
        self._enemies_killed = 0
        builder = PlayerBuilder()
        builder.build()
        self._gameObjects.append(builder.get_gameObject())
        self._enemy_pool = EnemyPool(self)
        self._projectile_pool = ProjectilePool(self)
    
    def instantiate(self, gameObject):
        gameObject.awake(self) 
        gameObject.start()
        self._gameObjects.append(gameObject)

    def subscribe(self, event, method):
        self._events[event] = method

    def enemy_death(self, gameObject):
        self._enemies_killed += 1
        match gameObject._entity_type:
            case Entities.WALKING_GOOSE:
                self._player_score += 1
            case Entities.AGGRO_GOOSE:
                self._player_score += 3
            case Entities.SHEEP:
                self._player_score += 7
            case Entities.GOOSIFER:
                self._player_score += 10

    def player_death(self, player):
        pass

    def spawn_enemy(self, entity_type, position):
        self.instantiate(self._enemy_pool.get_object(entity_type, position))
        
    def spawn_projectile(self, entity_type, position):
        self.instantiate(self._projectile_pool.get_object(entity_type, position))

    def awake(self):

        self.subscribe(GameEvents.ENEMY_DEATH, self.enemy_death)
        self.subscribe(GameEvents.PLAYER_DEATH, self.player_death)

        self.subscribe(GameEvents.MAIN, self.spawn_main_menu)
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self)

    def start(self):

        self.spawn_enemy(Entities.GOOSIFER, pygame.math.Vector2(2000,500))

        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def update(self):
        while self._running:

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if keys[pygame.K_p] and self._menu_bool == False:
                self._pause = Menu(self, Assets.PAUSE)
                self._menu_bool = True
            if keys[pygame.K_h]:
                Menu(self, Assets.WIN_SCREEN)
            

            if keys[pygame.K_k]:
                self._player.is_destroyed = True
                # self.__kage = Menu(self, Assets.START_MENU)
            if self._player.is_destroyed == True and self._menu_bool == False:
                self._loose = Menu(self, Assets.LOOSE_SCREEN)
                self._menu_bool = True


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for text in self._text_button[:]:
                        text.click_on_button()


            self._screen.fill("cornflowerblue")
            delta_time = self._clock.tick(60) / 1000.0

            for gameObject in self._gameObjects[:]:
                gameObject.update(delta_time)

            #Text update
            for text in self._text_button[:]:
                text.update(delta_time)

  

            for i, collider1 in enumerate(self._colliders):
                for j in range(i+1, len(self._colliders)):
                    collider2 = self._colliders[j]
                    collider1.collision_check(collider2)

            self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]
            self._colliders = [obj for obj in self._colliders if not obj.gameObject.is_destroyed]

            self._healthbar.draw()

            pygame.display.flip()

        pygame.quit()

    def add_to_text_button(self, button):
        self._text_button.append(button)

    # def add_to_gameObjects(self, gameObject):
    #     self._gameObjects.append(gameObject)

    def add_menu_and_button(self, gameObject):
        gameObject.awake(self)
        gameObject.start()



gw = GameWorld()

gw.awake()
gw.start()
gw.update()