from typing import List
import pygame
from Builder import PlayerBuilder
from Menu import Button, Menu
from SoundManager import SoundManager
from ObjectPool import EnemyPool, ProjectilePool
from CollisionRules import COLLISION_RULES
from Enums import Entities, Assets, GameEvents
from UI import Healthbar, LevelTimer, EnemyDeath
from AssetLoader import AssetLoader
from LevelManager import LevelManager

class GameWorld:

    def __init__(self) -> None: #Startup logic
        pygame.init()
        pygame.display.set_caption("Geese invaderz")
        pygame.display.set_icon(AssetLoader.get_sprite(Assets.HVEDER))
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

        self._boss = None
        self._enemies_killed = 0
        self._enemy_pool = EnemyPool(self)
        
        self._menu_bool = True
        self._pause_bool = False

        self._reset_game_bool = False

        self._level_manager = LevelManager(self)
        self._level_manager.active_bool = False
        self._start_manu = Menu(self, Assets.START_MENU)
        self._ui_timer = LevelTimer(self.screen)
        self._enemy_kill_counter = EnemyDeath(self.screen, self)

    @property
    def boss(self):
        return self._boss

    @boss.setter
    def boss(self, value):
        self._boss = value

    @property
    def sound_manager(self):
        return self._sound_manager
    
    @property
    def projectile_pool(self):
        return self._projectile_pool

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
    def level_manager(self):
        return self._level_manager
    
    @property
    def ui_timer(self):
        return self._ui_timer
    
    @property
    def enemy_kill_counter(self):
        return self._enemy_kill_counter

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
        return self._pause_bool
    
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

    @property
    def enemy_pool(self):
        return self._enemy_pool

    def change_level_manager_bool(self, value):
        self.level_manager.active_bool = value
    
    def reset_game(self): #Resets needed parameters for a clean rerun
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

        self._projectile_pool = ProjectilePool(self)
        self._level_manager.active_bool = True
        self._level_manager.reset_level_to_zero()

        self.awake()
        self.start()
    
    def set_background(self, asset: Assets): #
        self._background = AssetLoader.get_sprite(asset)
    
    def show_win_screen(self): #Win screen logic
        if not self._menu_bool:
            Menu(self, Assets.WIN_SCREEN)
            self._menu_bool = True
    
    def show_loose_screen(self): #Loss screen logic
        if not self._menu_bool:
            Menu(self, Assets.LOOSE_SCREEN)
            self._menu_bool = True
    
    def instantiate(self, gameObject): #Initialization logic for all gameObjects
        gameObject.awake(self) 
        gameObject.start()
        self._gameObjects.append(gameObject)

    def subscribe(self, event, method): #For subscribing to events
        self._events[event] = method

    def enemy_death(self, gameObject): #Handles Enemy death
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

    def player_death(self, player): #Handles player death
        self.show_loose_screen()
        self._player.is_destroyed = True
        self._level_manager.active_bool = False

    def spawn_enemy(self, entity_type, position): #Used for spawning enemies
        self.instantiate(self._enemy_pool.get_object(entity_type, position))
        
    def spawn_projectile(self, entity_type, position): #Used for spawning projectiles
        self.instantiate(self._projectile_pool.get_object(entity_type, position))

    def awake(self):

        self.subscribe(GameEvents.ENEMY_DEATH, self.enemy_death)
        self.subscribe(GameEvents.PLAYER_DEATH, self.player_death)

        for gameObject in self._gameObjects[:]:
            gameObject.awake(self)

    def start(self):
       
        if self.level_manager.active_bool == True:
            self.level_manager.start_level()

        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def update(self):
        while self._running:

            delta_time = min((self._clock.tick(60) / 1000.0), 0.05) #Clamps deltatime to avoid jumps when tabbed out/breaks
            if self._pause_bool:
                delta_time = 0

            if self._background:
                self._screen.blit(self._background, (0,0))
            else:
                self._screen.fill("cornflowerblue")

            #Update of UI and manager
            self.level_manager.update(delta_time)
            self._ui_timer.draw()
            self._enemy_kill_counter.draw()

            keys = pygame.key.get_pressed()

            if (self._reset_game_bool == True): #Resets game if triggered
                self.reset_game()
                self._reset_game_bool = False
            
            #Check certain player input
            if keys[pygame.K_ESCAPE]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if keys[pygame.K_p] and self._menu_bool == False:
                Menu(self, Assets.PAUSE)
                self._menu_bool = True
                self._pause_bool = True

            for event in pygame.event.get(): #Checks events
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for text in self._text_button[:]:
                        text.click_on_button()

            for gameObject in self._gameObjects[:]: #Update loop
                gameObject.update(delta_time)

            for text in self._text_button[:]:
                text.update(delta_time)

            for i, collider1 in enumerate(self._colliders): #Collision checks
                entity1 = collider1.gameObject.entity_type

                for j in range(i + 1, len(self._colliders)):
                    collider2 = self._colliders[j]
                    entity2 = collider2.gameObject.entity_type

                    if not self.can_collide(entity1, entity2):
                        continue  

                    if not self.within_x_range(collider1.gameObject, collider2.gameObject):
                        continue

                    collider1.collision_check(collider2)

            self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed] #Remove destroyed objects from updateloop
            self._colliders = [obj for obj in self._colliders if not obj.gameObject.is_destroyed] #Remove collider from colliders

            if self.level_manager.active_bool == True:
                self._healthbar.draw()


            pygame.display.flip()

        pygame.quit()

    def add_to_text_button(self, button): #Adds button
        self._text_button.append(button)

    def can_collide(self, entity_a, entity_b) -> bool: #Checks Rulesets if two objects can collide (used for avoiding needless collisionchecks)
        if entity_a in COLLISION_RULES and entity_b in COLLISION_RULES[entity_a]:
            return True

        if entity_b in COLLISION_RULES and entity_a in COLLISION_RULES[entity_b]:
            return True

        return False
    
    def within_x_range(self, go1, go2, max_distance=500) -> bool: #Checks if two objects are within a certain distance (default is 500 pixels) of each other (used for avoiding needless collisionchecks)
        return abs(go1.transform.position.x - go2.transform.position.x) <= max_distance
    
    def notify(self, event, data=None): #Used to trigger events from other classes
        if event in self._events:
            if data is None:
                self._events[event]()
            else:
                self._events[event](data)

    def boss_exists(self) -> bool: #Checks if enemy is active
        return self._boss in self._gameObjects

gw = GameWorld()

gw.awake()
gw.start()
gw.update()