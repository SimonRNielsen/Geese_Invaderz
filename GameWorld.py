from typing import List
import pygame, random
from Builder import PlayerBuilder
from Menu import Button, Menu

from ObjectPool import EnemyPool
from Enums import Entities, Assets, Button_Types

class GameWorld:

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Geese invaderz")
        self._screen = pygame.display.set_mode((1920,1080))
        self._gameObjects = []
        self._colliders = []
        self._text_button: List[Button] = []


        builder = PlayerBuilder()
        builder.build(pygame.math.Vector2(0,0)) #960,540
        self._player = builder.get_gameObject()


        self._gameObjects.append(self._player)
        self._enemy_pool = EnemyPool(self)

        self._start_manu = Menu(self, Assets.START_MENU)


        self._running = True
        self._clock = pygame.time.Clock()

    @property
    def screen(self):
        return self._screen
    
    @property
    def colliders(self):
        return self._colliders

    @property
    def texts(self):
        return self._text_button
    
    
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
            if keys[pygame.K_p]:
                print("Pause")
                self._pause = Menu(self, Assets.PAUSE).get_menu()
                self.add_menu_and_button(self._pause)
            if keys[pygame.K_d]:
                self._player.is_destroyed = True



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for text in self._text_button[:]:
                        text.klik_i_din_rumpe()


            self._screen.fill("cornflowerblue")
            delta_time = self._clock.tick(60) / 1000.0

            for gameObject in self._gameObjects[:]:
                gameObject.update(delta_time)

            #Text update
            for text in self._text_button[:]:
                text.update(delta_time)

            if self._player.is_destroyed == True:
                self._loose = Menu(self, Assets.LOOSE_SCREEN).get_menu()
                self.add_menu_and_button(self._loose)

            for i, collider1 in enumerate(self._colliders):
                for j in range(i+1, len(self._colliders)):
                    collider2 = self._colliders[j]
                    collider1.collision_check(collider2)

            self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]
            self._colliders = [obj for obj in self._colliders if not obj.gameObject.is_destroyed]

            pygame.display.flip()

        pygame.quit()

    def add_to_text_button(self, button):
        self._text_button.append(button)

    def add_to_gameObjects(self, gameObject):
        self._gameObjects.append(gameObject)

    def add_menu_and_button(self, gameObject):
        gameObject.awake(self)
        gameObject.start()



gw = GameWorld()

gw.awake()
gw.start()
gw.update()