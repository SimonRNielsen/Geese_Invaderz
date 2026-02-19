from typing import List
import pygame, random
from Builder import PlayerBuilder
from Menu import Button, Menu
from SoundManager import SoundManager
from ObjectPool import EnemyPool, ProjectilePool
from CollisionRules import COLLISION_RULES
from Enums import Entities, Assets, Button_Types, GameEvents
from UI import Healthbar, LevelTimer
from AssetLoader import AssetLoader
from LevelManager import LevelManager

class GameWorld:

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Geese invaderz")
        self._sound_manager = SoundManager()
        self._screen = pygame.display.set_mode((1920,1080))
        self._background = None
        self._running = True
        self._clock = pygame.time.Clock()
        self._gameObjects = []
        self._colliders = []
        self._events = {}
        self._player_score = 0
        self._text_button: List[Button] = []

        self._enemies_killed = 0

        # builder = PlayerBuilder()
        # builder.build()
        # self._player = builder.get_gameObject()
        # self._gameObjects.append(self._player)
 
        # player_entity = builder.get_gameObject().get_component("Entity")
        # self._healthbar = Healthbar(player_entity, self.screen)

        #self._gameObjects.append(self._player)
        self._enemy_pool = EnemyPool(self)
        self._projectile_pool = ProjectilePool(self)
        
        self._menu_bool = True
        self._pause_bool = False

        self._reset_game_bool = False

        self.level_manager = LevelManager(self)
        self.level_manager.active_bool = False
        self._start_manu = Menu(self, Assets.START_MENU)
        self.ui_timer = LevelTimer(self.screen)

    @property
    def screen(self):
        return self._screen
    
    @property
    def colliders(self):
        return self._colliders

    @property
    def texts(self):
        return self._text_button
    
    @texts.setter
    def texts(self, value):
        self._text_button = value

    @property
    def player_alive(self):
        return self._player
    
    @property
    def menu_bool(self):
        return self._menu_bool
    
    @menu_bool.setter
    def menu_bool(self, value):
        self._menu_bool = value
    
    @property
    def pause_bool(self):
        return self.pause_bool
    
    @pause_bool.setter
    def pause_bool(self, value):
        self._pause_bool = value

    @property
    def killed_enemies(self):
        return self._enemies_killed


    @property
    def reset_game_bool(self):
        return self._reset_game_bool
    
    @reset_game_bool.setter
    def reset_game_bool(self, value):
        self._reset_game_bool =value

    # def spawn_main_menu(self):
    #     Menu(self, Assets.START_MENU)

    def change_level_manager_bool(self, value):
        self.level_manager.active_bool = value
    
    def reset_game(self):
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
        self.level_manager.active_bool = True
        self.level_manager.reset_level_to_zero()

        self.awake()
        self.start()
    
    # def reset_game(self):
    #     self._gameObjects = []
    #     self._colliders = []
    #     self._events = {}
    #     self._player_score = 0
    #     self._enemies_killed = 0
    #     builder = PlayerBuilder()
    #     builder.build()
    #     self._gameObjects.append(builder.get_gameObject())
    #     self._enemy_pool = EnemyPool(self)
    #     self._projectile_pool = ProjectilePool(self)
    def set_background(self, asset: Assets):
        self._background = AssetLoader.get_sprite(asset)
    
    def show_win_screen(self):
        if not self._menu_bool:
            Menu(self, Assets.WIN_SCREEN)
            self._menu_bool = True
    
    def show_loose_screen(self):
        if not self._menu_bool:
            Menu(self, Assets.LOOSE_SCREEN)
            self._menu_bool = True
    
    # def reset_game(self):
    #     self._gameObjects = []
    #     self._colliders = []
    #     self._events = {}
    #     self._player_score = 0
    #     self._enemies_killed = 0
    #     builder = PlayerBuilder()
    #     builder.build()
    #     self._gameObjects.append(builder.get_gameObject())
    #     self._enemy_pool = EnemyPool(self)
    #     self._projectile_pool = ProjectilePool(self)
    
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
            case Entities.OBERST:
                self._player_score += 7
            case Entities.GOOSIFER:
                self._player_score += 10

    def player_death(self, player): ####################################################
        self.show_loose_screen()
        self._player.is_destroyed = True
        self.level_manager.active_bool = False
        # self._enemy_pool.set_allowed_enemies = None

    def spawn_enemy(self, entity_type, position):
        self.instantiate(self._enemy_pool.get_object(entity_type, position))
        
    def spawn_projectile(self, entity_type, position):
        self.instantiate(self._projectile_pool.get_object(entity_type, position))

    def awake(self):

        self.subscribe(GameEvents.ENEMY_DEATH, self.enemy_death)
        self.subscribe(GameEvents.PLAYER_DEATH, self.player_death)
        # self.subscribe(GameEvents.RESET_GAME,self.reset_game)
        # self.subscribe(GameEvents.MAIN, self.spawn_main_menu)
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self)

    def start(self):

        #self.spawn_enemy(Entities.GOOSIFER, pygame.math.Vector2(1000,500))
        
        if self.level_manager.active_bool == True:
            self.level_manager.start_level()

        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def update(self):
        while self._running:

            # delta_time = self._clock.tick(60) / 1000.0
            #Pause functionaly => stupid
            if self._pause_bool == False:
                delta_time = self._clock.tick(60) / 1000.0
            else:
                delta_time = 0

            if self._background:
                self._screen.blit(self._background, (0,0))
            else:
                self._screen.fill("cornflowerblue")


            self.level_manager.update(delta_time)
            self.ui_timer.draw()

            keys = pygame.key.get_pressed()

            if (self._reset_game_bool == True):
                self.reset_game()
                self._reset_game_bool = False
            

            if keys[pygame.K_ESCAPE]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if keys[pygame.K_p] and self._menu_bool == False:
                Menu(self, Assets.PAUSE)
                self._menu_bool = True
                self._pause_bool = True

            # if keys[pygame.K_h]:
            #     Menu(self, Assets.WIN_SCREEN)
            

            # if keys[pygame.K_k]:
            #     self._player.is_destroyed = True
            # if self._player.is_destroyed == True and self._menu_bool == False:
            #     Menu(self, Assets.LOOSE_SCREEN)
            #     self._menu_bool = True


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for text in self._text_button[:]:
                        text.click_on_button()


            for gameObject in self._gameObjects[:]:
                gameObject.update(delta_time)

            for text in self._text_button[:]:
                text.update(delta_time)

            for i, collider1 in enumerate(self._colliders):
                entity1 = collider1.gameObject._entity_type

                for j in range(i + 1, len(self._colliders)):
                    collider2 = self._colliders[j]
                    entity2 = collider2.gameObject._entity_type

                    if not self.can_collide(entity1, entity2):
                        continue  

                    if not self.within_x_range(collider1.gameObject, collider2.gameObject):
                        continue

                    collider1.collision_check(collider2)

            self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]
            self._colliders = [obj for obj in self._colliders if not obj.gameObject.is_destroyed]

            if self.level_manager.active_bool == True:
                self._healthbar.draw()

            pygame.display.flip()

        pygame.quit()

    def add_to_text_button(self, button):
        self._text_button.append(button)

    # def add_menu_and_button(self, gameObject):
    #     gameObject.awake(self)
    #     gameObject.start()

    def can_collide(self, entity_a, entity_b) -> bool:
        if entity_a in COLLISION_RULES and entity_b in COLLISION_RULES[entity_a]:
            return True

        if entity_b in COLLISION_RULES and entity_a in COLLISION_RULES[entity_b]:
            return True

        return False
    
    def within_x_range(self, go1, go2, max_distance=500) -> bool:
        return abs(go1.transform.position.x - go2.transform.position.x) <= max_distance

gw = GameWorld()

gw.awake()
gw.start()
gw.update()